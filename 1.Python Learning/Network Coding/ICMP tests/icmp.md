Your Python script is an ICMP network performance testing tool. It sends ICMP Echo Requests to a destination, measures Round Trip Time (RTT), calculates latency percentiles (P10, P50, P95, P99), measures packet loss, and exports the results into CSV files.

I'll explain it section by section, including what each Python function does, why it is used, and how it relates to networking.

# 1. Overall workflow of the script

Start Python script

Load modules and test configuration

Send ICMP Echo Request

Windows ping → 8.8.8.8

Receive Echo Reply or timeout

Extract RTT, status, and timestamp

Repeat 1,000 times

Collect successful RTTs and failures

Calculate statistics

Min, average, max, P10, P50, P95, P99, packet loss

Export CSV reports

Raw packet results + summary statistics

# 2. Importing Python libraries

Your code begins with:

```
import subprocessimport reimport csvimport timeimport mathimport statisticsfrom datetime import datetimefrom pathlib import Path
```

In Python, `import` loads functionality from an existing module.

| Module       | Purpose in your script                        |
| ------------ | --------------------------------------------- |
| `subprocess` | Executes the Windows `ping` command           |
| `re`         | Extracts RTT values using regular expressions |
| `csv`        | Saves measurements into CSV files             |
| `time`       | Controls intervals and measures test duration |
| `math`       | Calculates percentile positions               |
| `statistics` | Calculates average RTT                        |
| `datetime`   | Records timestamps                            |
| `pathlib`    | Creates and manages file paths                |

For example:

```
import subprocesssubprocess.run(["ping", "-n", "1", "8.8.8.8"])
```

This executes the same Windows command you would type manually:

```
ping -n 1 8.8.8.8
```

Important: Your script does not construct ICMP packets itself. It uses the Windows `ping.exe` utility, which handles sending and receiving ICMP messages.

# 3. ICMP test configuration

```
TARGET_IP = "8.8.8.8"PING_COUNT = 1000INTERVAL_SECONDS = 1TIMEOUT_MS = 2000PACKET_SIZE = 32
```

These are configuration variables.

| Variable           | Value     | Explanation                            |
| ------------------ | --------- | -------------------------------------- |
| `TARGET_IP`        | `8.8.8.8` | Destination IP                         |
| `PING_COUNT`       | 1000      | Number of ICMP Echo Requests           |
| `INTERVAL_SECONDS` | 1         | Intended interval between probe starts |
| `TIMEOUT_MS`       | 2000      | Wait up to 2 seconds for a reply       |
| `PACKET_SIZE`      | 32        | ICMP payload size in bytes             |

### What happens when you run this?

Your Windows computer sends an ICMP Echo Request to `8.8.8.8`.

Windows 11

ICMP Echo Request (Type 8)

ICMP Echo Reply (Type 0)

8.8.8.8

RTT = time from sending the Echo Request until receiving its Echo Reply

Suppose:

- Request sent at 10:00:00.000
- Reply received at 10:00:00.065

Then:

\\[ RTT=0.065\times1000=65\text{ ms} \\]

That RTT is recorded as one successful measurement.

# 4. Creating the output directory

```
OUTPUT_DIR = Path.home() / "Desktop" / "ICMP_Results"OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

Let's understand each part.

`Path.home()`

Returns your user home directory. On your Windows computer, this would normally be:

```
C:\Users\v-yaalam
```

`/ "Desktop" / "ICMP_Results"`

The `/` operator in `pathlib` joins directory components. It is not division.

The resulting path is typically:

```
C:\Users\v-yaalam\Desktop\ICMP_Results
```

`mkdir(parents=True, exist_ok=True)`

- `mkdir()` creates a directory.
- `parents=True` creates missing parent directories if necessary.
- `exist_ok=True` prevents an error if the directory already exists.

Note that if your Windows Desktop is redirected to OneDrive, `Path.home() / "Desktop"` might not be your actual Desktop location.

## Generating unique filenames

```
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
```

This generates a date/time string.

For example:

```
20261014_091530
```

Then:

```
RAW_FILE = OUTPUT_DIR / f"icmp_raw_{timestamp}.csv"SUMMARY_FILE = OUTPUT_DIR / f"icmp_summary_{timestamp}.csv"
```

Creates filenames such as:

```
icmp_raw_20261014_091530.csv
icmp_summary_20261014_091530.csv
```

The `f` before the string means f-string, which allows inserting variable values using `{}`.

# 5. Understanding the percentile function

This is one of the most important sections.

```
def percentile(values, percent):    if not values:        return None    values = sorted(values)    rank = (len(values) - 1) * percent / 100    lower = math.floor(rank)    upper = math.ceil(rank)    result = values[lower] + (        values[upper] - values[lower]    ) * (rank - lower)    return round(result, 2)
```

Let's break it down.

### Step A — Define the function

```
def percentile(values, percent):
```

`def` defines a reusable function.

It accepts two arguments:

- `values`: A collection of RTT measurements.
- `percent`: The percentile you want, such as 50, 95, or 99.

For example:

```
percentile([10, 20, 30, 40, 50], 50)
```

Returns:

```
30.0
```

### Step B — Check for empty measurements

```
if not values:    return None
```

Suppose all 1,000 ICMP probes fail.

Then:

```
values = []
```

Without this check, the script would attempt to calculate a percentile from an empty list and raise an error.

`None` means there is no available value.

### Step C — Sort RTT measurements

```
values = sorted(values)
```

Suppose the RTT measurements are:

```
values = [80, 30, 100, 50, 20]
```

After sorting:

```
values = [20, 30, 50, 80, 100]
```

Percentiles require ordered values.

### Step D — Calculate the percentile position

```
rank = (len(values) - 1) * percent / 100
```

Here:

- `len(values)` returns the number of RTT samples.
- `percent` is the desired percentile.
- `rank` is the zero-based position in the sorted data.

Suppose we have five samples:

```
values = [20, 30, 50, 80, 100]
```

For P50:

\\[ rank=(5-1)\times\frac{50}{100}=2 \\]

Python uses zero-based indexing:

| Index | RTT    |
| ----- | ------ |
| 0     | 20 ms  |
| 1     | 30 ms  |
| 2     | 50 ms  |
| 3     | 80 ms  |
| 4     | 100 ms |

Therefore:

```
values[2] = 50
```

P50 is 50 ms.

### Step E — Understand floor and ceil

```
lower = math.floor(rank)upper = math.ceil(rank)
```

`math.floor()` rounds downward to the nearest integer.

`math.ceil()` rounds upward to the nearest integer.

For example:

```
rank = 3.8math.floor(3.8)  # 3math.ceil(3.8)   # 4
```

Why do we need both?

Because the percentile may fall between two RTT measurements.

### Step F — Linear interpolation

```
result = values[lower] + (    values[upper] - values[lower]) * (rank - lower)
```

Let's calculate P95 for the same five samples.

\\[ rank=(5-1)\times0.95=3.8 \\]

Therefore:

```
lower = 3upper = 4
```

The corresponding RTTs are:

```
values[3] = 80values[4] = 100
```

Substituting:

\\[ P95=80+(100-80)\times0.8 \\]

\\[ \boxed{P95=96\text{ ms}} \\]

The script estimates P95 between 80 ms and 100 ms.

This is called linear interpolation. It is a common percentile calculation method, although some testing systems use different definitions.

Interactive percentile example

P50P95P99

Calculated P95

# 96.0 ms

Position (rank)

# 3.80

20

Index 0

30

Index 1

50

Index 2

80

Index 3

100

Index 4

Sorted RTT samples: 20, 30, 50, 80, 100 ms. Highlighted cells are used for interpolation.

Calculation: 80 + (100 − 80) × 0.80 = 96.0 ms

# 6. Understanding the `send_ping()` function

```
def send_ping(target):
```

This function is responsible for sending one ICMP request and interpreting its result.

## A. Constructing the Windows ping command

```
command = [    "ping",    "-4",    "-n", "1",    "-w", str(TIMEOUT_MS),    "-l", str(PACKET_SIZE),    target]
```

Python creates a list of command arguments.

For your configuration, this is equivalent to:

```
ping -4 -n 1 -w 2000 -l 32 8.8.8.8
```

| Option    | Explanation                   |
| --------- | ----------------------------- |
| `-4`      | Force IPv4                    |
| `-n 1`    | Send one Echo Request         |
| `-w 2000` | Reply timeout of 2000 ms      |
| `-l 32`   | Send 32 bytes of ICMP payload |
| `8.8.8.8` | Destination                   |

`str(TIMEOUT_MS)` converts the integer `2000` into the string `"2000"` because command-line arguments are passed as strings.

## B. Executing the command

```
result = subprocess.run(    command,    capture_output=True,    text=True,    timeout=(TIMEOUT_MS / 1000) + 3)
```

This is how Python interacts with the Windows operating system.

`subprocess.run()`

Starts an external process, waits for it to finish, and returns the result.

`capture_output=True`

Captures the command's output rather than printing it directly.

`text=True`

Returns the output as a Python string instead of bytes.

`timeout=(TIMEOUT_MS / 1000) + 3`

Sets a Python process timeout of five seconds:

\\[ 2000/1000+3=5\text{ seconds} \\]

There are two different timeouts here:

- Windows ping timeout: 2 seconds waiting for an ICMP reply.
- Python process timeout: 5 seconds waiting for the `ping.exe` process to finish.

## C. Extracting the RTT

```
output = result.stdout
```

`stdout` means standard output.

For example, Windows might return:

```
Reply from 8.8.8.8: bytes=32 time=25ms TTL=117
```

Now Python must extract `25`.

Your code uses:

```
match = re.search(    r"time\s*([=<])\s*(\d+)\s*ms",    output,    re.IGNORECASE)
```

This is a regular expression (regex).

| Regex part      | Meaning                                |
| --------------- | -------------------------------------- |
| `time`          | Find the word time                     |
| `\s*`           | Allow zero or more spaces              |
| `([=<])`        | Match `=` or `<`                       |
| `(\d+)`         | Capture one or more digits             |
| `ms`            | Match milliseconds                     |
| `re.IGNORECASE` | Ignore uppercase/lowercase differences |

For example:

```
time=25ms
```

Produces:

```
match.group(1)  # "="match.group(2)  # "25"
```

Then:

```
rtt = float(match.group(2))
```

Converts `"25"` to the number `25.0`.

## D. Handling successful replies

```
if result.returncode == 0 and match:
```

This checks that the ping command reported success and the expected RTT text was found.

Then:

```
return "Success", rtt, "Measured"
```

Returns three values:

```
status = "Success"rtt = 25.0note = "Measured"
```

This is called tuple unpacking when the values are assigned to separate variables.

### What happens for `time<1ms`?

Windows sometimes displays:

```
Reply from 192.168.1.1: bytes=32 time<1ms TTL=64
```

Your script returns:

```
return "Success", None, "<1ms"
```

It counts the reply as received, but excludes it from RTT statistics because the exact value is unknown.

That means your percentile calculations could be biased if many replies are under 1 ms.

## E. Handling failures

```
except subprocess.TimeoutExpired:    return "Timeout", None, "Process timeout"
```

If the ping process exceeds five seconds, this handles the exception without crashing the whole script.

```
except Exception as error:    return "Error", None, str(error)
```

This catches other errors, such as an inability to start the ping process.

A failed ping command returns:

```
return "Failed", None, "No reply"
```

One limitation: this status is fairly generic. It could mean an ICMP timeout, destination unreachable, or another ping failure. The script doesn't distinguish every ICMP error.

# 7. Understanding the main function

```
def main():
```

This function coordinates the entire test.

It initializes:

```
results = []rtts = []transmitted = 0received = 0
```

### Why two lists?

`results` stores every probe, including failures.

Example:

```
results = [    {"Sequence": 1, "Status": "Success", "RTT_ms": 25},    {"Sequence": 2, "Status": "Failed", "RTT_ms": None},    {"Sequence": 3, "Status": "Success", "RTT_ms": 30}]
```

`rtts` stores only successfully measured RTT values.

```
rtts = [25.0, 30.0]
```

Why?

Because a packet timeout is not a measured RTT. You shouldn't automatically assign a timeout a latency of 2,000 ms when calculating RTT percentiles.

Packet loss is measured separately.

# 8. Understanding the `for` loop

```
for sequence in range(1, PING_COUNT + 1):
```

With:

```
PING_COUNT = 1000
```

This generates:

```
1, 2, 3, 4, 5, ... 1000
```

Python's `range()` excludes the final boundary, which is why the code uses `PING_COUNT + 1`.

For each iteration:

```
probe_start = time.monotonic()
```

Records the start time for interval measurement.

```
timestamp_now = datetime.now().isoformat(    timespec="milliseconds")
```

Records the wall-clock timestamp, such as:

```
2026-10-14T09:15:30.125
```

Then:

```
status, rtt, note = send_ping(TARGET_IP)
```

Sends one ping.

### Updating counters

```
transmitted += 1
```

This is shorthand for:

```
transmitted = transmitted + 1
```

If the probe succeeds:

```
if status == "Success":    received += 1    if rtt is not None:        rtts.append(rtt)
```

`append()` adds the RTT to the list.

For example:

```
rtts = [25, 30]rtts.append(28)
```

Becomes:

```
[25, 30, 28]
```

# 9. Storing every ICMP result

```
results.append({    "Timestamp": timestamp_now,    "Sequence": sequence,    "Destination": TARGET_IP,    "Status": status,    "RTT_ms": rtt,    "Note": note})
```

The `{}` syntax creates a Python dictionary.

Each dictionary stores one probe.

Example:

```
```



























Great! Your screenshot now shows the exact location of `icmp_test.py`.

Copy and paste this command directly into your VS Code PowerShell terminal:

```
python "C:\Users\v-yaalam\Downloads\vscode_Dell_17-1\1.Python Learning\Network Coding\icmp_test.py"
```

Alternatively, navigate to the script's folder first:

```
cd "C:\Users\v-yaalam\Downloads\vscode_Dell_17-1\1.Python Learning\Network Coding"
```

Then execute:

```
python icmp_test.py
```

### Expected output

If you saved the ICMP testing code from earlier, you should see something similar to:

```
=======================================================
       WINDOWS ICMP LATENCY TEST
=======================================================
Destination : 8.8.8.8
Packets     : 1000
Interval    : 1 sec
Timeout     : 2000 ms
=======================================================

Seq=1 | Status=Success | RTT=25.0
Seq=2 | Status=Success | RTT=28.0
Seq=3 | Status=Success | RTT=26.0
...
```

After all probes complete, the script should display the P50, P95, P99, packet loss, and average RTT, and save the results as CSV files.

With 1,000 probes at approximately one-second intervals, the test should take around 17 minutes, potentially longer if probes time out.

Run the first command now. If another error appears, share the terminal output and I'll help you fix it.

