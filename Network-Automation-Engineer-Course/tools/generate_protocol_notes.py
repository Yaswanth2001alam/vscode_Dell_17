from __future__ import annotations

import re
from pathlib import Path

from network_course.protocol_catalog import PROTOCOLS, Protocol


COURSE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = COURSE_DIR / "protocols"
LAYER_NAMES = {
    1: "Physical",
    2: "Data Link",
    3: "Network",
    4: "Transport",
    5: "Session",
    6: "Presentation",
    7: "Application",
}

CAPTURE_FILTERS = {
    "Ethernet": "eth",
    "802.1Q": "vlan",
    "STP/RSTP/MST": "stp",
    "LACP": "lacp",
    "LLDP": "lldp",
    "802.1X/EAPOL": "eapol",
    "ARP": "arp",
    "IPv4": "ip",
    "IPv6": "ipv6",
    "ICMP/ICMPv6": "icmp || icmpv6",
    "OSPF": "ospf",
    "IS-IS": "isis",
    "BGP": "bgp || tcp.port == 179",
    "PIM": "pim",
    "VRRP": "vrrp",
    "GRE": "gre",
    "IPsec ESP": "esp || isakmp",
    "TCP": "tcp",
    "UDP": "udp",
    "SCTP": "sctp",
    "QUIC": "quic || udp.port == 443",
    "SIP": "sip || rtp || rtcp",
    "TLS": "tls",
    "DNS": "dns",
    "DHCPv4": "bootp",
    "HTTP/HTTPS": "http || tls",
    "SSH": "tcp.port == 22",
    "NETCONF": "tcp.port == 830",
    "RESTCONF": "http || tls",
    "gNMI": "http2 || tcp.port == 57400",
    "SNMP": "snmp",
    "NTP": "ntp",
    "Syslog": "syslog || tcp.port == 6514",
    "RADIUS": "radius",
    "TACACS+": "tcp.port == 49",
    "SMTP": "smtp",
    "FTP/TFTP/SFTP": "ftp || ftp-data || tftp || tcp.port == 22",
}

EVIDENCE_HINTS = {
    1: (
        "interface admin/oper state and negotiated media settings",
        "optic, PHY, signal, error, and carrier-transition counters",
        "two timestamped samples so counter rates can be calculated",
    ),
    2: (
        "local interface/VLAN state and forwarding role",
        "peer identity, MAC/control-PDU state, and error counters",
        "a bounded packet capture on an authorized lab interface",
    ),
    3: (
        "neighbor/session state and topology or received-route data",
        "RIB, FIB, adjacency/label state, and next-hop resolution",
        "forward and return-path probes with loss, latency, and MTU evidence",
    ),
    4: (
        "socket endpoints, state, negotiated options, and timeout",
        "handshake/close packets and retransmission/reset counters",
        "application response proving more than port reachability",
    ),
    5: (
        "session identity, establishment, authentication, and keepalive state",
        "idle/absolute timeout and reconnect/resumption behavior",
        "clean termination and server-side accounting",
    ),
    6: (
        "negotiated encoding, schema, compression, or cryptographic parameters",
        "identity/certificate validation and expiry where applicable",
        "successful and malformed payload decoding evidence",
    ),
    7: (
        "request, response status, headers/metadata, and structured body",
        "authentication, authorization, rate-limit, and audit evidence",
        "the intended external side effect or operational state",
    ),
}


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-")
    if not slug:
        raise ValueError(f"Cannot create filename for protocol {name!r}")
    return slug


def layer_label(protocol: Protocol) -> str:
    return ", ".join(
        f"Layer {layer} ({LAYER_NAMES[layer]})" for layer in protocol.layers
    )


def relative_layer_guide(protocol: Protocol) -> str:
    primary_layer = min(protocol.layers)
    return (
        "../../notes/07-osi-layers-and-protocols.md"
        f"#layer-{primary_layer}---{LAYER_NAMES[primary_layer].casefold().replace(' ', '-')}"
    )


def render_protocol(protocol: Protocol) -> str:
    primary_layer = min(protocol.layers)
    ports = ", ".join(str(port) for port in protocol.default_ports) or "None fixed"
    transport = protocol.transport or "Native to its layer or implementation-specific"
    focus_rows = "\n".join(
        f"| `{slugify(focus)}` | Expected value derived from source of truth | "
        f"Observed {focus} | PASS/FAIL/ERROR |"
        for focus in protocol.test_focus
    )
    objectives = "\n".join(
        f"- Explain and validate **{focus}**." for focus in protocol.test_focus
    )
    positive_tests = "\n".join(
        f"{index}. Verify `{focus}` matches the approved intent under normal operation."
        for index, focus in enumerate(protocol.test_focus, start=1)
    )
    negative_tests = "\n".join(
        f"{index}. Introduce a controlled `{focus}` mismatch in an isolated lab and "
        "confirm the validator reports FAIL rather than ERROR or PASS."
        for index, focus in enumerate(protocol.test_focus, start=1)
    )
    evidence = "\n".join(
        f"- {item}." for item in EVIDENCE_HINTS[primary_layer]
    )
    capture_filter = CAPTURE_FILTERS.get(protocol.name)
    capture_section = (
        "Use this Wireshark display filter in an authorized lab:\n\n"
        f"```text\n{capture_filter}\n```\n"
        if capture_filter
        else (
            "No universal Wireshark filter applies. Collect the platform's structured "
            "operational state and use the encapsulating protocol's filter when needed.\n"
        )
    )
    slug = slugify(protocol.name)

    return f"""<!-- Generated by tools/generate_protocol_notes.py; edit the catalog or generator. -->
# {protocol.name}

## Classification

| Property | Value |
|---|---|
| OSI placement | {layer_label(protocol)} |
| Primary layer | Layer {primary_layer} - {LAYER_NAMES[primary_layer]} |
| Transport/encapsulation | {transport} |
| Default ports | {ports} |

## Purpose

{protocol.purpose}.

The OSI placement is a learning aid. Implementations can cross layers, and a
successful lower-layer check does not prove that {protocol.name} is healthy.

## Learning objectives

After this module, you should be able to:

- Explain the problem solved by {protocol.name} and its operational scope.
- Identify its peers/endpoints, messages, state, timers, and identifiers.
{objectives}
- Distinguish protocol failure from collection, parsing, and transport errors.
- Design positive, negative, failure/recovery, scale, and security tests.

## How it works

Study {protocol.name} in this order:

1. **Scope and participants:** identify where it operates and every endpoint or
   peer that must agree.
2. **Discovery or establishment:** document how communication starts and which
   lower layers must already work.
3. **Messages and state:** list important message types, state transitions,
   timers, and negotiated capabilities.
4. **Selection or forwarding:** explain how the winning path, member, encoding,
   session, or response is selected.
5. **Failure behavior:** document detection, timeout, withdrawal, reconvergence,
   retry, and recovery.
6. **Security:** document identity, authentication, integrity, encryption,
   authorization, filtering, and resource limits.

For protocol-specific theory, read the
[OSI Layer 1-7 guide]({relative_layer_guide(protocol)}) and the
[protocol handbook](../../notes/02-protocol-handbook.md).

## Important validation fields

| Check | Expected | Observed | Result |
|---|---|---|---|
{focus_rows}

Do not accept configuration presence as proof of operational health. Save both
the intended value and the observed value.

## Evidence to collect

{evidence}
- Device/software identity, timestamp, command/API path, and collection status.
- Raw evidence reference plus normalized fields used by policy.

## Packet-capture guidance

{capture_section}
Capture files can contain addresses, identities, credentials, and payloads.
Minimize scope, restrict access, sanitize before sharing, and follow retention
policy.

## Positive tests

{positive_tests}
{len(protocol.test_focus) + 1}. Repeat collection to prove stable state rather
than one transient sample.
{len(protocol.test_focus) + 2}. Verify the real data-plane or application
outcome, not only control/configuration state.

## Negative and failure tests

Run disruptive cases only in an isolated lab with rollback prepared.

{negative_tests}
{len(protocol.test_focus) + 1}. Remove or interrupt one required lower-layer
dependency and confirm the failure is detected with a useful cause.
{len(protocol.test_focus) + 2}. Restore the dependency and verify bounded
recovery without stale state.
{len(protocol.test_focus) + 3}. Supply missing or malformed collected data and
confirm automation returns ERROR, never a success-shaped empty result.

## Security tests

1. Verify peer/server identity instead of trusting reachability alone.
2. Test valid and invalid authentication where the protocol supports it.
3. Verify unauthorized sources, operations, or routes are rejected.
4. Confirm secrets and sensitive payloads are absent from logs and reports.
5. Test replay, downgrade, spoofing, or injection protection where applicable.
6. Validate rate, prefix, session, payload, and resource limits.

## Troubleshooting workflow

1. Record expected and observed behavior, time, scope, and recent changes.
2. Prove every required lower layer from physical connectivity upward.
3. Compare both peers/endpoints, including timers, identity, policy, and MTU.
4. Compare control/session state with actual forwarding or application results.
5. Inspect counters/logs and a bounded capture before clearing state.
6. Reproduce one controlled failure in a lab.
7. Correct the root cause and add a regression fixture/test.

## Python catalog example

```python
from network_course.protocol_catalog import find_protocol

protocol = find_protocol({protocol.name!r})
print(protocol.to_dict())
assert {primary_layer} in protocol.layers
```

## Automation result example

```json
{{
  "protocol": "{protocol.name}",
  "check_id": "{slug.upper()}-001",
  "device": "lab-device-01",
  "expected": "value from approved intent",
  "observed": "normalized collected value",
  "status": "PASS",
  "evidence": "outputs/run-id/device/check.json"
}}
```

Allowed outcomes should be `PASS`, `FAIL`, `ERROR`, and `SKIP` with a reason.
Connection or parser failure is `ERROR`; observed state violating intent is
`FAIL`.

## Lab completion checklist

- [ ] Draw the protocol's encapsulation and peer relationship.
- [ ] Identify required lower-layer dependencies.
- [ ] Capture or collect normal state.
- [ ] Convert observations into structured fields.
- [ ] Implement intent assertions for every validation focus.
- [ ] Run at least one negative and one recovery test.
- [ ] Verify security controls and secret redaction.
- [ ] Save sanitized evidence and document the root cause of failures.
"""


def render_index(entries: list[tuple[Protocol, Path]]) -> str:
    sections = []
    for layer in range(1, 8):
        rows = []
        for protocol, relative_path in entries:
            if min(protocol.layers) != layer:
                continue
            layer_text = ", ".join(str(item) for item in protocol.layers)
            rows.append(
                f"| [{protocol.name}]({relative_path.as_posix()}) | "
                f"{layer_text} | {protocol.purpose} |"
            )
        sections.append(
            f"## Layer {layer} - {LAYER_NAMES[layer]}\n\n"
            "| Protocol | OSI layer(s) | Purpose |\n"
            "|---|---|---|\n"
            + "\n".join(rows)
        )

    return """# Individual Protocol Notes

This directory contains one generated learning and testing file for every
protocol or technology in `network_course/protocol_catalog.py`. Cross-layer
protocols are stored under their lowest/primary OSI layer and list all relevant
layers in their file.

Do not edit generated protocol files directly. Update the catalog or
`tools/generate_protocol_notes.py`, then run:

```powershell
python -m tools.generate_protocol_notes
```

""" + "\n\n".join(sections) + "\n"


def main() -> int:
    entries: list[tuple[Protocol, Path]] = []
    expected_files: set[Path] = set()

    for protocol in PROTOCOLS:
        layer = min(protocol.layers)
        relative_path = Path(f"layer-{layer}") / f"{slugify(protocol.name)}.md"
        target = OUTPUT_DIR / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_protocol(protocol), encoding="utf-8")
        entries.append((protocol, relative_path))
        expected_files.add(target)

    for existing in OUTPUT_DIR.glob("layer-*/*.md"):
        if existing not in expected_files:
            existing.unlink()

    (OUTPUT_DIR / "README.md").write_text(render_index(entries), encoding="utf-8")
    print(f"Generated {len(entries)} protocol files under {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
