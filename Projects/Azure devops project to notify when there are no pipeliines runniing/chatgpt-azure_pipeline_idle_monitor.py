#!/usr/bin/env python3
"""Email when an Azure DevOps project has no queued/running pipelines."""

from __future__ import annotations

import argparse
import json
import logging
import os
import smtplib
import sys
import time
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests


ACTIVE_STATUSES = {"inProgress", "notStarted", "postponed"}


def required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Required environment variable {name} is not set")
    return value


def config() -> dict[str, Any]:
    return {
        "organization": os.getenv("AZDO_ORGANIZATION", "1Wan").strip(),
        "project": os.getenv("AZDO_PROJECT", "SWAN").strip(),
        "pat": required_env("AZDO_PAT"),
        "smtp_host": os.getenv("SMTP_HOST", "smtp.gmail.com").strip(),
        "smtp_port": int(os.getenv("SMTP_PORT", "587")),
        "smtp_user": required_env("SMTP_USER"),
        "smtp_password": required_env("SMTP_PASSWORD"),
        "email_from": os.getenv("EMAIL_FROM", os.getenv("SMTP_USER", "")).strip(),
        "email_to": [x.strip() for x in required_env("EMAIL_TO").split(",") if x.strip()],
        "interval": int(os.getenv("CHECK_INTERVAL_SECONDS", "1800")),
        "state_file": Path(os.getenv("STATE_FILE", ".pipeline_monitor_state.json")),
        "send_recovery": os.getenv("SEND_RECOVERY_EMAIL", "false").lower() in {"1", "true", "yes"},
    }


def fetch_active_builds(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    org = quote(cfg["organization"], safe="")
    project = quote(cfg["project"], safe="")
    url = f"https://dev.azure.com/{org}/{project}/_apis/build/builds"
    response = requests.get(
        url,
        params={"statusFilter": ",".join(sorted(ACTIVE_STATUSES)), "api-version": "7.1"},
        auth=("", cfg["pat"]),
        headers={"Accept": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    builds = response.json().get("value", [])
    # Defensive check in case the service returns extra statuses.
    return [build for build in builds if build.get("status") in ACTIVE_STATUSES]


def load_state(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {"was_idle": False}


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(state, indent=2), encoding="utf-8")
    temporary.replace(path)


def send_email(cfg: dict[str, Any], subject: str, body: str) -> None:
    message = EmailMessage()
    message["From"] = cfg["email_from"]
    message["To"] = ", ".join(cfg["email_to"])
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(cfg["smtp_host"], cfg["smtp_port"], timeout=30) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(cfg["smtp_user"], cfg["smtp_password"])
        smtp.send_message(message)


def check_once(cfg: dict[str, Any], dry_run: bool = False) -> int:
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    active = fetch_active_builds(cfg)
    state = load_state(cfg["state_file"])
    was_idle = bool(state.get("was_idle", False))
    is_idle = not active
    project_url = f'https://dev.azure.com/{cfg["organization"]}/{cfg["project"]}/_build?view=pipelines'

    if is_idle and not was_idle:
        subject = f'[Azure DevOps] No pipelines running in {cfg["project"]}'
        body = (
            f'No queued or running pipelines were found.\n\n'
            f'Organization: {cfg["organization"]}\nProject: {cfg["project"]}\n'
            f'Checked at: {checked_at} (UTC)\nPipelines: {project_url}\n'
        )
        if dry_run:
            logging.info("DRY RUN - would send: %s", subject)
        else:
            send_email(cfg, subject, body)
            logging.warning("Idle alert email sent")
    elif active:
        logging.info("%d active pipeline(s): %s", len(active), ", ".join(
            f'{b.get("definition", {}).get("name", "unknown")} #{b.get("id")}' for b in active
        ))
        if was_idle and cfg["send_recovery"]:
            send_email(
                cfg,
                f'[Azure DevOps] Pipelines running again in {cfg["project"]}',
                f'{len(active)} pipeline(s) are now queued or running.\n\nPipelines: {project_url}\n',
            )
    else:
        logging.info("Still idle; duplicate email suppressed")

    # A dry run must not suppress the first real alert by changing persistent state.
    if not dry_run:
        save_state(cfg["state_file"], {"was_idle": is_idle, "checked_at_utc": checked_at})
    return 0 if active else 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Check once and exit")
    parser.add_argument("--dry-run", action="store_true", help="Do not send idle email")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    try:
        cfg = config()
        if args.once:
            return check_once(cfg, args.dry_run)
        while True:
            try:
                check_once(cfg, args.dry_run)
            except (requests.RequestException, smtplib.SMTPException, OSError, ValueError) as exc:
                logging.exception("Monitor check failed: %s", exc)
            time.sleep(cfg["interval"])
    except (RuntimeError, ValueError) as exc:
        logging.error("Configuration error: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
