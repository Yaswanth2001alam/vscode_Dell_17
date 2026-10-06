from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass(frozen=True)
class Protocol:
    name: str
    layers: tuple[int, ...]
    purpose: str
    transport: str = ""
    default_ports: tuple[int, ...] = ()
    test_focus: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.purpose.strip():
            raise ValueError("Protocol name and purpose are required")
        if not self.layers or any(layer not in range(1, 8) for layer in self.layers):
            raise ValueError("Protocol layers must be between 1 and 7")
        if any(port not in range(1, 65536) for port in self.default_ports):
            raise ValueError("Protocol ports must be between 1 and 65535")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


PROTOCOLS: tuple[Protocol, ...] = (
    Protocol("Ethernet PHY", (1,), "Carries Ethernet symbols over physical media",
             test_focus=("link", "speed", "FEC", "signal", "errors")),
    Protocol("Wi-Fi PHY", (1,), "Carries radio symbols over 802.11 channels",
             test_focus=("RSSI", "SNR", "channel", "retries")),
    Protocol("Ethernet", (2,), "Provides local frame delivery using MAC addresses",
             test_focus=("MAC learning", "FCS", "MTU")),
    Protocol("802.1Q", (2,), "Identifies VLANs and Layer 2 priority",
             test_focus=("access VLAN", "native VLAN", "allowed VLANs")),
    Protocol("STP/RSTP/MST", (2,), "Prevents Layer 2 forwarding loops",
             test_focus=("root", "roles", "states", "guards")),
    Protocol("LACP", (2,), "Negotiates link-aggregation membership",
             test_focus=("partner", "key", "collecting", "distributing")),
    Protocol("LLDP", (2,), "Advertises link-local identity and capabilities",
             test_focus=("chassis", "port", "TTL")),
    Protocol("802.1X/EAPOL", (2,), "Controls port-based network access",
             test_focus=("authorization", "method", "assigned policy")),
    Protocol("MACsec/MKA", (2,), "Protects hop-by-hop Ethernet frames",
             test_focus=("secure channel", "encryption", "replay", "rekey")),
    Protocol("ARP", (2, 3), "Resolves an IPv4 next hop to a MAC address",
             test_focus=("binding", "age", "duplicate", "inspection")),
    Protocol("MPLS", (2, 3), "Forwards traffic using a label stack",
             test_focus=("FEC", "label operation", "LSP path")),
    Protocol("IPv4", (3,), "Provides routed 32-bit packet addressing",
             test_focus=("address", "route", "TTL", "MTU")),
    Protocol("IPv6", (3,), "Provides routed 128-bit packet addressing",
             test_focus=("scope", "route", "hop limit", "PMTUD")),
    Protocol("ICMP/ICMPv6", (3,), "Signals network errors and supports diagnostics",
             test_focus=("type/code", "loss", "latency", "packet too big")),
    Protocol("OSPF", (3,), "Exchanges link-state routes within an IGP domain",
             transport="IP protocol 89", test_focus=("neighbor", "LSDB", "route", "SPF")),
    Protocol("IS-IS", (2, 3), "Exchanges TLV-based link-state reachability",
             transport="Layer 2", test_focus=("adjacency", "LSP", "route", "SPF")),
    Protocol("BGP", (3, 7), "Exchanges policy-controlled reachability",
             transport="TCP", default_ports=(179,),
             test_focus=("FSM", "prefixes", "attributes", "policy")),
    Protocol("PIM", (3,), "Builds multicast distribution trees",
             transport="IP protocol 103", test_focus=("neighbor", "RPF", "tree")),
    Protocol("VRRP", (3,), "Provides a redundant virtual default gateway",
             transport="IP protocol 112", test_focus=("master", "priority", "failover")),
    Protocol("GRE", (3,), "Encapsulates network-layer payloads",
             transport="IP protocol 47", test_focus=("source", "destination", "MTU")),
    Protocol("IPsec ESP", (3, 6), "Protects IP traffic",
             transport="IP protocol 50", test_focus=("SA", "cipher", "replay", "rekey")),
    Protocol("TCP", (4,), "Provides reliable ordered byte streams",
             test_focus=("handshake", "state", "retransmission", "window")),
    Protocol("UDP", (4,), "Provides connectionless datagrams",
             test_focus=("listener", "loss", "ordering", "application response")),
    Protocol("SCTP", (4,), "Provides message streams and multihoming",
             transport="IP protocol 132", test_focus=("association", "path", "stream")),
    Protocol("QUIC", (4, 5, 6, 7), "Provides encrypted multiplexed application streams",
             transport="UDP", default_ports=(443,),
             test_focus=("handshake", "TLS", "streams", "migration")),
    Protocol("RPC", (5, 7), "Coordinates request-response application sessions",
             test_focus=("session", "correlation", "timeout", "idempotency")),
    Protocol("SIP", (5, 7), "Establishes and controls multimedia sessions",
             transport="UDP/TCP/TLS", default_ports=(5060, 5061),
             test_focus=("registration", "dialog", "SDP", "teardown")),
    Protocol("TLS", (5, 6), "Authenticates and encrypts application data",
             test_focus=("version", "certificate", "cipher", "ALPN")),
    Protocol("ASN.1", (6,), "Defines structured data encodings",
             test_focus=("schema", "encoding", "malformed input")),
    Protocol("JSON/XML/Protobuf", (6,), "Serializes structured application data",
             test_focus=("schema", "types", "encoding", "compatibility")),
    Protocol("DNS", (7,), "Resolves names and service records",
             transport="UDP/TCP", default_ports=(53,),
             test_focus=("answer", "TTL", "rcode", "latency")),
    Protocol("DHCPv4", (7,), "Leases IPv4 configuration to clients",
             transport="UDP", default_ports=(67, 68),
             test_focus=("DORA", "lease", "options", "relay")),
    Protocol("HTTP/HTTPS", (7,), "Transfers application resources and API messages",
             transport="TCP/QUIC", default_ports=(80, 443),
             test_focus=("status", "headers", "schema", "semantics")),
    Protocol("SSH", (7,), "Provides secure remote access and channels",
             transport="TCP", default_ports=(22,),
             test_focus=("host key", "authentication", "authorization")),
    Protocol("NETCONF", (7,), "Manages YANG data using XML RPC operations",
             transport="SSH", default_ports=(830,),
             test_focus=("capabilities", "datastore", "validate", "commit")),
    Protocol("RESTCONF", (7,), "Manages YANG data using HTTP resources",
             transport="HTTPS", default_ports=(443,),
             test_focus=("status", "media type", "schema", "ETag")),
    Protocol("gNMI", (7,), "Gets, sets, and subscribes to modeled data over gRPC",
             transport="HTTP/2 TLS", default_ports=(57400,),
             test_focus=("capabilities", "path", "sync", "timestamp")),
    Protocol("SNMP", (7,), "Reads management objects and emits notifications",
             transport="UDP", default_ports=(161, 162),
             test_focus=("version", "view", "OID", "counter")),
    Protocol("NTP", (7,), "Synchronizes clocks",
             transport="UDP", default_ports=(123,),
             test_focus=("source", "reach", "offset", "stratum")),
    Protocol("Syslog", (7,), "Transports event messages",
             transport="UDP/TCP/TLS", default_ports=(514, 6514),
             test_focus=("source", "severity", "timestamp", "delivery")),
    Protocol("RADIUS", (7,), "Provides network access AAA",
             transport="UDP", default_ports=(1812, 1813),
             test_focus=("authentication", "authorization", "accounting")),
    Protocol("TACACS+", (7,), "Provides device-administration AAA",
             transport="TCP", default_ports=(49,),
             test_focus=("authentication", "commands", "accounting")),
    Protocol("SMTP", (7,), "Transfers email",
             transport="TCP", default_ports=(25, 465, 587),
             test_focus=("TLS", "relay", "delivery")),
    Protocol("FTP/TFTP/SFTP", (7,), "Transfers files using distinct protocols",
             test_focus=("authentication", "mode", "integrity", "permissions")),
)


def protocols_for_layer(layer: int) -> tuple[Protocol, ...]:
    if layer not in range(1, 8):
        raise ValueError("Layer must be between 1 and 7")
    return tuple(protocol for protocol in PROTOCOLS if layer in protocol.layers)


def find_protocol(name: str) -> Protocol:
    normalized = name.strip().casefold()
    for protocol in PROTOCOLS:
        if protocol.name.casefold() == normalized:
            return protocol
    raise KeyError(f"Unknown protocol {name!r}")


def validate_unique_names(protocols: Iterable[Protocol] = PROTOCOLS) -> None:
    names = [protocol.name.casefold() for protocol in protocols]
    if len(names) != len(set(names)):
        raise ValueError("Protocol names must be unique")
