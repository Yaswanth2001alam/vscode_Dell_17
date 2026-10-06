# 7. OSI Layers 1-7: Protocols, Automation, and Tests

The OSI model is a troubleshooting and design model, not a rule that every
protocol fits exactly one layer. Real protocols often cross layers. TLS is
commonly discussed at Layers 5-6, while implementations expose it above TCP.
MPLS is often called "Layer 2.5." ARP connects Layer 2 and Layer 3. Use the
layer assignment to organize reasoning, not to argue about labels.

## 7.1 Encapsulation and troubleshooting order

```text
L7 application data
 -> L6 encoded/encrypted representation
 -> L5 session/dialog state
 -> L4 TCP segment / UDP datagram / QUIC packet
 -> L3 IPv4/IPv6 packet
 -> L2 Ethernet/Wi-Fi frame
 -> L1 electrical/optical/radio symbols and bits
```

The receiver removes these wrappers in reverse. Every layer depends on the
layers below it. Troubleshoot from Layer 1 upward when the failure is broad,
but follow the specific flow end to end when only one application fails.

| Layer | Unit | Address/identifier | Typical device or function |
|---|---|---|---|
| 7 Application | data/message | URL, FQDN, resource, user | proxy, DNS, API, application |
| 6 Presentation | encoded data | format, cipher, certificate identity | TLS terminator, codec |
| 5 Session | dialog/session | session ID, token, RPC context | gateway, RPC/session service |
| 4 Transport | segment/datagram | TCP/UDP port, QUIC connection ID | stateful firewall, load balancer |
| 3 Network | packet | IPv4/IPv6 prefix and next hop | router, L3 switch |
| 2 Data link | frame | MAC, VLAN, VNI, label | switch, bridge, wireless AP |
| 1 Physical | bits/symbols | port, lane, frequency, wavelength | cable, optic, repeater |

---

# Layer 1 - Physical

## Purpose

Layer 1 transports bits as electrical, optical, or radio signals. It defines
media, connectors, pinouts, wavelengths/frequencies, modulation/encoding,
symbol rate, link speed, lane count, signal levels, and physical timing.
Layer 1 does not understand MAC addresses, IP addresses, or ports.

## Technologies and standards

- Copper Ethernet PHYs: 10/100/1000BASE-T, 2.5/5GBASE-T, 10GBASE-T.
- Fiber Ethernet: 1000BASE-SX/LX, 10GBASE-SR/LR, 40/100/400G variants.
- Pluggable optics: SFP/SFP+/SFP28, QSFP+/QSFP28/QSFP-DD; form factor alone
  does not guarantee speed, wavelength, reach, or platform compatibility.
- Structured cabling, single-mode/multimode fiber, MPO/MTP breakouts.
- Wi-Fi PHY (802.11): channels, width, modulation/coding, MIMO, RSSI/SNR.
- SONET/SDH, DWDM, OTN, DSL, DOCSIS, serial links, and PON.
- Power over Ethernet negotiates/delivers power alongside data.
- Auto-negotiation and, on applicable media, link training/FEC.

## Operational fields

- administrative and operational state;
- configured/negotiated speed, duplex, lanes, and FEC;
- optic vendor/part/serial, wavelength, transmit/receive power, temperature;
- loss of signal, carrier transitions, symbol/code errors;
- CRC/FCS errors (detected at L2 but frequently caused by L1);
- runts, giants, alignment errors, interface resets;
- wireless RSSI, SNR, noise, retries, channel utilization.

Optical thresholds are vendor/optic-specific. Never use one universal dBm
threshold. Compare readings with transceiver DOM alarm thresholds and design
loss budget.

## Common failures

- dirty/damaged fiber, incorrect polarity, excessive loss, bend radius;
- unsupported optic, wrong wavelength/reach, single-mode/multimode mismatch;
- copper pair fault, bad termination, EMI, speed/duplex mismatch;
- breakout/lane/FEC mismatch;
- weak Wi-Fi SNR, interference, channel overlap;
- err-disabled or administratively disabled port;
- unidirectional link that appears up on only one direction.

## Automation and tests

Collect structured transceiver/interface data twice and evaluate rates, not
only totals. Baseline normal levels for each optic type.

1. Verify admin/oper state and negotiated speed against intent.
2. Verify expected optic identity and supported type.
3. Compare optical levels with that optic's thresholds.
4. Send small and near-MTU traffic in both directions.
5. Confirm CRC/symbol/discard counters do not increase.
6. Shut/no-shut only in an approved lab; measure link recovery.
7. Test redundant member loss without taking down the logical service.

Python cannot directly prove cable quality through a normal socket. It consumes
device telemetry or platform commands and applies policy to those observations.

---

# Layer 2 - Data Link

## Purpose and sublayers

Layer 2 transfers frames on a local medium. IEEE separates Logical Link Control
(LLC) and Media Access Control (MAC). Ethernet uses 48-bit MAC addresses and an
FCS to detect corruption. Switches learn source MAC addresses and forward using
the destination MAC within a broadcast domain.

## Core protocols and technologies

### Ethernet (IEEE 802.3)

Frame fields include preamble/SFD on the wire, destination/source MAC, optional
802.1Q tag, EtherType/length, payload/padding, and FCS. Minimum/maximum sizes
depend on whether wire overhead and tags are counted.

### VLAN and 802.1Q

The tag carries PCP (priority), DEI, and 12-bit VLAN ID. Access ports normally
carry one untagged data VLAN. Trunks carry multiple VLANs. Native VLAN handling
must match. QinQ (802.1ad) stacks provider/customer tags.

### STP family

STP (802.1D), RSTP (802.1w), and MST (802.1s) prevent bridging loops. Validate
root identity, cost, roles, states, topology changes, and protections such as
BPDU Guard, Root Guard, Loop Guard, and UDLD.

### Link aggregation

LACP (802.1AX) negotiates bundle membership. Healthy forwarding members are
normally synchronized, collecting, and distributing. Static aggregation lacks
LACP's peer/member mismatch detection.

### Discovery and access

- LLDP (802.1AB) advertises chassis/port/capabilities with TLVs.
- CDP is Cisco proprietary discovery.
- 802.1X controls port access using EAPOL; RADIUS commonly carries AAA.
- MACsec (802.1AE) protects hop-by-hop Ethernet; MKA manages keys.
- Wi-Fi MAC (802.11) handles association, authentication, frames, and roaming.

### Other Layer 2 protocols

- ARP sits between L2/L3 and resolves IPv4 next-hop addresses.
- PPP/PPPoE supports point-to-point framing and negotiation.
- HDLC variants frame serial links.
- Frame Relay and ATM are legacy WAN technologies still useful conceptually.
- EVPN/VXLAN spans L2/L3 overlay functions; VXLAN uses UDP at the underlay.
- MPLS label forwarding is commonly described as Layer 2.5.

## Automation tests

- exact VLAN existence/state and access/trunk/native/allowed policy;
- exact LLDP neighbor system and remote port;
- expected MAC on expected port/VLAN and no unstable moves;
- LACP partner system/key/member flags and minimum-links;
- intended STP root, roles/states, guard policy, topology-change rate;
- 802.1X authorized state and correct assigned VLAN/ACL;
- MACsec secured channels, packet protection, rekey, integrity/replay counters;
- MTU, broadcast containment, unknown-unicast behavior, and failure recovery.

Packet capture display filters:

```text
eth
vlan
arp
stp
lldp
lacp
eapol
```

Raw packet capture usually requires administrator/root privileges and should
only run on authorized interfaces.

---

# Layer 3 - Network

## Purpose

Layer 3 provides logical addressing and packet forwarding across networks.
Routers perform longest-prefix match and select a next hop/interface. Control
plane protocols build reachability; the forwarding plane programs a FIB and
adjacencies.

## Data-plane protocols

### IPv4

Important header fields: version, IHL, DSCP/ECN, total length, identification,
flags/fragment offset, TTL, protocol, checksum, source, destination, options.
Routers decrement TTL and update the header checksum. Fragmentation behavior
depends on DF, MTU, and endpoint/path behavior.

### IPv6

The fixed header includes version, traffic class, flow label, payload length,
next header, hop limit, source, and destination. Extension headers form a
chain. Routers do not fragment ordinary transit packets; endpoints use Path MTU
Discovery and fragmentation headers when necessary.

### ICMP/ICMPv6

Provides diagnostics and essential error signaling: echo, unreachable, time
exceeded, redirect, and packet-too-big. ICMPv6 also supports Neighbor Discovery
and router discovery. Broad ICMP blocking breaks PMTUD and IPv6.

### Neighbor resolution

ARP resolves IPv4 on-link addresses. IPv6 Neighbor Discovery uses ICMPv6
neighbor solicitations/advertisements, router advertisements, duplicate address
detection, and neighbor unreachability detection.

### Tunnels

GRE, IP-in-IP, IPsec tunnel mode, and other overlays encapsulate packets.
Account for overhead, MTU, recursive routing, tunnel source reachability, and
security.

## Routing and signaling protocols

- Static/default routes: simple and deterministic, but need tracking/failover.
- RIP/RIPng: distance-vector, hop-count metric; mostly educational/legacy.
- OSPFv2/v3: link-state IGP using areas and SPF.
- IS-IS: link-state IGP using levels and TLVs.
- EIGRP: advanced distance-vector/hybrid behavior, DUAL and feasible successors.
- BGP-4/MP-BGP: policy-driven inter-AS and multiprotocol reachability.
- PIM: multicast routing (sparse/dense/source-specific modes).
- IGMP/MLD: host multicast membership at the L3/L2 boundary.
- VRRP/HSRP/GLBP: first-hop gateway redundancy.
- BFD: fast path failure detection used by routing protocols.
- LDP and RSVP-TE: MPLS label distribution and traffic-engineered signaling.

## Selection and validation

Do not test only adjacency. Validate this chain:

```text
neighbor/session
 -> topology/received route
 -> policy and best-path selection
 -> RIB
 -> FIB/label table
 -> neighbor rewrite
 -> data-plane path
 -> return path
```

Tests include exact neighbor set/state, unique IDs, timers/authentication, route
presence/absence, prefix-count thresholds, attributes/metrics, next-hop
resolution, VRF, ECMP, convergence, MTU, traceroute, and application probes.

Useful capture filters:

```text
ip || ipv6
icmp || icmpv6
ospf
isis
bgp
gre
esp
```

---

# Layer 4 - Transport

## TCP

TCP is connection-oriented and reliable. The three-way handshake exchanges SYN,
SYN-ACK, ACK and negotiates options such as MSS, window scaling, SACK, and
timestamps. Sequence/acknowledgment numbers track a byte stream. Flow control
protects the receiver; congestion control protects the network.

States include LISTEN, SYN-SENT, SYN-RECEIVED, ESTABLISHED, FIN-WAIT, CLOSE-WAIT,
LAST-ACK, TIME-WAIT, and CLOSED. RST aborts a connection. TIME-WAIT prevents old
segments from corrupting a new connection.

Test connection time, retransmissions, resets, zero window, MSS/PMTUD, idle
timeout, simultaneous sessions, server backlog, and graceful close.

## UDP

UDP is message-oriented with source/destination ports, length, and checksum.
It provides no handshake, retransmission, ordering, or congestion control.
Applications must define their own behavior. A UDP send succeeding does not
prove a listener received the datagram.

## SCTP, DCCP, and QUIC

- SCTP supports associations, multistreaming, and multihoming.
- DCCP offers congestion-controlled unreliable datagrams but is uncommon.
- QUIC runs over UDP, integrates TLS 1.3, supports streams, connection
  migration, and reduces handshake cost. It crosses traditional L4-L7 labels.

## Ports and sockets

Ports 0-1023 are well-known, 1024-49151 registered, and 49152-65535 dynamic by
IANA convention. A flow is commonly identified by protocol plus source and
destination addresses/ports. NAT and load balancers may rewrite it.

Examples:

| Service | Transport/port |
|---|---|
| SSH | TCP 22 |
| DNS | UDP/TCP 53; encrypted variants differ |
| DHCPv4 | UDP 67/68 |
| HTTP/HTTPS | TCP 80/443; HTTP/3 uses QUIC/UDP 443 |
| NETCONF over SSH | TCP 830 |
| BGP | TCP 179 |
| SNMP | UDP 161/162 |
| NTP | UDP 123 |
| RADIUS | usually UDP 1812/1813 |
| TACACS+ | TCP 49 |
| LDP | TCP/UDP 646 |
| syslog TLS | TCP 6514 |

Automation should set connect/read/total timeouts and classify refused,
timeout, DNS, TLS, authentication, and application failures separately.

---

# Layer 5 - Session

## Purpose

The session layer creates, maintains, synchronizes, and terminates dialogs.
Modern TCP/IP applications often implement this inside libraries or Layer 7,
so there is not always a separate Layer 5 header.

## Examples and concepts

- RPC conversations and request correlation;
- NetBIOS session service and legacy OSI session services;
- SIP dialog/session control (media itself commonly uses RTP);
- SMB sessions, SSH channels, database sessions;
- TLS session resumption is often discussed here though TLS spans L5-L6;
- checkpoints, keepalives, heartbeats, authentication sessions, reconnects.

Do not confuse:

- TCP connection with authenticated application session;
- keepalive with transaction success;
- session token validity with authorization;
- control session with media/data path.

## Automation tests

- establish/authenticate/close cleanly;
- session ID/token is unique, scoped, protected, and expires;
- idle and absolute timeouts match policy;
- reconnect and resumption do not duplicate a non-idempotent operation;
- keepalive detects a dead peer within requirement;
- multiple sessions do not leak state or authorization;
- failover preserves or deliberately terminates sessions as designed.

Python context managers model session cleanup well:

```python
with device_connection() as session:
    session.authenticate()
    session.run_read_only_check()
# close/logout occurs even when the check raises an exception
```

---

# Layer 6 - Presentation

## Purpose

Layer 6 transforms representation: serialization, character encoding,
compression, encryption, and format negotiation. Two systems can have working
TCP but still fail because they disagree on representation.

## Protocols and formats

- TLS/SSL: certificate authentication, key exchange, encryption, integrity.
- ASN.1 with BER/DER/PER: used by SNMP, certificates, and telecom systems.
- XDR: portable data representation used by some RPC systems.
- JSON, XML, YAML, CBOR, Protocol Buffers, MessagePack.
- UTF-8/UTF-16 and other character encodings.
- gzip/Brotli and media codecs/formats such as JPEG, PNG, MPEG.
- MIME and content negotiation identify application representations.

### TLS essentials

A client validates certificate chain, validity period, hostname/SAN, key usage,
and policy. Peers negotiate version/cipher and establish traffic keys. Mutual
TLS also authenticates the client certificate.

Validate:

- supported minimum/maximum TLS versions;
- certificate hostname/SAN and trusted chain;
- not-before/not-after with warning threshold;
- cipher/key policy and forward secrecy;
- ALPN protocol selection;
- mutual TLS identity when required;
- resumption and rekey behavior;
- certificate rotation without outage.

Never disable verification to make a lab "work" without documenting the trust
setup. Install the lab CA or use an explicit trusted CA file.

### Serialization tests

- schema and required fields;
- types, ranges, enums, and unknown-field policy;
- UTF-8 and special characters;
- malformed/truncated/oversized payload;
- compression limits and decompression-bomb protection;
- canonical form/signature handling;
- backward/forward compatibility.

---

# Layer 7 - Application

## Infrastructure and management protocols

### DNS

Resolves names and other records. DNS normally uses UDP 53, uses TCP for cases
such as large/truncated responses and zone transfers, and also has encrypted
transports. Record types include A, AAAA, CNAME, MX, NS, SOA, PTR, TXT, SRV,
CAA, and DNSSEC records.

Test authoritative/recursive behavior, positive/negative answer, TTL, CNAME
chain, IPv4/IPv6, split views, DNSSEC validation, TCP fallback, latency, and
failure response codes.

### DHCP

DHCPv4 commonly follows Discover, Offer, Request, Acknowledge. Relays forward
across subnets and may add information. Test scope, lease, options, relay,
reservations, exhaustion, decline/conflict, renewal/rebinding, snooping, and
rogue-server protection. DHCPv6 behavior differs and may coexist with SLAAC.

### HTTP and HTTPS

Methods include GET, HEAD, POST, PUT, PATCH, DELETE, and OPTIONS. Status classes
are 1xx informational, 2xx success, 3xx redirect, 4xx client error, and 5xx
server error. HTTP is stateless at the protocol level; cookies/tokens add state.

Test method/resource/status, headers, content type/schema, redirects, caching,
authentication/authorization, pagination, rate limits, idempotency, timeout,
TLS identity, and error bodies. Do not treat every 2xx as semantically correct.

### SSH

Provides encrypted remote login, command execution, tunnels, and SFTP. Validate
host key, key exchange/cipher/MAC policy, user authentication, AAA/command
authorization, privilege, idle timeout, source restriction, and accounting.
NETCONF commonly runs as an SSH subsystem on TCP 830.

### SNMP

Managers perform GET/GETNEXT/GETBULK/SET; agents expose OIDs in MIB trees and
send traps/informs. Prefer SNMPv3 authentication and privacy. Test views,
credentials, counter width/discontinuity, table indexing, timeout/retry, trap
delivery, and access restrictions.

### NTP/PTP

NTP synchronizes clocks using strata, reachability, delay, dispersion, and
offset. PTP provides higher precision with hardware timestamping in suitable
networks. Test selected sources, offset against requirement, authentication,
holdover, leap handling, path asymmetry, and failover.

### Email and file transfer

- SMTP sends mail; IMAP/POP retrieve it.
- FTP separates control/data and is unencrypted unless protected; SFTP is an
  SSH subsystem and is not FTP over SSH; TFTP is simple UDP with no security.
- Test authentication, encryption, active/passive/NAT behavior, integrity,
  permissions, resume, quota, and file size.

### Voice/video and real-time

SIP controls sessions; SDP describes media; RTP/RTCP carries and reports media.
Test registration, call setup/teardown, codec negotiation, one-way audio,
NAT traversal, packet loss, latency, jitter, ordering, QoS marking, and security.

### Network automation APIs

- NETCONF: XML RPC, YANG, datastores, lock/validate/commit.
- RESTCONF: HTTP access to YANG-modeled resources.
- gNMI: gRPC get/set/subscribe, often OpenConfig.
- syslog: event transport; TLS is preferred where supported.
- streaming telemetry: modelled periodic/on-change data.

Test capabilities/schema, authentication/authorization, TLS/SSH identity,
timeouts, structured error details, idempotency, concurrency conflict, rollback,
rate/volume, reconnect, and operational state after accepted configuration.

## Application test pattern

```text
resolve name
-> connect transport
-> authenticate secure channel
-> authenticate user/service
-> authorize operation
-> send valid request
-> validate status + schema + semantics
-> verify external side effect
-> test invalid/unauthorized/rate-limited request
-> close and confirm observability
```

---

# Cross-layer diagnostic examples

## Website/API failure

1. L1: link/Wi-Fi signal and errors.
2. L2: VLAN, MAC learning, STP/LAG.
3. L3: address, gateway/neighbor, route, ACL, return path.
4. L4: TCP/UDP reachability, resets/retransmissions.
5. L5: session/token establishment and timeout.
6. L6: TLS certificate/cipher and JSON/XML encoding.
7. L7: DNS answer, HTTP status/schema/semantic result.

## BGP session failure

1. L1/L2: peer-facing link and VLAN/LAG.
2. L3: route to peer/update-source and TTL.
3. L4: TCP 179 handshake/ACL.
4. L5-L7: BGP FSM, OPEN capabilities, AS/authentication, AFI/SAFI and policy.
5. Data plane: installed prefixes, next-hop resolution, FIB and traffic.

## Layered test-case template

Every automated case should record:

| Field | Example |
|---|---|
| ID | `BGP-L4-001` |
| Requirement | TCP 179 reachable only from approved peer |
| Preconditions | interface and route healthy |
| Input/action | bounded connect or capture |
| Expected | handshake succeeds from peer; denied elsewhere |
| Observed | structured values and raw evidence reference |
| Status | PASS, FAIL, ERROR, or SKIP |
| Cleanup | close socket/remove temporary lab change |
| Safety | read-only, timeout 3 s, lab subnet only |

Include positive, negative, boundary, timeout, malformed, authentication,
authorization, failure/recovery, scale, performance, and security cases.

# Practical capture and coding tools

- `ping`, `tracert`/`traceroute`, `pathping`/`mtr`.
- `Test-NetConnection`, `Resolve-DnsName`, `curl`.
- Wireshark/tshark and tcpdump.
- Scapy for authorized packet construction/analysis.
- Python `socket`, `ssl`, `ipaddress`, `http.client`, `urllib`, `json`.
- Netmiko/Scrapli/Paramiko for CLI/SSH.
- ncclient, requests/HTTPX, gNMI clients for APIs.
- pyATS/Genie, TextFSM/TTP, NAPALM for normalized observations.

The included `layer_diagnostics.py` uses only the standard library. It performs
bounded DNS, TCP, TLS, and HTTP checks. It does not scan ranges, capture traffic,
or modify a device.
