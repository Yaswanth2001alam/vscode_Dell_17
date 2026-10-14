
import socket
import time
import csv
import math
import statistics
from datetime import datetime
from pathlib import Path

# ==========================================
# TCP TEST CONFIGURATION
# ==========================================

TARGET_IP = "8.8.8.8"
TARGET_PORT = 53

TEST_COUNT = 1000
INTERVAL_SECONDS = 1
TIMEOUT_SECONDS = 2

# ==========================================
# OUTPUT FILES
# ==========================================

OUTPUT_DIR = Path.home() / "Desktop" / "TCP_Results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

RAW_FILE = OUTPUT_DIR / f"tcp_raw_{timestamp}.csv"
SUMMARY_FILE = OUTPUT_DIR / f"tcp_summary_{timestamp}.csv"

# ==========================================
# PERCENTILE FUNCTION
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
# TCP CONNECTION TEST
# ==========================================

def tcp_ping(ip, port, timeout):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(timeout)

    start = time.perf_counter()

    try:
        sock.connect((ip, port))

        end = time.perf_counter()

        latency_ms = (end - start) * 1000

        return "Success", round(latency_ms, 3), "Connected"

    except socket.timeout:
        return "Timeout", None, "Connection timeout"

    except ConnectionRefusedError:
        return "Refused", None, "Connection refused"

    except OSError as error:
        return "Error", None, str(error)

    finally:
        sock.close()


# ==========================================
# MAIN TCP TEST
# ==========================================

def main():

    results = []
    latencies = []

    print("=" * 60)
    print("           WINDOWS TCP PING TEST")
    print("=" * 60)
    print(f"Destination : {TARGET_IP}")
    print(f"TCP Port    : {TARGET_PORT}")
    print(f"Test Count  : {TEST_COUNT}")
    print(f"Interval    : {INTERVAL_SECONDS} seconds")
    print(f"Timeout     : {TIMEOUT_SECONDS} seconds")
    print("=" * 60)

    test_start = time.monotonic()

    for sequence in range(1, TEST_COUNT + 1):

        probe_start = time.monotonic()

        timestamp_now = datetime.now().isoformat(
            timespec="milliseconds"
        )

        status, latency, note = tcp_ping(
            TARGET_IP,
            TARGET_PORT,
            TIMEOUT_SECONDS
        )

        results.append({
            "Timestamp": timestamp_now,
            "Sequence": sequence,
            "Destination": TARGET_IP,
            "Port": TARGET_PORT,
            "Status": status,
            "TCP_Connect_ms": latency,
            "Note": note
        })

        if status == "Success":
            latencies.append(latency)

        print(
            f"Seq={sequence} | "
            f"TCP={TARGET_PORT} | "
            f"Status={status} | "
            f"Connect={latency} ms"
        )

        elapsed = time.monotonic() - probe_start
        remaining = INTERVAL_SECONDS - elapsed

        if remaining > 0 and sequence < TEST_COUNT:
            time.sleep(remaining)

    duration = time.monotonic() - test_start

    # ==========================================
    # TCP STATISTICS
    # ==========================================

    transmitted = len(results)
    successful = len(latencies)
    failed = transmitted - successful

    failure_percent = (
        failed / transmitted * 100
        if transmitted else 0
    )

    timeout_count = sum(
        1 for r in results if r["Status"] == "Timeout"
    )

    refused_count = sum(
        1 for r in results if r["Status"] == "Refused"
    )

    error_count = sum(
        1 for r in results if r["Status"] == "Error"
    )

    # Consecutive failure statistics
    current_streak = 0
    max_failure_streak = 0

    for r in results:
        if r["Status"] != "Success":
            current_streak += 1
            max_failure_streak = max(
                max_failure_streak,
                current_streak
            )
        else:
            current_streak = 0

    summary = {
        "Destination": TARGET_IP,
        "Port": TARGET_PORT,
        "Attempts": transmitted,
        "Successful": successful,
        "Failed": failed,
        "Failure_Percent": round(failure_percent, 4),
        "Timeouts": timeout_count,
        "Refused": refused_count,
        "Errors": error_count,
        "Max_Consecutive_Failures": max_failure_streak,
        "Duration_Seconds": round(duration, 2),
        "Min_TCP_ms": min(latencies) if latencies else None,
        "Avg_TCP_ms": (
            round(statistics.mean(latencies), 2)
            if latencies else None
        ),
        "Max_TCP_ms": max(latencies) if latencies else None,
        "P10_ms": percentile(latencies, 10),
        "P50_ms": percentile(latencies, 50),
        "P95_ms": percentile(latencies, 95),
        "P99_ms": percentile(latencies, 99)
    }

    # ==========================================
    # EXPORT RAW RESULTS
    # ==========================================

    with open(RAW_FILE, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)

    # ==========================================
    # EXPORT SUMMARY
    # ==========================================

    with open(SUMMARY_FILE, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=summary.keys()
        )
        writer.writeheader()
        writer.writerow(summary)

    # ==========================================
    # DISPLAY RESULTS
    # ==========================================

    print("\n" + "=" * 60)
    print("             TCP TEST SUMMARY")
    print("=" * 60)

    for key, value in summary.items():
        print(f"{key:30}: {value}")

    print("\nRaw CSV:", RAW_FILE)
    print("Summary CSV:", SUMMARY_FILE)


if __name__ == "__main__":
    main()
