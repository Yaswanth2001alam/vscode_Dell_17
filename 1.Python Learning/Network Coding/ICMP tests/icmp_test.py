import subprocess
import re
import csv
import time
import math
import statistics
from datetime import datetime
from pathlib import Path

# ==========================================
# ICMP TEST CONFIGURATION
# ==========================================

TARGET_IP = "8.8.8.8"
PING_COUNT = 1000
INTERVAL_SECONDS = 1
TIMEOUT_MS = 2000
PACKET_SIZE = 32

# Output directory
OUTPUT_DIR = Path.home() / "Desktop" / "ICMP_Results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

RAW_FILE = OUTPUT_DIR / f"icmp_raw_{timestamp}.csv"
SUMMARY_FILE = OUTPUT_DIR / f"icmp_summary_{timestamp}.csv"


# ==========================================
# PERCENTILE CALCULATION
# ==========================================

def percentile(values, percent):
    if not values:
        return None

    values = sorted(values)

    rank = (len(values) - 1) * percent / 100

    lower = math.floor(rank)
    upper = math.ceil(rank)

    result = values[lower] + (
        values[upper] - values[lower]
    ) * (rank - lower)

    return round(result, 2)


# ==========================================
# SEND ICMP PING
# ==========================================

def send_ping(target):
    command = [
        "ping",
        "-4",
        "-n", "1",
        "-w", str(TIMEOUT_MS),
        "-l", str(PACKET_SIZE),
        target
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=(TIMEOUT_MS / 1000) + 3
        )

        output = result.stdout

        # Handles time=25ms and time<1ms
        match = re.search(
            r"time\s*([=<])\s*(\d+)\s*ms",
            output,
            re.IGNORECASE
        )

        if result.returncode == 0 and match:
            rtt = float(match.group(2))

            if match.group(1) == "<":
                # Windows reports only an upper bound
                # for time<1ms; exact RTT is unknown.
                return "Success", None, "<1ms"

            return "Success", rtt, "Measured"

        return "Failed", None, "No reply"

    except subprocess.TimeoutExpired:
        return "Timeout", None, "Process timeout"

    except Exception as error:
        return "Error", None, str(error)


# ==========================================
# RUN ICMP TEST
# ==========================================

def main():

    results = []
    rtts = []

    transmitted = 0
    received = 0

    print("=" * 55)
    print("       WINDOWS ICMP LATENCY TEST")
    print("=" * 55)
    print(f"Destination : {TARGET_IP}")
    print(f"Packets     : {PING_COUNT}")
    print(f"Interval    : {INTERVAL_SECONDS} sec")
    print(f"Timeout     : {TIMEOUT_MS} ms")
    print("=" * 55)

    test_start = time.monotonic()

    for sequence in range(1, PING_COUNT + 1):

        probe_start = time.monotonic()
        timestamp_now = datetime.now().isoformat(
            timespec="milliseconds"
        )

        status, rtt, note = send_ping(TARGET_IP)

        transmitted += 1

        if status == "Success":
            received += 1

            if rtt is not None:
                rtts.append(rtt)

        results.append({
            "Timestamp": timestamp_now,
            "Sequence": sequence,
            "Destination": TARGET_IP,
            "Status": status,
            "RTT_ms": rtt,
            "Note": note
        })

        print(
            f"Seq={sequence} | "
            f"Status={status} | "
            f"RTT={rtt if rtt is not None else note}"
        )

        # Maintain approximately one probe per interval.
        # If a timeout exceeds the interval, the next
        # probe begins immediately.
        elapsed = time.monotonic() - probe_start
        remaining = INTERVAL_SECONDS - elapsed

        if remaining > 0 and sequence < PING_COUNT:
            time.sleep(remaining)

    duration = time.monotonic() - test_start

    lost = transmitted - received
    loss_percent = (lost / transmitted) * 100

    summary = {
        "Destination": TARGET_IP,
        "Transmitted": transmitted,
        "Received": received,
        "Lost": lost,
        "Packet_Loss_Percent": round(loss_percent, 4),
        "Duration_Seconds": round(duration, 2),
        "RTT_Samples": len(rtts),
        "Min_RTT_ms": min(rtts) if rtts else None,
        "Avg_RTT_ms": (
            round(statistics.mean(rtts), 2)
            if rtts else None
        ),
        "Max_RTT_ms": max(rtts) if rtts else None,
        "P10_ms": percentile(rtts, 10),
        "P50_ms": percentile(rtts, 50),
        "P95_ms": percentile(rtts, 95),
        "P99_ms": percentile(rtts, 99)
    }

    # Save raw ICMP measurements
    with open(RAW_FILE, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)

    # Save summary
    with open(SUMMARY_FILE, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=summary.keys()
        )
        writer.writeheader()
        writer.writerow(summary)

    print("\n" + "=" * 55)
    print("             ICMP TEST SUMMARY")
    print("=" * 55)

    for key, value in summary.items():
        print(f"{key:25}: {value}")

    print("\nRaw results:", RAW_FILE)
    print("Summary:", SUMMARY_FILE)


if __name__ == "__main__":
    main()
