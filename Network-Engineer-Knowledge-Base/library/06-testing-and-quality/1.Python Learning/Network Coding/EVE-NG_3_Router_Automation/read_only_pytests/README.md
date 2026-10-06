# Read-only live-device pytest suite

These tests connect to R1, R2, and R3 and execute only commands beginning with
`show` or `ping`. The command wrapper rejects every other command, and the suite
never enters configuration mode or saves configuration.

## Run

From PowerShell:

```powershell
Set-Location "C:\Users\v-yaalam\Downloads\vscode_Dell_17-1\1.Python Learning\Network Coding\EVE-NG_3_Router_Automation\read_only_pytests"
python -m pip install -r requirements.txt
python -m pytest -v
```

The suite automatically reads the parent lab's git-ignored `.env` and
`inventory.json`.

Run only one protocol or category:

```powershell
python -m pytest -v test_ospf.py
python -m pytest -v test_bgp.py
python -m pytest -v test_interfaces.py
python -m pytest -v test_routing_and_reachability.py
python -m pytest -v test_operations.py
```

Run against selected routers:

```powershell
c
python -m pytest -v --routers R1 R3
```

Every command output is saved as JSON under a timestamped folder in `results\`.
The latest overall pytest status is written to `results\latest_summary.json`.

## Coverage

- Management TCP/22 and SSH
- Hostname and device access
- Management, transit, and loopback interface state
- Interface descriptions, input errors, and CRC errors
- OSPF process, router IDs, FULL neighbors, network types, and LSDB
- BGP local ASNs, established peers, received prefixes, and BGP table
- Direct peer and all-loopback reachability
- Route availability and CEF
- CDP topology
- CPU, memory, interface state, and critical logs
