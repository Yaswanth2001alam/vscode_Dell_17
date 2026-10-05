# 3. Python and Data Engineering for Networks

## 3.1 Python skills in learning order

1. Values and types: `str`, `int`, `float`, `bool`, `None`.
2. Collections: `list`, `tuple`, `dict`, `set`.
3. Control flow: `if`, `for`, `while`, comprehensions.
4. Functions: parameters, return values, scope, pure functions.
5. Files and formats: text, CSV, JSON, YAML.
6. Exceptions: specific errors, cleanup, useful context.
7. Modules/packages, virtual environments, dependencies.
8. Classes, data classes, protocols/interfaces, type hints.
9. Logging, command-line interfaces, configuration.
10. Testing, mocking, concurrency, packaging, CI.

Prefer small functions that transform explicit inputs into explicit outputs.
Keep device I/O separate from parsing and policy. Then policy can be tested
without routers.

## 3.2 Address handling

Never manipulate addresses with string splitting when the standard `ipaddress`
module can enforce correctness:

```python
from ipaddress import ip_interface, ip_network

uplink = ip_interface("192.0.2.1/31")
assert str(uplink.network) == "192.0.2.0/31"
assert uplink.ip in ip_network("192.0.2.0/24")
```

Test IPv4 and IPv6, invalid values, boundaries, overlapping prefixes, duplicate
addresses, point-to-point `/31` or `/127`, host routes, and membership.

## 3.3 Data formats

- **JSON:** interoperable, strict, no comments, common for APIs.
- **YAML:** readable inventories but indentation and implicit types require
  care. Use a safe loader and schema validation.
- **CSV:** good for flat tables, poor for nested topology.
- **XML:** used heavily by NETCONF and YANG encodings; namespaces matter.
- **TOML:** useful for application/project configuration.

Parsing a file proves syntax only. Validate required fields, allowed values,
uniqueness, cross-references, address relationships, and business rules.

Example inventory principles:

- stable device ID separate from display hostname;
- explicit platform/OS and connection method;
- sites, roles, tags, and groups for selection;
- secrets referenced by environment/vault key, never stored;
- interfaces and peers cross-validated in both directions;
- version the schema and reject unknown incompatible versions.

## 3.4 Exceptions and results

Catch an exception only when you can add context, recover, or convert it into a
domain-specific error. Never use `except Exception: pass`.

Useful outcome categories:

- `PASS`: collected state meets intent;
- `FAIL`: collected state contradicts intent;
- `ERROR`: the check could not run (connection/parser/API problem);
- `SKIP`: intentionally not applicable with a recorded reason.

An empty neighbor list must not silently mean healthy. It may mean no neighbors
are expected, all are missing, the command failed, or parsing failed.

## 3.5 Types and data classes

Types document contracts and catch mistakes before a change reaches a device.
Data classes are useful for inventory and results:

```python
from dataclasses import dataclass
from typing import Literal

Status = Literal["PASS", "FAIL", "ERROR", "SKIP"]

@dataclass(frozen=True)
class Check:
    name: str
    status: Status
    expected: object
    observed: object
    detail: str = ""
```

Use `frozen=True` for immutable facts where appropriate. Do not force all API
data into one giant class; model the stable fields required by your intent.

## 3.6 Logging

Use `logging`, not scattered `print`, for operational tools. Include timestamp,
level, run/correlation ID, device, operation, duration, and result. Prefer JSON
or key-value output for machine ingestion.

Never log:

- passwords, tokens, private keys, SNMP communities, CAKs;
- complete authorization headers;
- unredacted configurations when policy classifies them as sensitive.

Keep user-facing summaries separate from detailed evidence files.

## 3.7 Concurrency

Network I/O is mostly waiting, so a bounded `ThreadPoolExecutor` or an async
library can improve throughput. Production requirements:

- explicit connection/command/overall timeouts;
- maximum workers chosen for AAA, device, jump host, and API capacity;
- per-device result isolation;
- deterministic mapping from future/task to device;
- cancellation/stop conditions;
- rate limiting and retry only for safe transient operations;
- no automatic retry of a non-idempotent change unless designed for it.

Start with five or fewer workers in a lab and measure. "Concurrent" must not
mean "send a change to every device simultaneously."

## 3.8 Configuration generation

Jinja2 is useful when configuration is naturally text. Use:

- `StrictUndefined` so missing variables fail;
- normalized validated data before rendering;
- whitespace control and deterministic ordering;
- golden/snapshot tests plus semantic assertions;
- platform-specific templates only where syntax differs.

Model-driven APIs can avoid text templates by editing structured data, but
schema validation and semantic checks remain necessary.

## 3.9 Parsing operational output

Preference order:

1. structured YANG/OpenConfig telemetry or API data;
2. vendor structured output (JSON/XML);
3. pyATS/Genie/NAPALM normalized getters;
4. TextFSM/TTP templates;
5. carefully tested custom parsing;
6. brittle regex or string splitting only as a last resort.

Parsers should be pure functions. Keep raw evidence for troubleshooting, but
tests and policy should consume normalized records.

Test parser inputs for normal output, empty output, banners, wrapped fields,
alternate release formatting, IPv6, malformed values, and explicit device
errors such as `% Invalid input`.

## 3.10 Git workflow

- One focused branch/change per purpose.
- Never commit `.env`, keys, tokens, captures with sensitive payload, or real
  production backups.
- Review generated configuration and inventory diffs.
- Commit code, tests, sample sanitized data, and directly related docs.
- CI should run formatting, lint, typing, unit tests, dependency/security
  checks, and secret detection before lab deployment.
- Tag or record the exact code revision in every change report.

## 3.11 Engineering structure

A maintainable automation project separates:

```text
inventory/source-of-truth
        -> schema/domain models
        -> intent/policy
        -> renderer or API payload
        -> transport driver
        -> normalized observations
        -> validators
        -> report/evidence
```

Do not combine credentials, connection setup, show commands, regex, policy,
printing, and configuration changes in one loop.

