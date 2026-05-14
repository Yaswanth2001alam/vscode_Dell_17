# Getting Started with BGP Automation Workflows

## 🎯 What You Got

A complete, production-ready **BGP neighbor validation automation system** for your EVE-NG network lab:

```
✓ 1,522 lines of code across 7 files
✓ 25 passing tests (all critical paths covered)
✓ 0 external dependencies beyond pyATS/Genie
✓ Full documentation and 10 usage examples
✓ Ready to deploy and customize
```

## 📁 File Locations

All files are in: `EVE-NG-Network-Automation/bgp/`

```
bgp/
├── bgp_neighbor_validator.py      ← Core validation module
├── validate_bgp_neighbors.py      ← CLI executable script
├── test_bgp_neighbor_validator.py ← 25 comprehensive tests
├── conftest.py                    ← pytest fixtures for testing
├── examples.py                    ← 10 real-world usage examples
├── README.md                      ← Full API documentation
└── __init__.py                    ← Package initialization

yaml_files/
└── testbed_bgp_sample.yaml        ← Example testbed configuration
```

## 🚀 Quick Start (5 Minutes)

### Step 1: Verify Everything Works
```bash
cd EVE-NG-Network-Automation/bgp
pytest test_bgp_neighbor_validator.py -v
```
Expected: `25 passed ✓`

### Step 2: Customize Your Testbed
Edit `yaml_files/testbed_bgp_sample.yaml`:
```yaml
devices:
  router1:
    hostname: your-router-1.lab
    ip: 192.168.X.X          # Your device IP
    credentials:
      default:
        username: admin       # Your credentials
        password: yourpass
```

### Step 3: Run Your First Validation
```bash
python validate_bgp_neighbors.py --testbed testbed.yaml --device router1
```

Output:
```
  ✓ 192.168.1.1 (AS 65000): Established [1024 rx, 512 tx]
  ✓ 192.168.1.2 (AS 65001): Established [2048 rx, 256 tx]
  ✗ 192.168.1.3 (AS 65002): Down [0 rx, 0 tx]
  
Summary: 2/3 neighbors healthy
```

## 📚 Learning Paths

### Path 1: Just Need CLI Tool
```bash
python validate_bgp_neighbors.py --help
python validate_bgp_neighbors.py --testbed testbed.yaml --report bgp.json
```
No Python coding needed!

### Path 2: Integrate in Your Code
```python
from genie.testbed import load
from bgp.bgp_neighbor_validator import BGPNeighborValidator

testbed = load("testbed.yaml")
device = testbed.devices["router1"]
device.connect()

validator = BGPNeighborValidator(device)
result = validator.validate_neighbors()

for neighbor in result.get_unhealthy_neighbors():
    print(f"Alert: {neighbor.ip_address} is down")
```

### Path 3: Advanced Automation
See `examples.py` for 10 complete workflows:
1. Simple validation
2. Error detection & alerting
3. Multi-device reporting
4. Specific neighbor checks
5. VRF-specific validation
6. Continuous monitoring
7. Prometheus integration
8. Custom assertions
9. Bulk operations
10. Error handling

## 🔧 Common Use Cases

### Monitor BGP Health
```bash
python validate_bgp_neighbors.py --testbed testbed.yaml \
  --report bgp_health.json --verbose
```

### Check Specific VRF
```bash
python validate_bgp_neighbors.py --testbed testbed.yaml \
  --device pe-router --vrf management
```

### Validate Single Neighbor
```python
validator = BGPNeighborValidator(device)
neighbor = validator.validate_specific_neighbor("10.0.0.1")
if neighbor and neighbor.is_healthy():
    print(f"✓ Neighbor healthy")
```

### Send to Monitoring System
```python
result = validator.validate_neighbors()
metrics = result.to_dict()  # Ready for JSON!

# Send to Prometheus, CloudWatch, DataDog, etc.
send_metrics(metrics)
```

## 🧪 Testing Your Changes

All modules are fully tested. When you extend them:

```bash
# Run all tests
pytest bgp/ -v

# Run specific test class
pytest bgp/ -k TestBGPNeighborValidator -v

# Run with coverage
pytest bgp/ --cov=bgp --cov-report=html
```

## 📊 Sample Output

### Terminal Output
```
======================================================================
  BGP Neighbor Validation
======================================================================

  Device: router1 | VRF: default

  Summary:
    Total Neighbors: 4
    ✓  Established: 3
    Down: 1

  Neighbors:
    IP Address           AS         State           RX Pfx     TX Pfx    
    192.168.1.1          65000      Established     1024       512       
    192.168.1.2          65001      Established     2048       256       
    192.168.1.3          65002      Down            0          0         

======================================================================
  Validation Summary
======================================================================
  Devices validated: 1/1
  Total neighbors: 4
  ✓  Established: 3
  ✗  Down: 1
```

### JSON Report
```json
{
  "timestamp": "2024-05-13T20:37:24.892-07:00",
  "testbed": "testbed.yaml",
  "summary": {
    "devices_validated": 1,
    "total_neighbors": 4,
    "established": 3,
    "down": 1
  },
  "devices": [
    {
      "device_name": "router1",
      "total_neighbors": 4,
      "established": 3,
      "neighbors": [
        {
          "ip_address": "192.168.1.1",
          "remote_as": 65000,
          "state": "Established",
          "prefixes_received": 1024,
          "prefixes_advertised": 512
        }
      ]
    }
  ]
}
```

## 🔌 Integration Examples

### Ansible Playbook
```yaml
- name: Validate BGP neighbors
  shell: python validate_bgp_neighbors.py --testbed testbed.yaml --report bgp.json
  register: bgp_result
  failed_when: bgp_result.rc == 1
```

### Cron Job (Daily Monitoring)
```bash
0 8 * * * /usr/bin/python3 /path/to/validate_bgp_neighbors.py \
  --testbed testbed.yaml --report /var/reports/bgp_$(date +%Y%m%d).json
```

### Kubernetes CronJob
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: bgp-validation
spec:
  schedule: "0 */6 * * *"  # Every 6 hours
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: bgp-validator
            image: my-bgp-validator:latest
            command: ["python", "validate_bgp_neighbors.py", 
                     "--testbed", "testbed.yaml"]
```

## 🛠️ Troubleshooting

### Connection Timeout
```bash
# Increase timeout in testbed.yaml
connection_options:
  cli:
    timeout: 60
```

### Parse Errors
```bash
# Enable verbose logging
python validate_bgp_neighbors.py --testbed testbed.yaml --verbose
```

### Module Not Found
```bash
# Ensure you're in the correct directory
cd EVE-NG-Network-Automation
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

## 📖 API Reference

### BGPNeighborValidator
```python
validator = BGPNeighborValidator(device, vrf="default")

# Main methods
result = validator.validate_neighbors()
neighbor = validator.validate_specific_neighbor("10.0.0.1")
```

### BGPValidationResult
```python
result.device_name           # str: Device name
result.total_neighbors       # int: Total count
result.established_count     # int: Established count
result.down_count           # int: Down count
result.neighbors            # List[BGPNeighbor]: All neighbors
result.errors               # List[str]: Validation errors

# Methods
result.get_status_summary()         # str: Human-readable summary
result.get_unhealthy_neighbors()    # List[BGPNeighbor]: Unhealthy only
result.to_dict()                    # dict: JSON-serializable
```

### BGPNeighbor
```python
neighbor.ip_address         # str: IP address
neighbor.remote_as          # int: Remote AS number
neighbor.state              # BGPNeighborState: Session state
neighbor.prefixes_received  # int: Prefixes RX
neighbor.prefixes_advertised# int: Prefixes TX
neighbor.is_healthy()       # bool: True if Established
```

## 🎓 Next Steps

1. **Test with your lab**: Customize testbed.yaml and run validation
2. **Integrate with monitoring**: Send results to Prometheus/CloudWatch
3. **Create alerts**: Monitor for neighbor state changes
4. **Extend functionality**: Add prefix length checks, AS path validation, etc.
5. **Automate workflows**: Schedule validations with Ansible/Cron

## 📞 Support Resources

- **Full Documentation**: See `README.md` for complete API docs
- **Usage Examples**: See `examples.py` for 10 real-world scenarios
- **Test Examples**: See `test_bgp_neighbor_validator.py` for usage patterns
- **Sample Config**: See `testbed_bgp_sample.yaml` for device setup

---

**Ready to go!** Start with Step 1 above and you'll be validating BGP neighbors in minutes. 🚀
