# Network Automation Engineer Course

This is a practical, vendor-neutral course for becoming a network automation
engineer. It combines networking theory, Python, APIs, source control,
configuration generation, validation, testing, observability, security, and
production change practices.

The examples are safe to run offline unless a section is explicitly marked
**LIVE LAB**. Live examples read credentials from environment variables; never
put passwords, tokens, private keys, or production addresses in source code.

## What you will be able to do

After completing the course, you should be able to:

1. Explain packet forwarding from an application through L2, L3, transport,
   routing, MPLS, and security layers.
2. Read captures and operational state for Ethernet, LLDP, LACP, STP, MACsec,
   OSPF, IS-IS, BGP, RSVP, MPLS, VXLAN EVPN, IPv4, and IPv6.
3. Write maintainable Python using types, data classes, exceptions, logging,
   tests, packages, virtual environments, and concurrency.
4. Automate CLI devices with Netmiko, Paramiko, Scrapli, Nornir, and pyATS.
5. Automate model-driven devices with NETCONF, RESTCONF, YANG, gNMI, and
   OpenConfig.
6. Render and validate configuration with Jinja2, YAML, JSON, Pydantic,
   TextFSM/TTP, Genie, and NAPALM.
7. Build pre-check, change, post-check, rollback, and evidence workflows.
8. Test code offline, test a virtual lab, and safely qualify changes before
   production.
9. Use Git, CI, secret management, least privilege, structured logs, metrics,
   and change review.
10. Design portfolio projects that demonstrate engineering rather than one-off
    scripts.

## Recommended prerequisites

- Basic routing and switching knowledge at roughly CCNA/JNCIA level.
- A computer with Python 3.11 or newer, Git, VS Code, and 8 GB RAM.
- Optional EVE-NG, GNS3, Cisco CML, containerlab, or vendor virtual routers.
- Never connect course code to production until it has passed offline and lab
  testing and has an approved change and rollback plan.

## Course map (24 weeks)

Use a slower pace if you are new to networking or programming. Each week should
include reading, packet analysis, coding, testing, and a short written summary.

| Phase | Weeks | Topics | Deliverable |
|---|---:|---|---|
| Foundations | 1-2 | OSI/TCP-IP, Ethernet, IPv4/6, subnetting, ARP/ND, TCP/UDP, DNS/DHCP/NTP | Packet-walk document and Wireshark captures |
| Python | 3-5 | Types, collections, functions, files, exceptions, OOP, typing, logging, packages, concurrency | Inventory/reporting CLI with unit tests |
| L2 campus | 6-7 | VLANs, trunks, STP/RSTP/MST, LLDP, LACP, MACsec, first-hop redundancy | Campus health validator |
| IGP/MPLS | 8-10 | Static routes, OSPF, IS-IS, MPLS, LDP, RSVP-TE, BFD | IGP adjacency and path test suite |
| BGP/DC | 11-13 | BGP policy, MP-BGP, route reflection, communities, EVPN/VXLAN | BGP/EVPN intent validator |
| Interfaces | 14-16 | SSH, Netmiko, Paramiko, Scrapli, Nornir, Ansible | Concurrent backup and audit tool |
| Model-driven | 17-19 | YANG, NETCONF, RESTCONF, gNMI, OpenConfig, telemetry | API-based interface workflow |
| Quality | 20-21 | pytest, mocks, parsers, pyATS/Genie, NAPALM, Batfish concepts, CI | Offline + integration test pipeline |
| Production | 22-23 | Git, security, secrets, observability, idempotency, rollback, SRE | Controlled change runbook |
| Capstone | 24 | Source of truth to deployed and verified intent | Demonstrable end-to-end project |

## Repository layout

```text
Network-Automation-Engineer-Course/
|-- README.md
|-- requirements.txt
|-- requirements-lab.txt
|-- inventory.example.yaml
|-- protocols/
|   |-- README.md
|   `-- layer-1/ ... layer-7/
|-- notes/
|   |-- 01-network-foundations.md
|   |-- 02-protocol-handbook.md
|   |-- 03-python-and-data.md
|   |-- 04-automation-libraries.md
|   |-- 05-testing-and-operations.md
|   |-- 06-labs-and-interview-guide.md
|   `-- 07-osi-layers-and-protocols.md
|-- network_course/
|   |-- __init__.py
|   |-- layer_diagnostics.py
|   |-- models.py
|   |-- protocol_catalog.py
|   |-- validators.py
|   `-- protocol_checks.py
|-- examples/
|   |-- cli_netmiko.py
|   |-- ssh_paramiko.py
|   |-- nornir_runner.py
|   |-- netconf_ncclient.py
|   `-- restconf_requests.py
|-- tools/
|   `-- generate_protocol_notes.py
`-- tests/
    |-- test_layers.py
    |-- test_models.py
    `-- test_validators.py
```

## Reading guide

1. [Network foundations](notes/01-network-foundations.md)
2. [Protocol handbook](notes/02-protocol-handbook.md)
3. [Python and data engineering](notes/03-python-and-data.md)
4. [Automation libraries and interfaces](notes/04-automation-libraries.md)
5. [Testing, security, and production operations](notes/05-testing-and-operations.md)
6. [Labs, projects, and interview guide](notes/06-labs-and-interview-guide.md)
7. [OSI Layers 1-7 protocols, automation, and tests](notes/07-osi-layers-and-protocols.md)
8. [Individual files for every protocol](protocols/README.md)

Read the chapters in order on the first pass. Later, use the protocol and
library chapters as field references.

The individual protocol files are generated from the typed protocol catalog.
Regenerate them after catalog or template changes:

```powershell
python -m tools.generate_protocol_notes
```

## Complete course file index

### Course chapters

1. [Network foundations](notes/01-network-foundations.md)
2. [Protocol handbook](notes/02-protocol-handbook.md)
3. [Python and data engineering](notes/03-python-and-data.md)
4. [Automation libraries and interfaces](notes/04-automation-libraries.md)
5. [Testing, security, and production operations](notes/05-testing-and-operations.md)
6. [Labs, projects, and interview guide](notes/06-labs-and-interview-guide.md)
7. [OSI Layers 1-7 protocols, automation, and tests](notes/07-osi-layers-and-protocols.md)
8. [Generated individual protocol index](protocols/README.md)

### Layer 1 - Physical protocols

1. [Ethernet PHY](protocols/layer-1/ethernet-phy.md)
2. [Wi-Fi PHY](protocols/layer-1/wi-fi-phy.md)

### Layer 2 - Data Link protocols

1. [Ethernet](protocols/layer-2/ethernet.md)
2. [802.1Q VLAN](protocols/layer-2/802-1q.md)
3. [STP, RSTP, and MST](protocols/layer-2/stp-rstp-mst.md)
4. [LACP](protocols/layer-2/lacp.md)
5. [LLDP](protocols/layer-2/lldp.md)
6. [802.1X and EAPOL](protocols/layer-2/802-1x-eapol.md)
7. [MACsec and MKA](protocols/layer-2/macsec-mka.md)
8. [ARP](protocols/layer-2/arp.md)
9. [MPLS](protocols/layer-2/mpls.md)
10. [IS-IS](protocols/layer-2/is-is.md)

### Layer 3 - Network protocols

1. [IPv4](protocols/layer-3/ipv4.md)
2. [IPv6](protocols/layer-3/ipv6.md)
3. [ICMP and ICMPv6](protocols/layer-3/icmp-icmpv6.md)
4. [OSPF](protocols/layer-3/ospf.md)
5. [BGP](protocols/layer-3/bgp.md)
6. [PIM](protocols/layer-3/pim.md)
7. [VRRP](protocols/layer-3/vrrp.md)
8. [GRE](protocols/layer-3/gre.md)
9. [IPsec ESP](protocols/layer-3/ipsec-esp.md)

### Layer 4 - Transport protocols

1. [TCP](protocols/layer-4/tcp.md)
2. [UDP](protocols/layer-4/udp.md)
3. [SCTP](protocols/layer-4/sctp.md)
4. [QUIC](protocols/layer-4/quic.md)

### Layer 5 - Session protocols

1. [RPC](protocols/layer-5/rpc.md)
2. [SIP](protocols/layer-5/sip.md)
3. [TLS](protocols/layer-5/tls.md)

### Layer 6 - Presentation protocols and formats

1. [ASN.1](protocols/layer-6/asn-1.md)
2. [JSON, XML, and Protobuf](protocols/layer-6/json-xml-protobuf.md)

### Layer 7 - Application protocols

1. [DNS](protocols/layer-7/dns.md)
2. [DHCPv4](protocols/layer-7/dhcpv4.md)
3. [HTTP and HTTPS](protocols/layer-7/http-https.md)
4. [SSH](protocols/layer-7/ssh.md)
5. [NETCONF](protocols/layer-7/netconf.md)
6. [RESTCONF](protocols/layer-7/restconf.md)
7. [gNMI](protocols/layer-7/gnmi.md)
8. [SNMP](protocols/layer-7/snmp.md)
9. [NTP](protocols/layer-7/ntp.md)
10. [Syslog](protocols/layer-7/syslog.md)
11. [RADIUS](protocols/layer-7/radius.md)
12. [TACACS+](protocols/layer-7/tacacs.md)
13. [SMTP](protocols/layer-7/smtp.md)
14. [FTP, TFTP, and SFTP](protocols/layer-7/ftp-tftp-sftp.md)

Cross-layer protocols are stored under their lowest or primary OSI layer. Each
individual file lists every layer relevant to that protocol.

### Core Python modules

- [Package exports](network_course/__init__.py)
- [Inventory and result models](network_course/models.py)
- [Reusable protocol validators](network_course/validators.py)
- [Offline protocol check demonstration](network_course/protocol_checks.py)
- [Typed protocol catalog](network_course/protocol_catalog.py)
- [DNS, TCP, TLS, and HTTPS diagnostics](network_course/layer_diagnostics.py)

### Automation library examples

- [Netmiko CLI collection and gated configuration](examples/cli_netmiko.py)
- [Paramiko SSH command execution](examples/ssh_paramiko.py)
- [Nornir orchestration and result handling](examples/nornir_runner.py)
- [NETCONF candidate and confirmed-commit workflow](examples/netconf_ncclient.py)
- [RESTCONF GET and gated PATCH workflow](examples/restconf_requests.py)

### Inventory, dependencies, and generation

- [Sanitized example inventory](inventory.example.yaml)
- [Core Python requirements](requirements.txt)
- [Extended lab requirements](requirements-lab.txt)
- [Individual protocol-note generator](tools/generate_protocol_notes.py)

### Unit tests

- [Inventory and result model tests](tests/test_models.py)
- [Protocol validator tests](tests/test_validators.py)
- [Layer catalog and diagnostic tests](tests/test_layers.py)
- [Protocol-note generator tests](tests/test_protocol_note_generator.py)

## Setup

The core examples and tests use only the Python standard library. This keeps
the first run deterministic:

```powershell
Set-Location "Network-Automation-Engineer-Course"
python -m unittest discover -s tests -v
python -m network_course.protocol_checks
```

Run a safe, bounded live diagnostic against one hostname you are authorized to
test:

```powershell
python -m network_course.layer_diagnostics example.com --port 443 --path /
```

This checks DNS (Layer 7), TCP (Layer 4), TLS (Layers 5-6), and HTTPS (Layer 7).
Physical, switching, and routing state must be collected from authorized network
devices using the library examples and validated using the included contracts.

Create an isolated environment before installing automation libraries:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install the larger lab stack only when you need pyATS/Nornir/NAPALM:

```powershell
pip install -r requirements-lab.txt
```

Versions are constrained by major release so future security and bug-fix
versions can be selected by pip. In a production repository, resolve and lock
exact versions with an approved dependency process.

## How to study each protocol

For every protocol, answer these questions:

1. **Problem:** What failure or scaling problem does it solve?
2. **Scope:** Is it link-local, an IGP domain, an AS, or end-to-end?
3. **Peers:** How are neighbors discovered and authenticated?
4. **State machine:** What states lead to operational readiness?
5. **Messages:** Which packet or PDU types are exchanged?
6. **Selection:** How is the winning link, path, root, or route selected?
7. **Timers:** Which timers affect detection and convergence?
8. **Tables:** Which control-plane and forwarding tables should agree?
9. **Failure:** What happens on a link, node, or policy failure?
10. **Evidence:** Which show commands, packet fields, logs, and telemetry prove
    correctness?
11. **Automation:** What structured fields form a stable test contract?
12. **Security:** How can the protocol be authenticated, filtered, or abused?

Do not automate only a command string. Automate an **intent** and validate the
resulting operational state.

## Standard change workflow

Every lab and real change should follow this sequence:

```text
intent -> inventory validation -> generated plan -> peer review
       -> pre-checks -> backup/checkpoint -> bounded change
       -> post-checks -> traffic/path validation -> save evidence
       -> commit or rollback -> monitor
```

Important properties:

- **Idempotent:** repeating the operation produces no harmful extra change.
- **Observable:** output, errors, timestamps, and device identities are saved.
- **Bounded:** the user selects devices, sites, and change size.
- **Fail-safe:** invalid inventory and failed pre-checks stop the change.
- **Recoverable:** the rollback is prepared and tested first.
- **Auditable:** intent, approval, code revision, and results can be traced.

## Test pyramid for network automation

1. **Static checks:** formatting, lint, typing, schema, secret scanning.
2. **Unit tests:** address math, templates, parsers, policy, expected commands.
3. **Contract tests:** mocked SSH/API payloads, YANG/schema expectations.
4. **Virtual lab integration:** real control-plane neighbors and routes.
5. **Pre-production qualification:** representative images and scale.
6. **Production canary:** one low-risk device/site with stop conditions.
7. **Post-change monitoring:** reachability, adjacency, routes, traffic, errors.

Never make a test pass by catching every exception or returning an empty result.
A connection failure, parser failure, missing field, and unhealthy protocol are
different outcomes and must be reported differently.

## Capstone: intent-driven branch deployment

Build a system with the following inputs and outputs:

**Inputs**

- YAML inventory: sites, roles, platforms, management endpoints.
- Intended links: local/remote ports, addresses, MTU, LAG, VLANs.
- Intended routing: OSPF/IS-IS area or level, BGP AS and neighbors.
- Policy: accepted prefixes, communities, maximum-prefix, security controls.

**Pipeline**

1. Validate the data model and all IP/prefix relationships.
2. Generate candidate configuration and a human-readable plan.
3. Run offline unit tests and policy checks in CI.
4. Collect pre-change state and configuration backups.
5. Deploy to a virtual lab; verify adjacency, routes, paths, and negative cases.
6. Require approval before a canary deployment.
7. Deploy with bounded concurrency and explicit timeouts.
8. Verify intent, save JSON evidence, and rollback on defined stop conditions.

**Acceptance criteria**

- No secrets in the repository or logs.
- Invalid inventory cannot reach a device.
- Every change has a dry-run and exact device list.
- A single failed device does not hide successful or unattempted devices.
- Tests cover success, timeout, authentication error, malformed data, wrong
  neighbor state, excess prefixes, packet loss, and rollback.
- Reports include timestamps, code revision, device, check, expected, observed,
  status, and error.

## Certification and skill directions

Certifications are optional; use them as structured syllabi rather than proof
of practical ability. Relevant tracks include Cisco DevNet/CCNP Enterprise,
Juniper JNCIA/JNCIS automation and routing, Red Hat Ansible, cloud networking,
Linux, and vendor-neutral Python/Git. Always verify current exam objectives on
the vendor's official site because they change.

The strongest portfolio contains readable code, tests, sample data, safe error
handling, diagrams, and a short demonstration of a failure and rollback.
