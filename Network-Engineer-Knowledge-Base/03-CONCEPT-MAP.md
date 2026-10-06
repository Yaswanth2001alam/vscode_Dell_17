# Network Engineering Concept Map

## Addressing and data modeling

**Questions to answer**

- Is the address valid?
- What are the network, broadcast, first host, and last host?
- Does the interface belong to the intended subnet?
- Are inventory fields complete and correctly typed?

**Repository techniques**

- Python `ipaddress`
- CSV/JSON/YAML parsing
- Inventory schema validation
- pyATS testbed files

## Interfaces and Layer 2

**Operational checks**

- Administrative and operational state
- Line protocol, errors, discards, speed, duplex, MTU
- VLAN membership and trunk state
- CDP/LLDP neighbors
- ARP/MAC learning

**Automation lesson**

Do not treat `status=up` alone as health. Combine status, protocol, errors,
neighbor evidence, addressing, and expected topology.

## OSPF

**Core concepts**

- Router ID, area, network type, hello/dead timers
- Neighbor states and FULL adjacency
- Passive interfaces
- DR/BDR behavior
- LSDB and route installation

**Repository lab**

The three-router project uses point-to-point OSPF network type on transit links
to avoid unnecessary DR/BDR election in two-router segments.

## BGP

**Core concepts**

- Local and remote AS
- eBGP versus iBGP
- Session state machine
- Prefix advertisement and receipt
- Next hop, best-path selection, filtering, and route reflectors
- Per-VRF neighbor state

**Repository implementation**

The BGP validator models neighbor state, parses Genie output, counts healthy and
unhealthy peers, and exports structured results. Extend it by validating
expected peers and expected prefix thresholds, not only session state.

## Automation architecture

```text
Inventory -> Precheck -> Plan -> Backup -> Apply -> Verify -> Report -> Save
```

- **Inventory:** expected devices, roles, platforms, addresses, and variables.
- **Precheck:** management reachability and dependency availability.
- **Plan:** exact commands and target scope, with no side effects.
- **Backup:** running/startup configuration and current state.
- **Apply:** explicit, limited, logged change.
- **Verify:** state-based success criteria, not command-send success.
- **Report:** timestamp, device, command, output, error, and result.
- **Save:** persist configuration only after successful verification.

## Testing pyramid

1. Unit-test pure helpers: subnetting, parsing, validation, command generation.
2. Mock device objects for parser and failure-path tests.
3. Run read-only tests against an EVE-NG lab.
4. Run configuration tests only in a disposable lab with backups.
5. Use production checks only after authorization and with a rollback plan.

## Packet analysis

Use packet captures to answer a specific unresolved question:

- Is DNS returning the expected address?
- Is the TCP three-way handshake completing?
- Is TLS negotiation failing?
- Are retransmissions or resets present?
- Is ICMP blocked or is routing broken?

Start with display filters and metadata. Avoid collecting payloads or unrelated
traffic. Packet captures are sensitive operational evidence.

## AI-assisted networking

AI should summarize evidence, not replace evidence collection. A safe pattern
is:

1. Collect approved read-only device output.
2. Parse and save structured context.
3. Remove credentials and unnecessary sensitive fields.
4. Ground the model in that context.
5. Require citations to device/source fields in the answer.
6. Have an engineer validate any recommended change.
