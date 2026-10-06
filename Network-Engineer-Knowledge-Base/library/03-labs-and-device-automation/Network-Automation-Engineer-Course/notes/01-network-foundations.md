# 1. Network Foundations

## 1.1 Mental model: control, data, and management planes

- **Data plane:** forwards frames/packets using programmed tables. Examples are
  MAC lookup, FIB lookup, ACL classification, label swap, and queue selection.
- **Control plane:** learns topology and calculates state. STP, OSPF, IS-IS,
  BGP, LDP, and RSVP are control-plane protocols.
- **Management plane:** configures and observes the device through console, SSH,
  SNMP, NETCONF, RESTCONF, gNMI, logs, and telemetry.

Automation usually enters through the management plane, expresses control-plane
intent, and verifies the data plane. A green configuration response is not
proof that packets forward.

## 1.2 Encapsulation and a packet walk

When a client opens HTTPS to a server:

1. DNS may resolve a name to an IPv4 or IPv6 address.
2. The application gives bytes to TCP. TCP selects ports, establishes state
   using SYN/SYN-ACK/ACK, sequences bytes, retransmits loss, and controls flow.
3. IP adds source/destination addresses. The host performs a longest-prefix
   match. A remote destination uses a default or more-specific route.
4. ARP (IPv4) or Neighbor Discovery (IPv6) resolves the next-hop IP to a MAC.
5. Ethernet carries the packet to the next hop. Switches learn source MACs and
   forward based on the destination MAC within a VLAN.
6. A router removes the L2 header, decrements IPv4 TTL or IPv6 Hop Limit,
   performs a route/FIB lookup, applies policy, and creates a new L2 header.
7. NAT, firewalls, load balancers, tunnels, MPLS labels, or overlays may alter
   the path. The reverse path can be different.

Automation tests should separate:

- name resolution;
- local interface and VLAN state;
- gateway/neighbor resolution;
- route and policy selection;
- transport connection;
- application response.

## 1.3 Ethernet and switching

An Ethernet frame includes destination MAC, source MAC, optional 802.1Q tag,
EtherType/length, payload, and frame check sequence (FCS). Preamble and
inter-frame gap are physical-layer overhead.

Key behavior:

- A switch learns the **source** MAC on the ingress port.
- Known unicast is forwarded to the learned port.
- Unknown unicast and broadcast are flooded in the VLAN, except ingress.
- Multicast forwarding depends on flooding or snooping/control-plane state.
- Entries age; moves can indicate endpoint mobility, loops, or miswiring.
- MTU mismatch can drop large frames while small pings succeed.

Useful checks:

```text
show interfaces status
show interfaces counters errors
show mac address-table
show vlan
show interfaces trunk
show spanning-tree
```

Test normal forwarding, unknown unicast policy, MAC learning, MAC moves,
broadcast containment, MTU, CRC/input/output errors, and speed/duplex.

## 1.4 VLANs and 802.1Q

A VLAN is an L2 broadcast domain. An access port normally carries one untagged
data VLAN. A trunk carries multiple VLANs using 802.1Q tags. The native VLAN is
usually untagged and must match on both ends.

Common failures:

- VLAN absent, suspended, or not allowed on a trunk.
- Native VLAN mismatch.
- Access/trunk mode mismatch.
- STP blocks the only expected path.
- SVI is down because no active member exists.
- Allowed-VLAN pruning breaks only selected services.
- Voice and data VLAN policy differs from the endpoint expectation.

Automation contract: desired mode, access/native VLAN, allowed VLAN set,
operational mode, forwarding state per VLAN, and endpoint MAC presence.

## 1.5 IPv4, subnetting, and forwarding

CIDR `/n` says the first `n` bits identify the network. For a normal subnet:

- network address: host bits all zero;
- broadcast address: host bits all one;
- usable host convention: values between them;
- total addresses: `2 ** (32 - prefix_length)`.

Exceptions include `/31` point-to-point links (RFC 3021) and `/32` host routes.
Routers choose the longest matching prefix, then protocol administrative
preference/distance, then protocol metric, and possibly equal-cost paths.

Know the difference:

- **RIB:** control-plane routes and alternatives.
- **FIB:** routes programmed for forwarding.
- **Adjacency/neighbor table:** L2 rewrite information for the next hop.

Test connected routes, recursive next-hop resolution, default route, longest
match, ECMP, unreachable next hop, VRF separation, ACL/NAT impact, and return
path.

## 1.6 IPv6 and Neighbor Discovery

IPv6 uses 128-bit addresses. Important scopes/types:

- global unicast, commonly from `2000::/3`;
- link-local `fe80::/10`, required on IPv6 interfaces;
- unique local `fc00::/7`;
- multicast `ff00::/8`;
- loopback `::1`; unspecified `::`; no broadcast.

Neighbor Discovery uses ICMPv6 for router solicitation/advertisement, neighbor
solicitation/advertisement, redirects, duplicate-address detection, and address
autoconfiguration. Blocking ICMPv6 broadly breaks IPv6.

Verify address scope, prefix length, link-local next hop, router advertisement
flags/lifetime, neighbor state, route, Path MTU Discovery, and dual-stack DNS.

## 1.7 ARP and common gateway behavior

ARP maps an on-link IPv4 address to a MAC. Request is broadcast; reply is
normally unicast. Gratuitous ARP can announce an address/MAC binding and assist
failover. Dynamic ARP Inspection can validate bindings against a trusted source.

HSRP, VRRP, and similar first-hop redundancy protocols present a virtual IP and
MAC. Test active/master selection, priority/preemption policy, tracked uplink
failure, gratuitous ARP update, failover loss, and recovery behavior.

## 1.8 TCP, UDP, and ICMP

TCP provides a byte stream with sequencing, acknowledgments, retransmission,
flow control, congestion control, and connection state. A successful TCP
three-way handshake proves more than ICMP reachability but not application
health. Inspect resets, retransmissions, zero windows, MSS, and handshake time.

UDP has no handshake or delivery guarantee. The application implements any
reliability. DNS, streaming, syslog, SNMP, and routing protocols may use UDP.

ICMP reports errors and supports diagnostics. Important messages include echo,
destination unreachable, time exceeded, packet-too-big, and redirects. Ping
loss and latency are observations, not diagnoses.

## 1.9 Infrastructure services

| Service | Typical port | What to validate |
|---|---:|---|
| DNS | UDP/TCP 53 | correct view, A/AAAA/PTR, TTL, recursion policy, latency |
| DHCPv4 | UDP 67/68 | scope, relay, options, lease, exclusions, snooping |
| DHCPv6 | UDP 546/547 | stateful/stateless mode, relay, prefix delegation |
| NTP | UDP 123 | selected source, offset, reach, stratum, authentication |
| SNMP | UDP 161/162 | prefer v3, views, traps, counters, rate and timeout |
| Syslog | UDP/TCP/TLS 514/6514 | source, timestamp, severity, loss, TLS |
| SSH | TCP 22 | host key, algorithms, AAA, privilege, timeout |
| HTTPS | TCP 443 | certificate, hostname, expiry, TLS policy, API response |
| RADIUS | UDP 1812/1813 | auth/accounting, shared secret, fallback |
| TACACS+ | TCP 49 | AAA, command authorization, accounting, fallback |

## 1.10 Wireshark/tcpdump method

Capture as close as possible to both sides of a suspected failure. Record time,
interface, direction, capture filter, and topology. Useful display filters:

```text
arp
icmp || icmpv6
tcp.flags.syn == 1
tcp.analysis.retransmission
dns
lldp || lacp || stp
ospf || bgp || isis
```

Follow a stream, compare sequence/timestamps, and correlate capture evidence
with device counters and logs. Packet capture may contain credentials, payload,
addresses, and customer data; minimize scope, protect files, and delete them
according to policy.

