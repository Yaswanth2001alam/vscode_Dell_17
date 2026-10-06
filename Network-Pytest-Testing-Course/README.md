# Network Testing with pytest

This is a separate, self-contained course and reference suite for testing
networks with `pytest`. It does not depend on or modify the existing network
automation course.

The goal is not to claim that one suite can test every network. The goal is to
provide a comprehensive framework covering the test categories a network
engineer can automate, with clear safety boundaries and reusable examples.

## Safety model

The default command runs **offline tests only**:

```powershell
Set-Location "Network-Pytest-Testing-Course"
python -m pytest
```

Live and disruptive tests never run by default:

```powershell
# Read-only live checks against one explicitly supplied lab target
$env:NETWORK_TEST_TARGET = "192.0.2.10"
python -m pytest -m live --run-live

# Disruptive tests require both opt-in flags and must only target an isolated lab
python -m pytest -m disruptive --run-live --run-disruptive
```

No included test changes a device. The disruptive marker and empty template are
provided to demonstrate gating; you must implement platform-specific setup,
rollback, and recovery validation before adding a disruptive action.

## What can be tested

| Domain | Examples |
|---|---|
| Inventory | schema, required fields, duplicate IPs, peer references, roles |
| Layer 1 | link, speed, duplex, optics, signal, FEC, CRC/error rate |
| Layer 2 | VLAN, trunk, MAC, LLDP, LACP, STP, 802.1X, MACsec |
| Layer 3 | IPv4/6, ARP/ND, routes, OSPF, IS-IS, BGP, multicast, FHRP |
| MPLS/overlay | labels, LDP, RSVP-TE, VRF, VXLAN, EVPN |
| Layer 4 | TCP handshake, UDP response, ports, loss, latency, jitter |
| Services | DNS, DHCP, NTP, HTTP, TLS, SSH, SNMP, syslog, AAA |
| Model-driven | NETCONF, RESTCONF, gNMI, YANG/OpenConfig |
| Security | ACL, prefix policy, algorithms, certificates, authorization |
| Operations | backup, drift, idempotency, rollback, convergence, evidence |
| Quality | parser contracts, mocks, schemas, templates, reports, timeouts |
| Scale/performance | route/session scale, API latency, concurrency, soak tests |

See [TEST-CATALOG.md](TEST-CATALOG.md) for the complete test-case inventory.

## Project structure

```text
Network-Pytest-Testing-Course/
|-- README.md
|-- TEST-CATALOG.md
|-- pytest.ini
|-- requirements.txt
|-- network_pytest/
|   |-- __init__.py
|   |-- checks.py
|   `-- probes.py
`-- tests/
    |-- conftest.py
    |-- test_bgp.py
    |-- test_configuration_security.py
    |-- test_http.py
    |-- test_interfaces.py
    |-- test_inventory.py
    |-- test_isis.py
    |-- test_lacp.py
    |-- test_lldp.py
    |-- test_live_templates.py
    |-- test_macsec.py
    |-- test_ntp.py
    |-- test_ospf.py
    |-- test_reachability.py
    |-- test_route_policy.py
    |-- test_stp.py
    |-- test_tls.py
    `-- test_vlan.py
```

Tests are intentionally split into dedicated protocol or domain modules rather
than collected in one large test file. Parameterized cases for one protocol
remain together so shared fixtures, markers, and boundary values are readable.

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The example suite uses pure functions and sanitized fixtures. Real projects can
add Netmiko, Scrapli, Nornir, pyATS/Genie, NAPALM, ncclient, requests, gNMI,
Scapy, or vendor SDK collectors. Keep collection separate from assertions.

## pytest concepts demonstrated

- fixtures and fixture composition;
- parameterization and boundary values;
- custom command-line options;
- registered markers and marker selection;
- default skip gates for live/disruptive work;
- exception testing with `pytest.raises`;
- temporary paths;
- monkeypatching environment and sockets;
- deterministic pure-function tests;
- readable assertion IDs;
- offline contract fixtures;
- test grouping by protocol/domain.

## Recommended test architecture

```text
collector (SSH/API/telemetry/capture)
 -> raw evidence
 -> parser/normalizer
 -> typed observation
 -> pure policy check
 -> pytest assertion
 -> JSON/JUnit/HTML evidence
```

Do not place connections and complex parsing directly inside every test. Use
session-scoped collection only when data can safely be shared, and preserve
per-test clarity.

## Useful commands

```powershell
# Entire safe offline suite
python -m pytest

# Show test names and skip reasons
python -m pytest -vv -rs

# Only Layer 2 checks
python -m pytest -m layer2

# Routing but not BGP
python -m pytest -m "routing and not bgp"

# Stop after first failure
python -m pytest -x

# Run the last failures first
python -m pytest --ff

# JUnit report for CI
python -m pytest --junitxml=outputs\pytest-junit.xml

# Coverage after installing pytest-cov
python -m pytest --cov=network_pytest --cov-report=term-missing
```

## Test outcome meanings

- **PASS:** collected state satisfies explicit intent.
- **FAIL:** collection succeeded, but observed state violates intent.
- **ERROR:** setup, connection, parsing, fixture, or test code failed.
- **SKIP:** deliberately not run, with a recorded reason.
- **XFAIL:** a known, documented defect; do not use it to hide instability.

An empty neighbor or route table must not automatically pass. Decide whether
empty is expected, a failure, or a collection/parser error.

## Moving from fixtures to devices

1. Build and test a collector separately.
2. Save sanitized real outputs as contract fixtures.
3. Normalize vendor-specific data into stable records.
4. Reuse the pure checks in this course.
5. Add a `live` test that explicitly selects lab devices.
6. Add timeouts and per-device error reporting.
7. Require an additional gate for configuration or failure injection.
8. Save evidence with time, device identity, code revision, expected, observed,
   result, and error.
