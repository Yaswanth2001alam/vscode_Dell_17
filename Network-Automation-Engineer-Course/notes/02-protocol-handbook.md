# 2. Protocol Handbook

This chapter is a field reference. Exact command syntax and default timers vary
by vendor and release. Prefer structured API/telemetry fields over scraping
decorated CLI text where possible.

## 2.1 LLDP

**Purpose:** IEEE 802.1AB link-local discovery. Devices advertise identity,
port, capabilities, management address, and optional organizational TLVs to
directly connected neighbors. Frames use destination MAC
`01:80:c2:00:00:0e` and are not routed.

**Operation:** LLDP advertisements contain chassis ID, port ID, Time To Live,
and other TLVs. A neighbor remains valid until TTL expiry. LLDP-MED adds
endpoint, voice, location, and power information.

**Validate**

- intended local interface has LLDP transmit/receive enabled;
- expected remote system and port IDs match the cabling source of truth;
- neighbor is fresh and capabilities/management address are plausible;
- exactly one expected neighbor exists unless the medium intentionally differs.

**Negative tests:** swap cables, disable transmit on one side, alter a port
description, and wait for TTL expiry. Distinguish "no neighbor" from collection
failure. LLDP is unauthenticated topology information; disable it where not
needed and do not treat a neighbor advertisement as identity proof.

## 2.2 LACP and link aggregation

**Purpose:** IEEE 802.1AX/802.3ad combines compatible physical links into one
logical link while detecting membership problems.

LACP system ID is priority plus MAC. Port ID is priority plus port number. An
aggregator selects links that agree on system/key properties. Common modes are
active and passive; at least one side should be active. Fast periodic mode sends
more frequent PDUs than slow mode.

State flags commonly include activity, timeout, aggregation,
synchronization, collecting, distributing, defaulted, and expired. A healthy
forwarding member is normally synchronized, collecting, and distributing.

**Validate**

- bundle is up and minimum-links policy is met;
- intended members are present, not suspended/individual;
- speed, duplex, MTU, VLAN mode, native/allowed VLANs, and LACP key agree;
- partner system ID and partner port map match intent;
- hashing uses expected header fields and traffic distribution is reasonable.

**Failure tests:** shut one member and measure loss; create a VLAN/MTU mismatch;
set both ends passive; move a cable; test minimum-links and recovery. One flow
normally hashes to one member, so do not expect a single flow to consume the
sum of all member bandwidth.

## 2.3 STP, RSTP, and MST

**Purpose:** prevent L2 loops while retaining redundant links.

The bridge with the lowest bridge ID (priority plus MAC, with protocol-specific
extensions) becomes root. Each non-root bridge selects a root port by best BPDU
path information. Each segment chooses a designated port. Other redundant ports
block/discard.

- Classic 802.1D states: blocking, listening, learning, forwarding, disabled.
- RSTP roles include root, designated, alternate, and backup; states are
  discarding, learning, and forwarding.
- MST maps VLANs into instances; region name, revision, and VLAN mapping must
  match for devices to be in one region.

**Root selection comparison order:** root ID, root path cost, sender bridge ID,
sender port ID, then local port ID as needed.

**Protection**

- PortFast/edge only on endpoint-facing ports.
- BPDU Guard disables an edge port receiving a BPDU.
- Root Guard prevents an unexpected superior root.
- Loop Guard helps prevent unidirectional failures from creating forwarding.
- UDLD is commonly used to detect unidirectional fiber conditions.

**Validate:** intended root/secondary, mode/region, root cost, every port role
and state, topology-change rate, edge settings, guard consistency, and no
unexpected root change. Test redundant-link failure and restoration while
measuring loss and MAC relearning. Never test a loop in production.

## 2.4 MACsec

**Purpose:** IEEE 802.1AE provides hop-by-hop Layer 2 confidentiality,
integrity, and origin authenticity. It protects a link, not the entire routed
path. MACsec commonly uses MKA (802.1X-2010) to establish secure connectivity
associations and distribute Secure Association Keys.

Key terms:

- **CA:** connectivity association shared by authorized participants.
- **SCI:** secure channel identifier, derived from system identity and port.
- **SC/SA:** secure channel and secure association; SAs support key rollover.
- **AN:** association number identifying the active SA.
- **PN:** packet number used for replay protection; exhaustion requires rekey.
- **ICV:** integrity check value.
- **SecTAG:** MACsec security tag.
- **CAK/CKN:** connectivity association key/name used by MKA.

Policies may require encryption or allow integrity-only, and may fail closed or
permit an unsecured fallback. These are security decisions, not mere reachability
settings.

**Validate**

- policy/cipher suite and key method agree;
- MKA session and secure channel are up in both directions;
- controlled port is authorized/secured as intended;
- encryption/integrity counters increment with traffic;
- invalid ICV, late/replay, and dropped-uncontrolled counters stay zero;
- active/next key and rollover state are healthy;
- effective MTU accounts for MACsec overhead.

**Tests:** correct-key establishment, wrong CAK/CKN rejection, peer loss,
rekey/rollover without unacceptable loss, replay rejection in an isolated lab,
MTU/large-frame forwarding, and fail-open/fail-closed policy. Never log keys.

## 2.5 OSPF

**Purpose:** link-state IGP using shortest-path-first calculation. OSPFv2 is for
IPv4; OSPFv3 supports IPv6 and can support additional address families.

OSPF packet types: Hello, Database Description, Link-State Request, Link-State
Update, and Link-State Acknowledgment. Neighbor states commonly progress Down,
Attempt (NBMA), Init, 2-Way, ExStart, Exchange, Loading, Full.

On broadcast/NBMA networks, a DR/BDR reduces adjacency count. Point-to-point
links do not need a DR. Neighbors generally require compatible area, timers,
authentication, network behavior, and options. Router IDs must be unique.

Areas improve scale. Area 0 is the backbone. ABRs connect areas; ASBRs
redistribute external routes. Stub, totally stubby (vendor extension), and NSSA
areas limit external information. LSA types and support vary by OSPF version
and area.

OSPF path cost is based on configured/reference bandwidth. Equal-cost routes
may be installed. External E1 includes internal cost to the ASBR; E2 normally
uses external metric primarily.

**Validate**

- expected neighbors reach Full (or 2-Way for non-DR peers where appropriate);
- unique router IDs and correct interface area/network type;
- hello/dead timers, authentication, MTU, and options match;
- expected LSAs and routes exist without unexpected redistribution;
- SPF/LSA churn is acceptable and passive interfaces are intentional;
- RIB/FIB next hops and end-to-end return path are correct.

**Failure tests:** link loss/convergence, timer mismatch, area mismatch,
authentication failure, MTU mismatch (often stuck in ExStart/Exchange),
duplicate router ID, passive interface, max-metric maintenance, and route
summarization. Use BFD carefully for faster detection; aggressive timers can
cause instability under CPU stress.

## 2.6 IS-IS

**Purpose:** link-state IGP carried directly over Layer 2 rather than IP. It is
common in service-provider cores and scalable fabrics. Integrated IS-IS carries
IP reachability using TLVs.

- Level 1 routes within an area.
- Level 2 routes between areas.
- L1/L2 routers connect both domains.
- NET identifies the routing process, area, system ID, and NSEL.

PDU families include IIH hellos, LSPs, CSNPs, and PSNPs. On broadcast media, a
DIS helps database synchronization; there is no OSPF-like backup DIS, and other
routers still form adjacencies. Point-to-point links avoid LAN election.

Adjacency states typically progress Down, Initializing, Up. Metrics may be
narrow or wide; modern networks normally use wide metrics. Authentication can
protect hello and/or LSP exchange.

**Validate:** expected level and circuit type, unique system IDs/NETs,
area agreement for L1, interface enabled for the intended address family,
authentication, MTU/padding behavior, database sequence/checksum/lifetime,
overload bit, attached bit, expected prefixes, and SPF stability.

**Failure tests:** area or level mismatch, authentication mismatch, MTU issue,
overload bit, passive interface, link failure, metric change, and LSP flooding.
Capture filters may need `isis`; remember it does not use TCP/UDP ports.

## 2.7 BGP

**Purpose:** policy-driven inter-domain and large-scale reachability exchange.
BGP runs over TCP port 179. eBGP is between autonomous systems; iBGP distributes
external or other address-family routes within an AS.

FSM states: Idle, Connect, Active, OpenSent, OpenConfirm, Established. Messages:
OPEN, UPDATE, KEEPALIVE, NOTIFICATION, and ROUTE-REFRESH.

Important attributes include ORIGIN, AS_PATH, NEXT_HOP, LOCAL_PREF, MED,
COMMUNITY, extended/large communities, and route-reflector originator/cluster
attributes. Selection details vary by vendor, but highest local preference,
shortest AS path, origin, MED under defined comparison, eBGP/iBGP, IGP cost to
next hop, and tie-breakers are common concepts. Weight is vendor-specific.

iBGP does not advertise routes learned from one iBGP peer to another by
default. Full mesh, route reflectors, or confederations solve that scaling
constraint. MP-BGP carries VPN, IPv6, EVPN, labeled, and other families.

**Validate**

- session is Established with expected local/remote AS and address family;
- source/update-source, multihop, authentication, and TTL security are correct;
- received/accepted/advertised prefix counts satisfy thresholds;
- expected prefixes and attributes exist; forbidden routes do not;
- next hops resolve in the intended VRF;
- import/export policies and default-deny behavior match intent;
- maximum-prefix, route limits, RPKI state, and graceful-restart policy are safe;
- route-reflector client/cluster design avoids loops and path hiding issues.

**Failure tests:** wrong AS, unreachable peer/source, ACL/TCP 179 block, password
mismatch, AFI/SAFI disabled, next-hop unresolved, policy deny, maximum-prefix,
route withdrawal, RPKI invalid policy, and RR failure. A TCP-established socket
does not prove the BGP session or routes are healthy.

## 2.8 MPLS, LDP, and RSVP-TE

**MPLS:** forwarding uses a label stack. An LSR can push, swap, or pop labels.
The bottom-of-stack bit identifies the last label. TTL and traffic class fields
support loop prevention and QoS behavior. Penultimate-hop popping can remove
the transport label before the egress.

**LDP:** distributes label bindings, commonly following IGP shortest paths.
Discovery typically uses UDP 646; sessions use TCP 646. Router/transport
address reachability matters.

**RSVP/RSVP-TE:** RSVP signals soft state. Path messages travel downstream and
Resv messages upstream. RSVP-TE can establish traffic-engineered label-switched
paths with constraints, explicit routes, bandwidth reservation, priorities,
fast reroute, and record-route objects. Soft state must be refreshed.

**Validate**

- IGP reachability and MPLS enabled on intended interfaces;
- label neighbor/session state and bindings align with FECs;
- LFIB operation matches push/swap/pop expectations;
- LSP/tunnel path, next hop, labels, bandwidth, priority, and protection match;
- RSVP interface bandwidth and reservation accounting are sane;
- end-to-end LSP ping/traceroute and customer route/VRF tests pass.

**Failure tests:** core link/node failure, LDP/IGP synchronization, missing MPLS
on one interface, transport-address loss, insufficient RSVP bandwidth,
constraint exclusion, preemption, FRR activation, and reoptimization. Verify
both control-plane LSP state and actual data path.

## 2.9 BFD

BFD provides rapid forwarding-path failure detection independent of a routing
protocol. Peers negotiate transmit/receive intervals and multiplier; detection
time is derived from them. Asynchronous mode is common, and echo mode may test
forwarding with reduced peer CPU work.

Validate session state, local/remote discriminators, negotiated intervals,
diagnostic reason, protocol clients, and flaps. Test path loss and CPU load.
Overly aggressive timers across many sessions can create false failures.

## 2.10 VXLAN EVPN

VXLAN encapsulates L2 frames (and, in symmetric IRB designs, routed overlay
traffic) over an IP underlay. VNI is a 24-bit segment identifier. VTEPs
encapsulate/decapsulate. BGP EVPN distributes endpoint and reachability state.

Common EVPN route concepts:

- Type 1: Ethernet auto-discovery.
- Type 2: MAC/IP advertisement.
- Type 3: inclusive multicast Ethernet tag (BUM discovery).
- Type 4: Ethernet segment route.
- Type 5: IP prefix.

**Validate:** underlay reachability/MTU, NVE/VTEP state, VLAN-to-VNI and
VRF/L3VNI mapping, route-target import/export, expected EVPN route types,
MAC/IP mobility sequence, anycast gateway consistency, multihoming/DF state,
and BUM replication/multicast. Test endpoint move, VTEP/link failure, duplicate
IP/MAC, orphan port, route withdrawal, and MTU.

## 2.11 QoS

QoS classifies, marks, polices, shapes, queues, schedules, and manages
congestion. DSCP marks the IP header; 802.1p PCP marks VLAN-tagged Ethernet.
Trust boundaries define where markings become authoritative.

Validate policy attachment/direction, class match counters, drops, queue depth,
bandwidth guarantees, policer/shaper rate and burst, remarking, and end-to-end
mark preservation. Test offered load below and above thresholds. A configuration
presence test is insufficient; counters and traffic behavior are required.

## 2.12 IPsec

IPsec protects L3 traffic. IKE authenticates peers and negotiates security
associations; ESP commonly provides confidentiality and integrity. Route-based
VPNs use tunnel interfaces; policy-based VPNs select traffic with policy.

Validate IKE and child SA state, peer identity, proposals, PFS, lifetimes,
selectors, routes, NAT exemption/traversal, anti-replay, encrypt/decrypt
counters, DPD/liveness, and rekey. Test wrong identity/key, proposal mismatch,
selector mismatch, path MTU, peer failover, replay rejection, and rekey.

## 2.13 Protocol test matrix

| Protocol | Healthy evidence | Essential negative test |
|---|---|---|
| LLDP | expected system/port and fresh TTL | disable advertisement / wrong cable |
| LACP | synchronized collecting/distributing members | member loss and key mismatch |
| STP | intended root and roles, stable changes | root attempt blocked by policy |
| MACsec | secured SAs, traffic counters, no ICV/replay errors | wrong key and rekey |
| OSPF | Full neighbors, expected LSDB/routes | area/auth/MTU mismatch |
| IS-IS | Up adjacency, expected LSPs/routes | level/auth mismatch |
| BGP | Established, policy-correct accepted routes | policy deny / max-prefix |
| LDP | operational session and correct bindings | transport loss |
| RSVP-TE | signaled LSP on intended protected path | bandwidth/path failure |
| BFD | Up with negotiated timers | forwarding path loss |
| EVPN | expected route types and endpoint state | endpoint move/VTEP loss |
| IPsec | SAs up and bidirectional counters | proposal mismatch/rekey |

