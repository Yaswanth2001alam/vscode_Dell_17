import subprocess
from datetime import datetime
import os

# EVE-NG IP address
EVE_NG_IP = "192.168.32.128"

# Folder where ping results will be stored
LOG_FOLDER = "ping_results"

# Create folder if it does not already exist
os.makedirs(LOG_FOLDER, exist_ok=True)

# Current timestamp
timestamp = datetime.now()

# Timestamp for file name
file_timestamp = timestamp.strftime("%Y-%m-%d_%H-%M-%S")

# Timestamp shown inside the log
display_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

# New file name for every run
file_name = f"EVE_NG_Ping_{file_timestamp}.txt"

file_path = os.path.join(LOG_FOLDER, file_name)

# Windows ping command
command = [
    "ping",
    "-n", "4",
    EVE_NG_IP
]

print("=" * 60)
print("EVE-NG Ping Test")
print("=" * 60)

print(f"Timestamp : {display_timestamp}")
print(f"Target IP : {EVE_NG_IP}")
print("Running ping test...\n")

try:
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    # Determine status
    if result.returncode == 0:
        status = "UP - Ping Successful"
    else:
        status = "DOWN - Ping Failed"

    print(f"Status: {status}")
    print(result.stdout)

    # Write results into a NEW file
    with open(file_path, "w", encoding="utf-8") as log_file:

        log_file.write("=" * 60 + "\n")
        log_file.write("EVE-NG PING TEST RESULT\n")
        log_file.write("=" * 60 + "\n\n")

        log_file.write(f"Timestamp : {display_timestamp}\n")
        log_file.write(f"Target IP : {EVE_NG_IP}\n")
        log_file.write(f"Status    : {status}\n\n")

        log_file.write("Ping Output:\n")
        log_file.write("-" * 60 + "\n")

        log_file.write(result.stdout)

        if result.stderr:
            log_file.write("\nErrors:\n")
            log_file.write(result.stderr)

    print("\nPing test completed.")
    print(f"Result saved to: {file_path}")

except Exception as error:

    print(f"Error running ping test: {error}")