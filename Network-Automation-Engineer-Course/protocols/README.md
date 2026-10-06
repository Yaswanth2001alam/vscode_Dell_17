# Individual Protocol Notes

This directory contains one generated learning and testing file for every
protocol or technology in `network_course/protocol_catalog.py`. Cross-layer
protocols are stored under their lowest/primary OSI layer and list all relevant
layers in their file.

Do not edit generated protocol files directly. Update the catalog or
`tools/generate_protocol_notes.py`, then run:

```powershell
python -m tools.generate_protocol_notes
```

## Layer 1 - Physical

| Protocol | OSI layer(s) | Purpose |
|---|---|---|
| [Ethernet PHY](layer-1/ethernet-phy.md) | 1 | Carries Ethernet symbols over physical media |
| [Wi-Fi PHY](layer-1/wi-fi-phy.md) | 1 | Carries radio symbols over 802.11 channels |

## Layer 2 - Data Link

| Protocol | OSI layer(s) | Purpose |
|---|---|---|
| [Ethernet](layer-2/ethernet.md) | 2 | Provides local frame delivery using MAC addresses |
| [802.1Q](layer-2/802-1q.md) | 2 | Identifies VLANs and Layer 2 priority |
| [STP/RSTP/MST](layer-2/stp-rstp-mst.md) | 2 | Prevents Layer 2 forwarding loops |
| [LACP](layer-2/lacp.md) | 2 | Negotiates link-aggregation membership |
| [LLDP](layer-2/lldp.md) | 2 | Advertises link-local identity and capabilities |
| [802.1X/EAPOL](layer-2/802-1x-eapol.md) | 2 | Controls port-based network access |
| [MACsec/MKA](layer-2/macsec-mka.md) | 2 | Protects hop-by-hop Ethernet frames |
| [ARP](layer-2/arp.md) | 2, 3 | Resolves an IPv4 next hop to a MAC address |
| [MPLS](layer-2/mpls.md) | 2, 3 | Forwards traffic using a label stack |
| [IS-IS](layer-2/is-is.md) | 2, 3 | Exchanges TLV-based link-state reachability |

## Layer 3 - Network

| Protocol | OSI layer(s) | Purpose |
|---|---|---|
| [IPv4](layer-3/ipv4.md) | 3 | Provides routed 32-bit packet addressing |
| [IPv6](layer-3/ipv6.md) | 3 | Provides routed 128-bit packet addressing |
| [ICMP/ICMPv6](layer-3/icmp-icmpv6.md) | 3 | Signals network errors and supports diagnostics |
| [OSPF](layer-3/ospf.md) | 3 | Exchanges link-state routes within an IGP domain |
| [BGP](layer-3/bgp.md) | 3, 7 | Exchanges policy-controlled reachability |
| [PIM](layer-3/pim.md) | 3 | Builds multicast distribution trees |
| [VRRP](layer-3/vrrp.md) | 3 | Provides a redundant virtual default gateway |
| [GRE](layer-3/gre.md) | 3 | Encapsulates network-layer payloads |
| [IPsec ESP](layer-3/ipsec-esp.md) | 3, 6 | Protects IP traffic |

## Layer 4 - Transport

| Protocol | OSI layer(s) | Purpose |
|---|---|---|
| [TCP](layer-4/tcp.md) | 4 | Provides reliable ordered byte streams |
| [UDP](layer-4/udp.md) | 4 | Provides connectionless datagrams |
| [SCTP](layer-4/sctp.md) | 4 | Provides message streams and multihoming |
| [QUIC](layer-4/quic.md) | 4, 5, 6, 7 | Provides encrypted multiplexed application streams |

## Layer 5 - Session

| Protocol | OSI layer(s) | Purpose |
|---|---|---|
| [RPC](layer-5/rpc.md) | 5, 7 | Coordinates request-response application sessions |
| [SIP](layer-5/sip.md) | 5, 7 | Establishes and controls multimedia sessions |
| [TLS](layer-5/tls.md) | 5, 6 | Authenticates and encrypts application data |

## Layer 6 - Presentation

| Protocol | OSI layer(s) | Purpose |
|---|---|---|
| [ASN.1](layer-6/asn-1.md) | 6 | Defines structured data encodings |
| [JSON/XML/Protobuf](layer-6/json-xml-protobuf.md) | 6 | Serializes structured application data |

## Layer 7 - Application

| Protocol | OSI layer(s) | Purpose |
|---|---|---|
| [DNS](layer-7/dns.md) | 7 | Resolves names and service records |
| [DHCPv4](layer-7/dhcpv4.md) | 7 | Leases IPv4 configuration to clients |
| [HTTP/HTTPS](layer-7/http-https.md) | 7 | Transfers application resources and API messages |
| [SSH](layer-7/ssh.md) | 7 | Provides secure remote access and channels |
| [NETCONF](layer-7/netconf.md) | 7 | Manages YANG data using XML RPC operations |
| [RESTCONF](layer-7/restconf.md) | 7 | Manages YANG data using HTTP resources |
| [gNMI](layer-7/gnmi.md) | 7 | Gets, sets, and subscribes to modeled data over gRPC |
| [SNMP](layer-7/snmp.md) | 7 | Reads management objects and emits notifications |
| [NTP](layer-7/ntp.md) | 7 | Synchronizes clocks |
| [Syslog](layer-7/syslog.md) | 7 | Transports event messages |
| [RADIUS](layer-7/radius.md) | 7 | Provides network access AAA |
| [TACACS+](layer-7/tacacs.md) | 7 | Provides device-administration AAA |
| [SMTP](layer-7/smtp.md) | 7 | Transfers email |
| [FTP/TFTP/SFTP](layer-7/ftp-tftp-sftp.md) | 7 | Transfers files using distinct protocols |
