# Python companions for OSI Layers 1-7

Each of the 44 protocol Markdown modules has an executable `.py` companion
beside it with the same filename stem. Existing Markdown and configuration files
are unchanged.

## What these programs do

These are **offline normalized-state validators**, not implementations of
Ethernet, BGP, TLS, DNS, or other wire protocols. They do not connect to routers,
configure devices, capture traffic, or prove service health without collected
observations. Built-in samples demonstrate successful policy checks.

Each companion provides:

- protocol metadata, OSI layers, purpose, transport, and example ports;
- `EXPECTED` teaching intent and `SAMPLE_OBSERVATION`;
- `validate()` and `report()` functions for reuse;
- exact-value, allowed-value, numeric-boundary, and integer checks;
- explicit failures for missing fields and type mismatches;
- JSON output and exit code 0 for pass or 1 for policy failure.

Invalid files or JSON produce an explicit Python error and nonzero exit code.
NaN and Infinity are rejected. No credentials or external dependencies are
required.

## Running examples

From the course directory:

```powershell
python .\protocols\layer-1\ethernet-phy.py
python .\protocols\layer-2\lacp.py
python .\protocols\layer-3\bgp.py
python .\protocols\layer-4\tcp.py
python .\protocols\layer-5\tls.py
python .\protocols\layer-6\asn-1.py
python .\protocols\layer-7\dns.py
```

Validate collected state instead of the sample:

```powershell
python .\protocols\layer-3\bgp.py --input .\observations.json
```

Example BGP observation:

```json
{
  "FSM": "established",
  "prefixes": 42,
  "attributes": "policy-compliant",
  "policy": "applied"
}
```

The strings summarizing attributes/policy must come from independent collector
and policy logic. Do not fill them with optimistic defaults.

## Important limitations

- The inventory contains 44 **catalog entries**, some grouping protocol families
  such as STP/RSTP/MST and FTP/TFTP/SFTP. It does not enumerate every protocol
  ever standardized.
- Expectations are illustrative lab intent. Optic power, MTU, speed, FEC,
  wireless channel, loss, jitter, timers, algorithms, and authentication policy
  must be customized for the actual platform and service.
- DNS TTL is an unsigned cache lifetime, not the IPv4 TTL or IPv6 hop limit.
- BGP prefix counts and protocol counters must be integers.
- MPLS FEC means forwarding equivalence class, not physical-layer forward error
  correction.
- Multi-field symbolic summaries are teaching simplifications; real collectors
  should expose detailed peer, route, cipher, certificate, and policy records.
- Exact comparisons are case-sensitive unless the collector normalizes values.

## Tests and maintenance

```powershell
python -B -m unittest discover -s tests -p test_protocol_python.py -v
```

Tests cover all 44 companions, all seven layers, CLI success/failure, missing
fields, boundaries, type errors, sample isolation, and invalid JSON.

The standalone modules intentionally contain their own small validation engine
so learners can run or copy any single file without imports from the course.
To update that common engine consistently, run:

```powershell
python -B -m tools.harden_protocol_examples
```

This tool reads metadata from the existing companions and rewrites only those
Python companions; it does not regenerate or edit the Markdown notes.
