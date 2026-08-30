import os
import platform
import subprocess
import time
import smtplib
import requests

from datetime import datetime
from email.mime.text import MIMEText


# ============================================================
# CONFIGURATION
# ============================================================

EVE_NG_IP = "192.168.32.128"

# Recommended: 300 seconds = 5 minutes
# Change to 3600 if you really want once every hour.
CHECK_INTERVAL = 300

# Send DOWN alert only after this many failures
FAILURE_THRESHOLD = 3

# Teams Workflow webhook URL
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")

# Gmail settings
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# You can send the notification to yourself
EMAIL_TO = os.getenv("EMAIL_TO")


# ============================================================
# PING FUNCTION
# ============================================================

def ping_host(ip_address):
    """
    Ping the target IP once.
    Returns True if reachable, otherwise False.
    """

    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", "-w", "3000", ip_address]

    else:
        command = ["ping", "-c", "1", "-W", "3", ip_address]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return result.returncode == 0

    except Exception as error:
        print(f"Ping error: {error}")
        return False


# ============================================================
# TEAMS ALERT
# ============================================================

def send_teams_alert(message):

    if not TEAMS_WEBHOOK_URL:
        print("Teams webhook not configured.")
        return

    payload = {
        "text": message
    }

    try:
        response = requests.post(
            TEAMS_WEBHOOK_URL,
            json=payload,
            timeout=10
        )

        response.raise_for_status()

        print("Teams notification sent.")

    except Exception as error:
        print(f"Teams notification failed: {error}")


# ============================================================
# GMAIL ALERT
# ============================================================

def send_email_alert(subject, message):

    if not GMAIL_USER or not GMAIL_APP_PASSWORD or not EMAIL_TO:
        print("Gmail configuration missing.")
        return

    email = MIMEText(message)

    email["Subject"] = subject
    email["From"] = GMAIL_USER
    email["To"] = EMAIL_TO

    try:

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as server:

            server.login(
                GMAIL_USER,
                GMAIL_APP_PASSWORD
            )

            server.send_message(email)

        print("Gmail notification sent.")

    except Exception as error:
        print(f"Gmail notification failed: {error}")


# ============================================================
# DOWN ALERT
# ============================================================

def send_down_alert():

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    message = f"""
🚨 EVE-NG DOWN ALERT

EVE-NG machine is unreachable.

IP Address:
{EVE_NG_IP}

Status:
PING FAILED

Failure threshold:
{FAILURE_THRESHOLD} consecutive ping failures

Detected:
{timestamp}

Please check:
• VMware / EVE-NG VM status
• Network adapter
• EVE-NG management interface
• Host routing
• Firewall
"""

    print(message)

    send_teams_alert(message)

    send_email_alert(
        subject=f"🚨 EVE-NG DOWN - {EVE_NG_IP}",
        message=message
    )


# ============================================================
# RECOVERY ALERT
# ============================================================

def send_recovery_alert():

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    message = f"""
✅ EVE-NG RECOVERED

EVE-NG machine is reachable again.

IP Address:
{EVE_NG_IP}

Status:
PING SUCCESS

Recovered:
{timestamp}
"""

    print(message)

    send_teams_alert(message)

    send_email_alert(
        subject=f"✅ EVE-NG RECOVERED - {EVE_NG_IP}",
        message=message
    )


# ============================================================
# MONITOR
# ============================================================

def monitor():

    consecutive_failures = 0

    device_down = False

    print("=" * 60)
    print("EVE-NG Availability Monitor")
    print("=" * 60)

    print(f"Target IP       : {EVE_NG_IP}")
    print(f"Check interval  : {CHECK_INTERVAL} seconds")
    print(f"Failure limit   : {FAILURE_THRESHOLD}")
    print("=" * 60)

    while True:

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        reachable = ping_host(EVE_NG_IP)

        # -----------------------------------------------------
        # Device reachable
        # -----------------------------------------------------

        if reachable:

            print(
                f"[{current_time}] "
                f"{EVE_NG_IP} - UP"
            )

            consecutive_failures = 0

            # Device was previously down
            if device_down:

                send_recovery_alert()

                device_down = False

        # -----------------------------------------------------
        # Device unreachable
        # -----------------------------------------------------

        else:

            consecutive_failures += 1

            print(
                f"[{current_time}] "
                f"{EVE_NG_IP} - DOWN "
                f"(failure {consecutive_failures}/"
                f"{FAILURE_THRESHOLD})"
            )

            # Send alert only once
            if (
                consecutive_failures >= FAILURE_THRESHOLD
                and not device_down
            ):

                send_down_alert()

                device_down = True

        time.sleep(CHECK_INTERVAL)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    try:
        monitor()

    except KeyboardInterrupt:

        print("\nMonitoring stopped.")