"""
PYTHON FILE HANDLING + EXCEPTION HANDLING
Practice Exercises for Network Engineers
==========================================

Files used:
  - network_devices.txt   (plain text device status log)
  - network_inventory.csv (CSV interface inventory)

Run each exercise function from main() one at a time, or run them all.
Read the comments -- they map directly to the concepts in your notes.
"""

import csv
import os

DEVICES_TXT = "network_devices.txt"
INVENTORY_CSV = "network_inventory.csv"
REPORT_TXT = "down_devices_report.txt"
LOG_TXT = "network_changes.log"


# -------------------------------------------------------------------
# 2 & 3. OPENING + READING A FILE (whole file)
# -------------------------------------------------------------------
def exercise_1_read_whole_file():
    print("\n--- Exercise 1: Read entire device log ---")
    file = open(DEVICES_TXT, "r")
    content = file.read()
    print(content)
    file.close()


# -------------------------------------------------------------------
# 4. READ LINE BY LINE -- find DOWN devices (a real NOC task)
# -------------------------------------------------------------------
def exercise_2_find_down_devices():
    print("\n--- Exercise 2: Find devices that are DOWN ---")
    file = open(DEVICES_TXT, "r")
    for line in file:
        if "Status: DOWN" in line:
            print("ALERT:", line.strip())
    file.close()


# -------------------------------------------------------------------
# 5 & 6. WRITE + APPEND -- generate an outage report
# -------------------------------------------------------------------
def exercise_3_write_down_report():
    print("\n--- Exercise 3: Write a DOWN-devices report (overwrite) ---")
    with open(DEVICES_TXT, "r") as src:
        lines = src.readlines()

    # "w" mode -- overwrites report.txt each time this runs
    with open(REPORT_TXT, "w") as report:
        report.write("=== Down Device Report ===\n")
        for line in lines:
            if "Status: DOWN" in line:
                report.write(line)

    print(f"Report written to {REPORT_TXT}")


def exercise_4_append_change_log():
    print("\n--- Exercise 4: Append an entry to a change log ---")
    # "a" mode -- adds a new line without erasing history.
    # In real NOC work this is exactly how you'd keep a running log.
    with open(LOG_TXT, "a") as log:
        log.write("Checked device status -- see down_devices_report.txt\n")
    print(f"Appended entry to {LOG_TXT}")


# -------------------------------------------------------------------
# 7. with STATEMENT -- recommended pattern (used throughout above too)
# -------------------------------------------------------------------
def exercise_5_with_statement():
    print("\n--- Exercise 5: Safe read using 'with' ---")
    with open(DEVICES_TXT, "r") as file:
        content = file.read()
        print(f"File has {len(content.splitlines())} lines.")


# -------------------------------------------------------------------
# 8. CSV FILES -- parse an interface inventory, count UP vs DOWN
# -------------------------------------------------------------------
def exercise_6_read_csv_inventory():
    print("\n--- Exercise 6: Read CSV inventory ---")
    with open(INVENTORY_CSV, "r") as file:
        reader = csv.reader(file)
        header = next(reader)  # skip header row
        print("Columns:", header)
        for row in reader:
            print(row)


def exercise_7_csv_dictreader_summary():
    print("\n--- Exercise 7: Use DictReader to summarize VLANs ---")
    vlan_counts = {}
    with open(INVENTORY_CSV, "r") as file:
        reader = csv.DictReader(file)  # lets you access columns by name
        for row in reader:
            vlan = row["vlan"]
            vlan_counts[vlan] = vlan_counts.get(vlan, 0) + 1
    print("Devices per VLAN:", vlan_counts)


def exercise_8_write_csv_report():
    print("\n--- Exercise 8: Write a filtered CSV (only UP devices) ---")
    with open(INVENTORY_CSV, "r") as infile:
        reader = csv.DictReader(infile)
        up_devices = [row for row in reader if row["status"] == "UP"]

    with open("up_devices_only.csv", "w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["hostname", "ip_address", "interface", "status", "uptime_days", "vlan"])
        writer.writeheader()
        writer.writerows(up_devices)

    print(f"Wrote {len(up_devices)} UP devices to up_devices_only.csv")


# -------------------------------------------------------------------
# 9, 10, 11, 12. EXCEPTION HANDLING -- realistic network scenarios
# -------------------------------------------------------------------
def exercise_9_basic_try_except():
    print("\n--- Exercise 9: Validate a port number input ---")
    try:
        port = int(input("Enter a TCP/UDP port number: "))
        print("Port accepted:", port)
    except ValueError:
        print("Invalid input -- port must be a number.")


def exercise_10_specific_exceptions_ip_math():
    print("\n--- Exercise 10: Specific exception -- divide subnet hosts ---")
    total_hosts = 256
    try:
        subnets = int(input("Split into how many subnets?: "))
        hosts_per_subnet = total_hosts / subnets
        print(f"Each subnet gets {hosts_per_subnet} hosts.")
    except ZeroDivisionError:
        print("Cannot split into 0 subnets.")
    except ValueError:
        print("Please enter a whole number.")


def exercise_11_file_not_found():
    print("\n--- Exercise 11: Handle a missing config file gracefully ---")
    # This is one of THE most common real-world file errors:
    # trying to read a config that was never generated/uploaded yet.
    filename = "router_config_backup.txt"
    try:
        with open(filename, "r") as file:
            print(file.read())
    except FileNotFoundError:
        print(f"'{filename}' not found. Has the backup job run yet?")


def exercise_12_finally_block():
    print("\n--- Exercise 12: finally always runs (e.g. closing a connection) ---")
    try:
        print("Connecting to device...")
        raise ConnectionError("Simulated SSH timeout")
    except ConnectionError as e:
        print("Error:", e)
    finally:
        print("Closing session (this always runs).")


# -------------------------------------------------------------------
# BONUS: a small combined mini-project -- exactly like your
# "Beginner Practice Programs" list, but network-flavored.
# Ping-sweep-style log simulation -> write results -> handle bad input.
# -------------------------------------------------------------------
def bonus_mini_project_status_checker():
    print("\n--- Bonus: Mini Device Status Checker ---")
    devices = {
        "CORE-SW01": "UP",
        "ACCESS-SW01": "DOWN",
        "ROUTER-EDGE2": "DOWN",
    }

    try:
        name = input("Enter device hostname to check: ").strip()
        status = devices[name]  # KeyError if not found
        print(f"{name} is currently {status}")
    except KeyError:
        print(f"No device named '{name}' found in inventory.")
    finally:
        print("Lookup attempt finished.")


def main():
    exercise_1_read_whole_file()
    exercise_2_find_down_devices()
    exercise_3_write_down_report()
    exercise_4_append_change_log()
    exercise_5_with_statement()
    exercise_6_read_csv_inventory()
    exercise_7_csv_dictreader_summary()
    exercise_8_write_csv_report()

    # Interactive ones -- comment out any you don't want to run right now
    exercise_9_basic_try_except()
    exercise_10_specific_exceptions_ip_math()
    exercise_11_file_not_found()
    exercise_12_finally_block()
    bonus_mini_project_status_checker()


if __name__ == "__main__":
    main()
