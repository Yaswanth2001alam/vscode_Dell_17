# BGP Neighbor Validation Automation

Complete automation workflow for validating BGP neighbor relationships on Cisco IOS/IOS-XE devices in EVE-NG labs.

## Overview

This package provides reusable modules and CLI tools to:
- **Validate** BGP neighbor session states
- **Monitor** prefix advertisement and reception
- **Report** on neighbor health and anomalies
- **Integrate** with existing pyATS/Genie workflows

## Features

✓ Parse `show ip bgp summary` using Genie  
✓ Detect neighbor state changes (Established, Down, Idle, etc.)  
✓ Extract prefix metrics (received/advertised)  
✓ Support multiple VRFs  
✓ JSON and human-readable output formats  
✓ Comprehensive error handling  
✓ Fully tested with pytest (30+ unit/integration tests)  

## Installation

### Prerequisites
```bash
pip install pyats[full] genie
```

### Setup
1. Copy the `bgp/` directory to your automation project
2. Prepare a Genie testbed YAML (see `testbed_bgp_sample.yaml`)
3. Run tests to verify: `pytest bgp/test_bgp_neighbor_validator.py -v`

## Quick Start

### 1. Using the CLI Script

Validate all devices in testbed:
```bash
python validate_bgp_neighbors.py --testbed testbed.yaml
```

Validate specific device:
```bash
python validate_bgp_neighbors.py --testbed testbed.yaml --device router1
```

Save JSON report:
```bash
python validate_bgp_neighbors.py --testbed testbed.yaml --report report.json
```

Validate specific VRF:
```bash
python validate_bgp_neighbors.py --testbed testbed.yaml --vrf management
```

### 2. Using the Core Module

```python
from genie.testbed import load
from bgp.bgp_neighbor_validator import BGPNeighborValidator

# Load testbed
testbed = load("testbed.yaml")
device = testbed.devices["router1"]
device.connect()

# Validate BGP neighbors
validator = BGPNeighborValidator(device, vrf="default")
result = validator.validate_neighbors()

# Access results
print(f"Total neighbors: {result.total_neighbors}")
print(f"Established: {result.established_count}")
print(f"Down: {result.down_count}")

# Get unhealthy neighbors
unhealthy = result.get_unhealthy_neighbors()
for neighbor in unhealthy:
    print(f"⚠ {neighbor.ip_address} ({neighbor.state.value})")

# Validate specific neighbor
neighbor = validator.validate_specific_neighbor("192.168.1.1")
if neighbor and neighbor.is_healthy():
    print(f"✓ {neighbor.ip_address} is healthy")

device.disconnect()
```

## Module API

### `BGPNeighborValidator`

Main validation class for BGP neighbors.

**Methods:**

- `validate_neighbors() -> BGPValidationResult`
  - Validate all BGP neighbors for the device
  - Returns result with metrics and neighbor details

- `validate_specific_neighbor(neighbor_ip: str) -> Optional[BGPNeighbor]`
  - Validate a specific neighbor by IP address
  - Returns neighbor object or None

**Example:**
```python
validator = BGPNeighborValidator(device, vrf="default")
result = validator.validate_neighbors()

if result.down_count > 0:
    for neighbor in result.get_unhealthy_neighbors():
        print(f"Alert: {neighbor.ip_address} is {neighbor.state.value}")
```

### `BGPValidationResult`

Data class containing validation results.

**Attributes:**
- `device_name: str` - Device being validated
- `vrf: str` - VRF context
- `neighbors: List[BGPNeighbor]` - List of neighbors
- `total_neighbors: int` - Total neighbor count
- `established_count: int` - Number of established neighbors
- `down_count: int` - Number of down neighbors
- `error_neighbors: int` - Count of other non-healthy states

**Methods:**
- `get_status_summary() -> str` - Human-readable summary
- `get_unhealthy_neighbors() -> List[BGPNeighbor]` - Filter unhealthy neighbors
- `to_dict() -> dict` - Convert to JSON-serializable dict

### `BGPNeighbor`

Data class representing a single BGP neighbor.

**Attributes:**
- `ip_address: str` - Neighbor IP address
- `remote_as: int` - Remote AS number
- `state: BGPNeighborState` - Session state
- `prefixes_received: int` - Prefixes received
- `prefixes_advertised: int` - Prefixes advertised
- `uptime: Optional[str]` - Session uptime

**Methods:**
- `is_healthy() -> bool` - Returns True if state is Established

## CLI Script Usage

### Arguments

- `--testbed FILE` - Path to Genie testbed YAML (default: testbed.yaml)
- `--device NAME` - Validate specific device only
- `--vrf NAME` - VRF to validate (default: default)
- `--report FILE` - Save JSON report to file
- `--verbose` - Enable debug logging

### Exit Codes

- `0` - All neighbors healthy
- `1` - Connection or validation error
- `2` - Neighbors down (warning)

### Example Output

```
======================================================================
  BGP Neighbor Validation
======================================================================

======================================================================
  Device: router1 | VRF: default
======================================================================

  Summary:
    Total Neighbors: 4
    ✓  Established: 3
    Down: 1
    Error/Other: 0

  Neighbors:
    ------------------------------------------------------------------
    IP Address           AS         State           RX Pfx     TX Pfx    
    ------------------------------------------------------------------
    ✓  192.168.1.1       65000      Established     1024       512       
    ✓  192.168.1.2       65001      Established     2048       256       
    ✗  192.168.1.3       65002      Down            0          0         
    ⚠  192.168.1.4       65003      Active          0          0         

  Unhealthy Neighbors:
    ⚠  192.168.1.3 (Down)
    ⚠  192.168.1.4 (Active)

======================================================================
  Validation Summary
======================================================================
  Devices validated: 1/1
  Total neighbors: 4
  ✓  Established: 3
  ✗  Down: 1

  Report saved to: report.json
```

## Testing

Run full test suite:
```bash
pytest bgp/ -v
```

Run with coverage:
```bash
pytest bgp/ --cov=bgp --cov-report=html
```

Run specific test:
```bash
pytest bgp/test_bgp_neighbor_validator.py::TestBGPNeighborValidator::test_validate_neighbors_success -v
```

## Sample Test Data

Mock device fixtures are provided in `conftest.py`:

- `sample_bgp_output_ios_xe` - IOS-XE BGP output with 4 neighbors
- `sample_bgp_output_multicast` - Multi-VRF BGP output

## Troubleshooting

### Parse errors
If Genie cannot parse `show ip bgp summary`, the script falls back to raw command execution.

```python
# Enable debug logging to see parse attempts
import logging
logging.getLogger("bgp").setLevel(logging.DEBUG)
```

### Connection failures
Verify credentials and connectivity:
```bash
python validate_bgp_neighbors.py --testbed testbed.yaml --verbose
```

### Timeout issues
Adjust connection timeout in testbed YAML:
```yaml
connection_options:
  cli:
    timeout: 60  # Increase from 30
```

## Advanced Use Cases

### 1. Monitor specific VRF
```python
validator = BGPNeighborValidator(device, vrf="management")
result = validator.validate_neighbors()
```

### 2. Custom validation logic
```python
result = validator.validate_neighbors()
critical_neighbors = [
    n for n in result.neighbors
    if n.remote_as in [65000, 65001]  # Critical ASes
]
```

### 3. Integration with monitoring systems
```python
result = validator.validate_neighbors()
metrics = {
    "bgp_neighbors_total": result.total_neighbors,
    "bgp_neighbors_established": result.established_count,
    "bgp_neighbors_down": result.down_count,
}
# Send to Prometheus, CloudWatch, etc.
```

## File Structure

```
bgp/
├── __init__.py                    # Package exports
├── bgp_neighbor_validator.py      # Core validation module (250 lines)
├── validate_bgp_neighbors.py      # CLI script (350 lines)
├── conftest.py                    # pytest fixtures
├── test_bgp_neighbor_validator.py # Test suite (320 lines, 30+ tests)
└── ../yaml_files/
    └── testbed_bgp_sample.yaml    # Example testbed config
```

## Performance Notes

- **Parse time**: ~1-2 seconds per device (includes connection)
- **Memory**: ~5-10 MB per validation
- **Parallelization**: Run CLI script via job scheduler for multi-device parallel validation

## Contributing

To extend this module:

1. Add new validation methods to `BGPNeighborValidator`
2. Define new data classes if needed
3. Add tests to `test_bgp_neighbor_validator.py`
4. Update this README with usage examples

## License

Part of the network automation suite.
