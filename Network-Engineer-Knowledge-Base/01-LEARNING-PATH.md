# Network Engineering Learning Path

## Phase 1: Core networking

Study in this order:

1. IPv4 addresses, CIDR, subnet boundaries, usable hosts, `/31`, and `/32`.
2. Ethernet, MAC addresses, ARP, VLANs, trunks, and access ports.
3. Interface state: administrative state, operational state, speed, duplex,
   errors, drops, and MTU.
4. TCP, UDP, ICMP, DNS, HTTP, and TLS.
5. Static routing, default routes, longest-prefix match, and administrative
   distance.

Useful repository material includes the `ipaddress` exercises, TCP/UDP/DNS
notebooks, Wireshark notebooks, packet captures, VLAN utilities, and interface
CSV parsing examples.

## Phase 2: Routing and switching labs

1. Build a three-router EVE-NG topology.
2. Establish management connectivity and SSH.
3. Configure loopbacks and point-to-point transit networks.
4. Configure and verify OSPF area 0.
5. Configure eBGP between separate autonomous systems.
6. Compare eBGP, iBGP, and route-reflector behavior.
7. Introduce controlled failures: interface shutdown, area mismatch, AS
   mismatch, and prefix filtering.

Primary projects:

- `1.Python Learning/Network Coding/EVE-NG_3_Router_Automation`
- `EVE-NG-Network-Automation/bgp`
- `EVE-NG-Network-Automation/14-MAY-Configure-lldp,OSPF`
- `EVE-NG-Network-Automation/vlan`

## Phase 3: Python for network engineers

Focus on:

- `ipaddress` for subnet validation.
- `pathlib`, CSV, JSON, and YAML for inventories and reports.
- Functions, dataclasses, enums, exceptions, logging, and context managers.
- Type hints and small testable functions.
- Environment variables for credentials.
- Timestamped structured output for auditability.

Avoid making notebooks the only executable form. Move stable logic into `.py`
modules, keep notebooks for demonstrations, and add tests around the modules.

## Phase 4: Automation frameworks

Learn the tools by responsibility:

| Tool | Best use |
|---|---|
| Netmiko | Simple SSH command execution and configuration |
| pyATS | Testbeds, connections, reusable test workflows |
| Genie | Structured parsing and operational-state models |
| Ansible | Declarative multi-device orchestration |
| pytest | Fast unit and read-only validation tests |
| EVE-NG | Repeatable virtual network laboratories |

Use the workflow `precheck -> plan -> backup -> apply -> verify -> save`.

## Phase 5: Troubleshooting and observability

Practice evidence collection before diagnosis:

1. Confirm scope and recent changes.
2. Check reachability and management access.
3. Check physical/interface state.
4. Check Layer 2 adjacency and VLAN state.
5. Check IP addressing, ARP, and routes.
6. Check protocol neighbors and learned prefixes.
7. Check end-to-end traffic with ping/traceroute.
8. Capture packets only when command output is insufficient.
9. Save raw evidence and a timestamped summary.

## Phase 6: Production readiness

Before calling a project production-ready, require:

- No embedded credentials.
- Dry-run or plan mode.
- Explicit confirmation for configuration changes.
- Timeouts and bounded retries.
- Per-device error reporting.
- Idempotent behavior where possible.
- Backups and rollback instructions.
- Unit tests plus read-only integration checks.
- Structured logs and machine-readable reports.
- Documentation for assumptions and supported platforms.
