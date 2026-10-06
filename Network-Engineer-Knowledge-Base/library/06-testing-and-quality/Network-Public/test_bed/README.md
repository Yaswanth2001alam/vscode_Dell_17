# EVE-NG IOS-XRv Lab — pyATS Health Check Kit

## Files
- `testbed.yaml`  — device inventory (edit IPs + hostnames)
- `check_lab.py`  — automated health check script

## Quick start

### 1. Install dependencies
```bash
python3 -m venv netauto-env
source netauto-env/bin/activate
pip install pyats[full] genie
```

### 2. Edit testbed.yaml
Update the two IP addresses to match your EVE-NG pnet0 assignments:
```yaml
ip: 192.168.100.10   # XRv-PE1
ip: 192.168.100.11   # XRv-PE2
```
Also ensure the device key name (XRv-PE1 / XRv-PE2) matches the
router's configured hostname exactly.

### 3. Set credentials
```bash
export NET_USER=admin
export NET_PASS=admin
```

### 4. Validate testbed
```bash
pyats validate testbed testbed.yaml
```

### 5. Run checks
```bash
# All devices
python check_lab.py

# Single device only
python check_lab.py --device XRv-PE1

# Save JSON report
python check_lab.py --report report.json
```

## What each check does

| Check | Command used | What to look for |
|---|---|---|
| Interface status | show interfaces | oper=up, line=up |
| Bundle-Ether | show bundle | Members with SA (Selected Active) flags |
| MACsec | show macsec summary + detail | session_state = Secured |
| BGP | show bgp summary | session_state = Established |

## Adding more devices
Copy one of the device blocks in testbed.yaml, update the name,
IP, and topology interfaces. The script auto-loops over all devices.

## IOS-XRv SSH setup (if not already done)
```
ssh server v2
ssh server vrf mgmt
!
username admin
 group root-lr
 secret admin
!
```
