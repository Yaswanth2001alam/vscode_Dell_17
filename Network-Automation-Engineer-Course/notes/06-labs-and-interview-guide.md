# 6. Labs, Projects, and Interview Guide

## 6.1 Suggested lab platforms

- EVE-NG, GNS3, or Cisco CML for traditional virtual appliances.
- containerlab for containerized network operating systems.
- Vendor sandboxes for supported API exercises.
- Linux network namespaces, FRRouting, and Open vSwitch for open labs.

Only use images for which you have a valid license. Keep the management network
isolated from production, and take snapshots/checkpoints.

## 6.2 Progressive lab topology

Build one topology that grows:

```text
HostA--Access1====Access2--HostB
          |          |
        Edge1------Edge2
          \          /
           P1------P2
```

- Access layer: VLAN, trunk, RSTP/MST, LACP, LLDP, optional MACsec.
- Underlay: OSPF or IS-IS with BFD.
- Service-provider extension: MPLS/LDP or RSVP-TE.
- Edge: eBGP and iBGP route reflection.
- Data-center extension: VXLAN EVPN if supported.
- Management: SSH, NETCONF, RESTCONF, telemetry, syslog, NTP.

## 6.3 Labs

### Lab 1: packet walk

Capture DHCP, DNS, ARP/ND, TCP handshake, TLS setup, and application response.
Annotate source/destination addresses, MAC changes at each routed hop, ports,
flags, timing, and failure signals.

### Lab 2: Python inventory

Load a sanitized YAML inventory, validate required fields and IPs, detect
duplicate management addresses and unknown peers, and emit normalized JSON.
Add unit tests for every invalid case.

### Lab 3: concurrent read-only collection

Use Netmiko or Scrapli to collect identity, interfaces, LLDP, and routing.
Bound concurrency, use explicit timeouts, classify errors, and save per-device
JSON. A single failure must not stop other devices or appear healthy.

### Lab 4: L2 intent validation

Describe VLAN, trunk, LAG, LLDP neighbor, STP root, and protection intent.
Compare normalized observations with intent. Inject wrong VLAN, missing member,
unexpected LLDP peer, and superior-root attempt.

### Lab 5: IGP validation

Build OSPF, then repeat with IS-IS. Validate exact neighbors, LSDB/topology,
routes, next hops, and pings. Inject timer/authentication/MTU/level mismatch and
measure convergence with and without BFD.

### Lab 6: BGP policy

Create eBGP edges and iBGP route reflection. Originate test prefixes. Enforce
prefix filters, local preference, communities, maximum-prefix, and default
policy. Prove required routes and absence of forbidden routes.

### Lab 7: NETCONF candidate change

Read capabilities, lock candidate, edit a loopback/description, validate, issue
a confirmed commit, run operational checks, confirm, and unlock. Repeat with a
failed post-check and prove automatic rollback.

### Lab 8: RESTCONF workflow

GET a YANG interface resource, use ETag if available, PATCH a safe field, check
status/body, GET it again, and restore. Test invalid authentication, content
type, schema field, and stale ETag.

### Lab 9: security

Enable MACsec or IPsec in an isolated lab. Verify encrypted counters, wrong-key
failure, rekey, replay/integrity counters, and effective MTU. Confirm that logs
and reports contain no key material.

### Lab 10: CI and virtual integration

On every pull request, run lint/type/unit/schema tests and render candidate
configuration. On an approved branch, deploy a disposable lab and execute
integration tests. Store sanitized test artifacts.

## 6.4 Portfolio projects

### Project A: network pre-check engine

Input: inventory and change scope. Output: HTML/JSON report of device identity,
redundancy, interfaces, neighbors, route health, CPU/memory, NTP, and backup.
Include plugin-style checks, tests, and explicit error categories.

### Project B: source-of-truth reconciler

Compare intended devices/interfaces/IPs/VLANs/neighbors with observed state.
Produce a drift plan; do not change devices by default. Add an approved,
bounded remediation mode with post-check and rollback.

### Project C: BGP policy verifier

Validate sessions, prefix limits, required/forbidden routes, next hops,
attributes, communities, RPKI state, and data-plane probes. Include withdrawal,
route-reflector failure, and malformed parser fixture tests.

### Project D: telemetry service

Subscribe to interface and BGP state, normalize paths, store time-series data,
expose health through an API, and alert with deduplication. Handle reconnect,
stale data, deletes, and out-of-order timestamps.

## 6.5 Interview questions with answer points

### Why is ping insufficient?

ICMP may be filtered or handled differently. Ping does not prove DNS, TCP/UDP
port reachability, application behavior, path symmetry, MTU, or policy. Combine
route/neighbor state, transport/application checks, counters, and captures.

### Netmiko versus Paramiko?

Paramiko is a general SSH implementation. Netmiko adds network-device prompt,
privilege, paging, and configuration handling. Use Paramiko for low-level SSH
needs; Netmiko/Scrapli for interactive network CLI.

### NETCONF versus RESTCONF?

Both expose YANG-modeled data. NETCONF uses XML RPCs and supports datastore
operations such as lock/candidate/confirmed commit where advertised. RESTCONF
maps data to HTTP resources and representations. Capabilities and platform
support decide; neither is automatically safer without validation and rollback.

### What is idempotency?

Applying the same desired intent repeatedly has no additional harmful effect
and converges to the same state. CLI command repetition alone is not proof;
check semantic state and device behavior.

### How do you prevent blast radius?

Validate inventory and exact selection, default to dry-run, require review,
backup/checkpoint, canary first, batch with low concurrency, define stop
conditions, independently verify service, and test rollback.

### Why separate collection, parsing, and validation?

It enables offline tests, reuse across transports, clear error classification,
and changes in device output without rewriting policy.

### OSPF stuck in ExStart/Exchange?

Check MTU mismatch first, then duplicate router IDs, master/slave negotiation,
network type, loss, and software issues. Use logs/capture and interface details.

### BGP Active state?

The peer is retrying TCP establishment. Check routes to peer/source, source
address/update-source, TCP 179 ACL/firewall, local/remote AS only after OPEN,
multihop/TTL, and peer configuration. An MD5 mismatch may also prevent progress.

### LACP bundle member suspended?

Compare LACP mode, system/port IDs, key, speed/duplex, bundle settings, VLAN
mode/list, MTU, and minimum-links. Inspect actor/partner flags rather than only
the port-channel summary.

### STP root unexpectedly changed?

Find the superior BPDU source and path, compare priority/MAC, validate intended
root configuration, and check Root Guard/BPDU Guard. Do not simply force a
priority without understanding the unexpected bridge.

### How do you test a parser?

Pure function, sanitized fixtures from supported releases, success and malformed
outputs, missing/empty fields, device error text, IPv4/IPv6, and explicit
failure when the contract cannot be met.

## 6.6 Completion checklist

You are ready for junior-to-mid network automation responsibilities when you
can independently:

- subnet and troubleshoot IPv4/IPv6 packet paths;
- explain and validate the major L2, IGP, BGP, MPLS, and security protocols;
- write typed, tested Python with clear errors and logs;
- use Git and review diffs;
- safely collect from dozens of devices with bounded concurrency;
- use at least CLI and one model-driven interface;
- design tests around intent and negative cases;
- produce a dry-run, backup, canary, post-check, rollback, and evidence;
- protect secrets and verify SSH/TLS identity;
- demonstrate two end-to-end projects with tests and documentation.

Mastery is not memorizing every command. It is building a correct mental model,
collecting decisive evidence, and making repeatable low-risk changes.

