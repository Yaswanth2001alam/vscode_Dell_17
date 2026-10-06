# Comprehensive Network pytest Test Catalog

This catalog is a planning reference. Select tests based on topology, platform,
service intent, risk, and available lab capabilities. Not every test applies to
every network.

## 1. Inventory and source-of-truth tests

- Inventory file parses and matches its schema version.
- Required device fields exist and unknown fields follow policy.
- Device names, IDs, management endpoints, serials, and loopbacks are unique.
- IP addresses, prefixes, ports, ASNs, VLANs, VNIs, route targets, and metrics
  are within valid ranges.
- IPv4/IPv6 networks do not overlap unless explicitly allowed.
- Every peer/link reference resolves and is reciprocal where required.
- Interface names are valid for the selected platform.
- Device platform, OS, role, site, and groups use allowed values.
- Variables resolve with documented precedence and required values are not null.
- No password, token, key, community, or real production secret is committed.
- Every production device has owner, site, role, maintenance, backup, and
  out-of-band metadata.
- Change selection contains only approved devices and respects batch limits.

## 2. Configuration-generation tests

- Jinja2 renders with `StrictUndefined`.
- Rendering is deterministic for identical input.
- Output contains required commands/sections exactly once.
- Output excludes forbidden/deprecated/insecure commands.
- Platform syntax and hierarchy are correct.
- Interface, policy, prefix-list, community, VLAN, VRF, and routing references
  are defined before use.
- Configuration is idempotent or semantic diff is empty on second application.
- Empty lists do not generate invalid stanzas.
- IPv4 and IPv6 render correctly.
- Boundary values render correctly.
- Malformed/unsupported input fails before connecting.
- Candidate diff remains inside approved scope and line-count threshold.
- Rollback configuration/checkpoint can be generated.
- Secrets are references or redacted, never rendered into reports.

## 3. Parser and normalization contract tests

- Healthy real output parses into the expected normalized shape.
- Empty valid output is distinguished from parser failure.
- CLI error text is detected.
- Permission-denied output becomes ERROR.
- Wrapped, paged, banner-prefixed, and localized output is handled or rejected.
- Alternate supported software-release formats parse.
- Missing optional fields use explicit `None`, not misleading defaults.
- Missing required fields fail loudly.
- Invalid IP, integer, enum, timestamp, and counter values fail.
- Duplicate rows and reordered fields are handled deterministically.
- JSON/XML namespaces and schema revisions are handled.
- Large tables do not produce quadratic behavior.
- Raw evidence is retained and sensitive fields are redacted.

## 4. Layer 1 and interface tests

- Administrative and operational state match intent.
- Negotiated speed/duplex/media/lane count match.
- Autonegotiation and FEC mode match.
- MTU supports expected frame/packet size.
- Input/output/CRC/FCS/symbol/discard counters do not increase beyond policy.
- Carrier transitions and interface flaps remain below threshold.
- Optic vendor, type, wavelength, reach, and supported status match.
- Transmit/receive optical power, bias, voltage, and temperature are inside the
  specific optic's warning/alarm thresholds.
- Wireless channel, width, RSSI, SNR, noise, retry, utilization, and data rate
  meet policy.
- PoE class, allocation, delivery, and budget meet endpoint requirements.
- Link fails and recovers within the required time in a lab.
- Unidirectional fault detection works.
- Redundant link/member failure preserves the service.

## 5. Layer 2 tests

### Ethernet, VLAN, trunks, and MAC

- Access/trunk/routed mode matches.
- Access, voice, native, and allowed VLANs match exact intent.
- VLAN exists, is active, and has intended ports.
- No forbidden VLAN traverses the trunk.
- MAC address appears on expected interface/VLAN.
- Static/dynamic MAC type and aging match.
- MAC move/flap rate remains below threshold.
- Broadcast, multicast, and unknown-unicast policy matches.
- Storm-control thresholds and actions match.
- QinQ outer/inner tags and rewrite behavior match.

### LLDP/CDP

- Exact neighbor chassis/system and remote port are present.
- No unexpected neighbor exists.
- Management address, capabilities, description, and TTL are valid.
- Neighbor symmetry agrees from both ends.
- Expired/stale neighbor disappears within policy.

### LACP/link aggregation

- Logical bundle and exact members are present/up.
- Actor/partner system IDs, keys, port IDs, and modes match.
- Members are synchronized, collecting, and distributing.
- No member is individual, suspended, defaulted, or expired.
- Speed/duplex/MTU/VLAN policy is consistent across members.
- Minimum-links behavior matches.
- Hashing and multi-flow distribution are reasonable.
- One-member and multi-member failure/recovery meet loss objectives.

### STP/RSTP/MST

- Mode, region name, revision, and VLAN-instance mapping match.
- Intended root and secondary root are selected.
- Port roles, costs, priorities, and states match.
- Edge/PortFast is enabled only on approved endpoint ports.
- BPDU Guard, Root Guard, Loop Guard, and UDLD policies match.
- Topology-change rate remains below threshold.
- Superior-root attempts are blocked in a lab.
- Redundant path convergence meets requirement.

### 802.1X and MACsec

- Supplicant authentication succeeds with approved method.
- Invalid identity/credential/certificate is rejected.
- Assigned VLAN, downloadable ACL, role, and session timeout match.
- MAB fallback occurs only for approved endpoint classes.
- MACsec MKA session and secure channels are up.
- Cipher, confidentiality offset, replay window, and policy match.
- Protected/encrypted counters increase and invalid ICV/replay drops do not.
- Wrong key is rejected and rekey completes within loss objective.

## 6. IPv4, IPv6, and first-hop tests

- Address, mask/prefix, scope, anycast/virtual address, and VRF match.
- Connected and local routes exist.
- No duplicate IPv4/IPv6 address is detected.
- ARP/ND entry maps expected IP to MAC/interface.
- Neighbor state is reachable/stable and stale entries recover.
- IPv6 link-local address and router advertisement flags/lifetimes match.
- SLAAC/DHCPv6 behavior matches endpoint policy.
- DAD detects a duplicate in an isolated lab.
- Default gateway/FHRP virtual IP and MAC match.
- HSRP/VRRP active/master, standby/backup, priority, preemption, and tracking
  match.
- Gateway failure, gratuitous ARP/NA update, recovery, and packet loss meet SLA.
- Path MTU Discovery and near-MTU traffic work for IPv4 and IPv6.

## 7. Routing-protocol tests

### Static and policy routing

- Required static/default route exists with correct VRF, next hop, distance, and
  tracking.
- Recursive next hop resolves.
- Floating static activates only after primary failure.
- Policy-based routing match/action and fallback match.

### OSPF

- Exact expected neighbor set exists; no unexpected neighbor.
- State is Full, except intentional broadcast non-adjacent peers.
- Router IDs are unique.
- Area, network type, hello/dead/retransmit timers, priority, MTU, authentication,
  and BFD match.
- DR/BDR outcome matches intent.
- Required LSAs/prefixes exist and forbidden redistributed routes do not.
- Stub/NSSA/default/summarization behavior matches.
- Route type, metric, next hop, ECMP, and FIB match.
- SPF/LSA churn remains below threshold.
- Link/node failure and recovery convergence meet SLA.

### IS-IS

- Exact expected adjacency set and Up state.
- NET/system ID uniqueness and area/level/circuit type match.
- Hello timers, priority, DIS, authentication, MTU, and address families match.
- Required LSPs/TLVs/prefixes exist.
- Overload/attached bits match operational intent.
- Wide metrics, route selection, ECMP, and FIB match.
- LSP churn and SPF frequency remain below threshold.
- Link/node failure and recovery convergence meet SLA.

### BGP

- Exact expected neighbor set and Established state.
- Local/remote AS, router ID, source, multihop/TTL security, authentication, and
  capabilities match.
- Required AFI/SAFI is negotiated.
- Received, accepted, rejected, and advertised prefix counts are in range.
- Required prefixes exist and forbidden/default/bogon routes do not.
- Local preference, AS path, origin, MED, next hop, communities, and RPKI state
  match policy.
- Import/export policy, maximum-prefix, remove-private-AS, next-hop-self, and
  default-originate match.
- Route-reflector client, cluster ID, originator ID, and path propagation match.
- Graceful-restart/helper behavior matches.
- Withdraw, failover, route-reflector loss, and recovery converge within SLA.
- TCP session without correct routing policy does not count as service success.

### Multicast and BFD

- IGMP/MLD membership and snooping state match.
- PIM neighbors, mode, RP/BSR, RPF, source/group tree, and outgoing interfaces
  match.
- Receiver join/leave and source failure behavior meet SLA.
- BFD state, discriminators, negotiated intervals/multiplier, clients, and
  diagnostic reason match.
- Aggressive timer scale does not overload control plane.

## 8. MPLS, VPN, and overlay tests

- MPLS enabled on exact core interfaces.
- LDP discovery/session, transport address, peer, FEC, and label bindings match.
- LIB/LFIB push/swap/pop operations match expected LSP.
- LDP/IGP synchronization prevents blackholing.
- RSVP-TE tunnel state, explicit/recorded path, bandwidth, affinity, priority,
  preemption, FRR, and reoptimization match.
- LSP ping/traceroute succeeds.
- VRF RD, import/export route targets, routes, labels, and route leaking match.
- PE-CE protocol and customer reachability are isolated correctly.
- VXLAN VTEP/NVE state, source, VNI, replication, and MTU match.
- EVPN route types, route targets, MAC/IP routes, mobility sequence, Ethernet
  segment, DF, and anycast gateway match.
- Endpoint move, VTEP loss, multihoming failure, and recovery meet SLA.

## 9. Transport and active-probe tests

- TCP port accepts/refuses/times out as intended.
- TCP handshake latency is below threshold.
- MSS, window scale, SACK, timestamps, keepalive, idle timeout, and close
  behavior match.
- No excessive retransmission, reset, duplicate ACK, or zero-window behavior.
- UDP request receives the correct application response.
- Loss, latency, jitter, reordering, and duplication meet SLA.
- SCTP association, paths, streams, and failover match.
- QUIC version, TLS, streams, migration, and fallback behavior match.
- NAT/firewall state, translation, timeout, and return traffic match.
- Load balancer health, distribution, persistence, failover, and draining match.

## 10. Infrastructure service tests

### DNS

- A, AAAA, CNAME, PTR, MX, NS, SOA, TXT, SRV, and CAA answers match.
- Correct recursive/authoritative view and response code.
- TTL and negative caching match.
- TCP fallback and large responses work.
- DNSSEC status and failure behavior match.
- Split-horizon answers are correct from each client zone.
- Latency, availability, failover, and cache behavior meet SLA.

### DHCP

- Discover/Offer/Request/Ack completes.
- Scope, relay, server ID, address, mask, router, DNS, domain, NTP, routes,
  lease/T1/T2, reservation, and options match.
- Renewal, rebinding, release, decline, exhaustion, failover, and conflict
  detection behave correctly.
- Snooping trust/bindings and rogue-server blocking work.

### NTP/PTP

- Client is synchronized to an approved source.
- Reachability, stratum, offset, delay, jitter, dispersion, and frequency meet
  policy.
- Authentication and source restrictions match.
- Preferred source failure, failover, holdover, and recovery meet requirement.
- PTP grandmaster, domain, profile, port state, path delay, and hardware
  timestamping match.

### SNMP, syslog, and telemetry

- SNMPv3 authentication/privacy succeeds; invalid credentials fail.
- View allows required OIDs and denies forbidden OIDs/SET.
- Scalar/table values and counter-rate calculations are correct.
- Trap/inform delivery, retry, source, timestamp, and content match.
- Syslog source, transport/TLS, facility, severity, timestamp, parsing,
  deduplication, and retention match.
- Streaming telemetry capabilities, paths, values, sample/on-change behavior,
  sync response, deletes, timestamps, reconnect, stale-data detection, and
  backpressure match.

## 11. Application, API, and management tests

- SSH host key, algorithms, authentication, privilege, authorization, timeout,
  and accounting match.
- NETCONF capabilities/datastores exist as required.
- NETCONF get/filter, lock, edit, validate, confirmed commit, cancel/rollback,
  commit, notification, and RPC error details work.
- RESTCONF resource, method, media type, status, body/schema, ETag, conflict,
  authentication, authorization, pagination, and rate limit work.
- gNMI capabilities, get, set, atomicity, subscribe modes, updates, deletes,
  timestamps, sync, and reconnect work.
- HTTP method, URL, redirect, status, headers, content type, schema, semantics,
  cache, compression, pagination, idempotency, authentication, authorization,
  rate limit, timeout, and error response match.
- API returns correct error category rather than success-shaped empty data.
- CLI command privilege, error detection, pager handling, prompt, timeout, and
  output parsing work.

## 12. Security tests

- Management ACL/firewall permits only approved sources and services.
- Default credentials, Telnet, HTTP, SNMPv1/v2c, weak SSH/TLS algorithms, and
  unused services are absent.
- SSH host keys and TLS certificate chain, hostname, validity, key usage, and
  minimum version match.
- AAA authentication, command authorization, accounting, fallback, lockout, and
  least privilege match.
- ACL rules permit required flows and deny forbidden flows in correct order.
- Control-plane policing counters/rates and protection behavior match.
- Routing authentication, TTL security, prefix limits, bogon filtering, RPKI,
  and route policy match.
- DHCP snooping, Dynamic ARP Inspection, source guard, RA Guard, BPDU Guard,
  storm control, and port security work.
- Secrets do not appear in repositories, logs, exceptions, reports, backups, or
  packet captures.
- Invalid, oversized, malformed, replayed, spoofed, downgraded, unauthorized,
  and rate-exceeding inputs are rejected safely.

## 13. Change, resilience, and operations tests

- Pre-check verifies identity, health, redundancy, time, storage, and backup.
- Dry-run lists exact devices and semantic changes.
- Backup/checkpoint is complete and restorable.
- Change runs only against approved scope and bounded concurrency.
- Accepted configuration reaches intended operational state.
- Reapplying intent is idempotent.
- Manual drift is detected and reported.
- Canary and each batch satisfy health gates before continuation.
- Defined stop conditions halt later batches.
- Link, member, node, process, route, service, controller, DNS, AAA, NTP, and
  telemetry collector failures are detected.
- Convergence, traffic loss, session survival, and recovery meet objectives.
- Rollback restores configuration and operational/data-plane health.
- Evidence includes run ID, time, code revision, device, expected, observed,
  result, duration, and error.

## 14. Performance, scale, and soak tests

- Collection latency and timeout percentiles meet target.
- Concurrent workers stay within device/AAA/controller capacity.
- Route, MAC, ARP/ND, VLAN, ACL, session, tunnel, and telemetry scale meet
  supported design.
- CPU, memory, queue, buffer, drop, and control-plane health remain acceptable.
- High churn does not cause loss beyond objective.
- API pagination, bulk retrieval, and rate limits behave correctly.
- Long-duration soak has no memory leak, session leak, stale lock, or increasing
  error rate.
- Reports remain bounded and complete at scale.

## 15. pytest-specific quality tests

- Marker names are registered and strict marker mode is enabled.
- Live/disruptive tests skip unless explicitly enabled.
- Fixtures have the narrowest practical scope.
- Tests are independent and order-insensitive.
- Parameter IDs clearly name protocol/peer/boundary.
- No test depends on production by default.
- Timeouts prevent a hung device from hanging CI.
- Retries are limited to known transient read-only operations and reported.
- Flaky tests are fixed, not hidden by broad reruns or `xfail`.
- JUnit/artifacts preserve failures without exposing secrets.

