#!/usr/bin/env python3
"""
Azure DevOps Pipeline Monitor
------------------------------
Checks whether any pipelines are currently running (queued or in-progress)
in a given Azure DevOps project, and sends an email alert if none are running.

Recommended usage: run this script every 30 minutes via cron (Linux/Mac) or
Task Scheduler (Windows). A single-check design like this is more reliable
than a long-running Python loop, because the OS scheduler will keep re-running
it even if the machine reboots or the previous run crashed.

If you'd rather have the script loop forever on its own, pass --loop.

------------------------------------------------------------------------------
SETUP
------------------------------------------------------------------------------
1. Create an Azure DevOps Personal Access Token (PAT):
   Azure DevOps -> User Settings -> Personal Access Tokens -> New Token
   Scope needed: "Build (Read)"  (Read-only is enough)

2. Set the following environment variables (don't hardcode secrets in the script):
   Linux/Mac:
       export AZDO_PAT="your_pat_here"
       export SMTP_PASSWORD="your_email_app_password"

   Windows (PowerShell):
       setx AZDO_PAT "your_pat_here"
       setx SMTP_PASSWORD "your_email_app_password"

3. Edit the CONFIG section below (org, project, email settings).

4. Install dependency:
       pip install requests

5. Test it manually:
       python check_pipelines.py

6. Schedule it:
   Linux/Mac (crontab -e):
       */30 * * * * /usr/bin/python3 /path/to/check_pipelines.py >> /path/to/pipeline_monitor.log 2>&1

   Windows Task Scheduler:
       Create a Basic Task -> Trigger: Repeat every 30 minutes ->
       Action: Start a program -> python.exe -> Arguments: C:\path\to\check_pipelines.py
------------------------------------------------------------------------------
"""

import os
import sys
import json
import time
import base64
import logging
import smtplib
import argparse
from email.mime.text import MIMEText
from datetime import datetime, timezone

import requests

# ============================== CONFIG =====================================

ORGANIZATION = "1Wan"                 # from your URL: dev.azure.com/1Wan
PROJECT = "SWAN"                      # from your URL: /SWAN/_build

# Optional: limit the check to specific pipeline definitions (by name).
# Leave as None to check ALL pipelines in the project.
PIPELINE_NAME_FILTER = None           # e.g. ["WAN Chaos Test Pipeline", "wan-oob-nightly"]

# Email (SMTP) settings
SMTP_SERVER = "smtp.office365.com"    # e.g. smtp.gmail.com, smtp.office365.com
SMTP_PORT = 587
SMTP_USERNAME = "your_email@company.com"
EMAIL_FROM = "your_email@company.com"
EMAIL_TO = ["you@company.com", "teammate@company.com"]
EMAIL_SUBJECT = "[Alert] No Azure DevOps pipelines currently running"

# Avoid re-sending an email every single 30-min check while the "no pipelines
# running" condition persists. Only re-alert after this many minutes.
RE_ALERT_INTERVAL_MINUTES = 120

# Where to store "last alert sent" state so repeated runs know not to spam you
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pipeline_monitor_state.json")

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pipeline_monitor.log")

# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)


def get_pat():
    pat = os.environ.get("AZDO_PAT")
    if not pat:
        log.error("AZDO_PAT environment variable is not set. See setup instructions.")
        sys.exit(1)
    return pat


def get_auth_header(pat):
    token = base64.b64encode(f":{pat}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def get_running_builds(pat):
    """
    Queries Azure DevOps for builds that are currently in progress or not yet started.
    Docs: https://learn.microsoft.com/en-us/rest/api/azure/devops/build/builds/list
    """
    url = f"https://dev.azure.com/{ORGANIZATION}/{PROJECT}/_apis/build/builds"
    params = {
        "statusFilter": "inProgress,notStarted",
        "api-version": "7.1",
    }
    headers = get_auth_header(pat)

    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    builds = data.get("value", [])

    if PIPELINE_NAME_FILTER:
        builds = [b for b in builds if b.get("definition", {}).get("name") in PIPELINE_NAME_FILTER]

    return builds


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def should_send_alert(state):
    last_alert = state.get("last_alert_utc")
    if not last_alert:
        return True
    last_alert_dt = datetime.fromisoformat(last_alert)
    minutes_since = (datetime.now(timezone.utc) - last_alert_dt).total_seconds() / 60
    return minutes_since >= RE_ALERT_INTERVAL_MINUTES


def send_email_alert():
    smtp_password = os.environ.get("SMTP_PASSWORD")
    if not smtp_password:
        log.error("SMTP_PASSWORD environment variable is not set. Cannot send email.")
        return False

    body = (
        f"No Azure DevOps pipelines are currently running or queued.\n\n"
        f"Organization: {ORGANIZATION}\n"
        f"Project: {PROJECT}\n"
        f"Checked at (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"View pipelines: https://dev.azure.com/{ORGANIZATION}/{PROJECT}/_build?view=pipelines\n"
    )

    msg = MIMEText(body)
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(EMAIL_TO)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.starttls()
            server.login(SMTP_USERNAME, smtp_password)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        log.info("Alert email sent to %s", EMAIL_TO)
        return True
    except Exception as e:
        log.error("Failed to send email: %s", e)
        return False


def run_check():
    pat = get_pat()
    try:
        running_builds = get_running_builds(pat)
    except requests.exceptions.RequestException as e:
        log.error("Failed to query Azure DevOps API: %s", e)
        return

    if running_builds:
        names = ", ".join(b.get("definition", {}).get("name", "unknown") for b in running_builds)
        log.info("%d pipeline(s) running/queued: %s", len(running_builds), names)
        # Reset alert state so the next "no pipelines running" event alerts immediately
        save_state({})
        return

    log.warning("No pipelines currently running or queued.")
    state = load_state()
    if should_send_alert(state):
        if send_email_alert():
            state["last_alert_utc"] = datetime.now(timezone.utc).isoformat()
            save_state(state)
    else:
        log.info("Skipping email — already alerted within the last %d minutes.", RE_ALERT_INTERVAL_MINUTES)


def main():
    parser = argparse.ArgumentParser(description="Monitor Azure DevOps pipelines and email if none are running.")
    parser.add_argument("--loop", action="store_true", help="Run continuously, checking every 30 minutes.")
    parser.add_argument("--interval", type=int, default=30, help="Minutes between checks in --loop mode (default 30).")
    args = parser.parse_args()

    if args.loop:
        log.info("Starting continuous monitor loop (every %d minutes). Press Ctrl+C to stop.", args.interval)
        while True:
            run_check()
            time.sleep(args.interval * 60)
    else:
        run_check()


if __name__ == "__main__":
    main()
