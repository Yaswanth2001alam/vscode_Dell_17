# 4. Network Automation Libraries and Interfaces

No single library is "best." Choose the highest-level stable interface that
meets the requirement, and isolate transport-specific code behind your own
small functions.

## 4.1 Capability map

| Tool/interface | Best use | Important caution |
|---|---|---|
| `ipaddress` | IPv4/IPv6 math and validation | distinguish address, interface, network |
| `socket` | DNS/TCP reachability fundamentals | TCP success is not protocol health |
| Paramiko | low-level SSH/SFTP control | prompts/channels and host keys are your job |
| Netmiko | multi-vendor CLI commands/config | CLI parsing and prompt timing can vary |
| Scrapli | typed sync/async CLI transports | platform/community driver coverage |
| Nornir | inventory, filtering, task orchestration | tasks/plugins still need safe design |
| Ansible | declarative workflows and modules | idempotency depends on module/platform |
| `requests`/HTTPX | RESTCONF and other REST APIs | TLS, timeouts, status and pagination |
| ncclient | NETCONF RPCs and datastores | XML namespaces, capabilities, locking |
| gNMI clients | streaming/set/get telemetry/config | paths/models and TLS vary |
| Jinja2 | deterministic text configuration | validate data; use StrictUndefined |
| TextFSM/TTP | parse CLI into records | templates are release-sensitive contracts |
| pyATS/Genie | testbeds, parsers, learning/diff | large dependencies; parser coverage varies |
| NAPALM | normalized getters/config workflows | lowest-common-denominator limitations |
| Pydantic | validate/coerce structured models | avoid surprising coercion; version matters |
| pytest | unit/fixture/parameterized tests | mark live tests and prevent accidental runs |
| Batfish | offline config/control-plane analysis | model/vendor feature coverage varies |
| Nornir/Ansible + vault | orchestration at scale | still require approvals and blast-radius limits |

## 4.2 Paramiko

Paramiko is an SSH implementation. Use it when you need control over SSH
transport, channels, SFTP, or a device workflow unsupported by a network CLI
library.

Production rules:

- verify host keys; do not automatically trust unknown keys;
- use key-based authentication or a secret provider;
- set connect, banner, auth, and command/channel timeouts;
- close clients in `finally` or a context manager;
- distinguish authentication, host-key, timeout, and remote-command failures;
- `exec_command` works for servers that support command execution; network
  devices often require an interactive shell with prompt handling.

Paramiko does not understand enable mode, configuration mode, paging, or vendor
prompts. If that is the task, Netmiko/Scrapli is usually better.

## 4.3 Netmiko

Netmiko wraps interactive SSH for network CLIs:

```python
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.0.2.10",
    "username": username,
    "password": password,
}
with ConnectHandler(**device) as connection:
    facts = connection.send_command("show version", read_timeout=30)
    output = connection.send_config_set(
        ["interface Loopback123", "description AUTOMATION-LAB"]
    )
```

Core methods include `send_command` (prompt/pattern-aware),
`send_command_timing` (timing-driven interactions), `send_config_set`, file
transfer helpers, and save operations. Use the correct `device_type`.

Safe pattern:

1. validate input and resolve device selection;
2. preview generated commands;
3. connect with explicit timeouts;
4. identify the device (hostname/serial) before changing it;
5. collect backup and pre-checks;
6. enter configuration through the library;
7. detect CLI errors in output;
8. collect post-checks and save only after success;
9. close the session and write a per-device result.

Do not assume that receiving a prompt means every command succeeded.

## 4.4 Scrapli

Scrapli provides sync/async transports, platform drivers, response objects, and
configuration operations. Its strict host-key behavior and structured response
handling can be useful for robust applications. Community platform definitions
extend vendor support.

Check `response.failed` and `response.result`; configure privilege levels and
timeouts explicitly. Use async only when the entire call chain and operational
limits are designed for it.

## 4.5 Nornir

Nornir is Python-native orchestration. It loads inventory, filters hosts, and
runs tasks concurrently while preserving per-host results:

```python
from nornir import InitNornir
from nornir.core.task import Result, Task

def verify_role(task: Task) -> Result:
    role = task.host.data.get("role")
    return Result(host=task.host, result=role, failed=role is None)

nr = InitNornir(config_file="config.yaml")
leafs = nr.filter(role="leaf")
result = leafs.run(task=verify_role)
```

Nornir itself does not provide every connection/config/parser behavior. Plugins
such as `nornir_netmiko`, `nornir_scrapli`, `nornir_napalm`, inventory plugins,
and output processors provide integrations.

Inspect `MultiResult` and every host result. A task exception on one host must
not be flattened into an apparently successful global run.

## 4.6 Ansible

Ansible playbooks express tasks and desired state. Network modules often use a
controller-side connection (`network_cli`, `netconf`, or HTTP API). Important
features include inventory groups, variables, templates, roles, check mode,
diffs, tags, serial batches, handlers, and vault integrations.

Prefer resource modules and structured arguments over raw CLI commands. Verify
that the selected module actually supports check mode and idempotency on the
target platform. Use `serial` and explicit failure percentages to control blast
radius. Keep validation and rollback tasks in the workflow.

## 4.7 NETCONF and YANG

NETCONF is an XML-based RPC protocol, commonly over SSH port 830. It exposes
datastores and capabilities rather than simulating a terminal.

Key operations:

- `<get>`: configuration and state;
- `<get-config>`: configuration from a datastore;
- `<edit-config>`: modify a target datastore;
- `<validate>`, `<commit>`, confirmed commit, `<discard-changes>`;
- `<lock>`/`<unlock>` to coordinate edits;
- subscriptions/notifications where supported.

Datastores may include running, candidate, startup, and operational concepts.
Support is capability-driven; inspect server capabilities instead of assuming.

YANG defines schema: containers, lists with keys, leaves, types, constraints,
identities, RPCs/actions, and notifications. Namespaces in XML are mandatory and
are a frequent source of empty filters or rejected edits.

Safe candidate workflow:

```text
connect + verify host key
-> inspect capabilities
-> lock candidate
-> edit candidate
-> validate
-> confirmed commit with rollback timer
-> operational post-check
-> confirm commit
-> unlock
```

If any operation fails, report the NETCONF error tag/path/message. Confirmed
commit is not a replacement for an independent rollback design.

## 4.8 RESTCONF

RESTCONF maps YANG data to HTTP resources, commonly using JSON or XML. Typical
operations:

- `GET`: retrieve resource;
- `POST`: create/invoke as defined;
- `PUT`: replace/create target resource;
- `PATCH`: partial update (media type/semantics matter);
- `DELETE`: remove.

Use the server's documented base path and YANG-qualified resource names. Send
and accept the correct YANG media types, for example
`application/yang-data+json`.

Always:

- validate TLS certificates and hostnames;
- set a timeout;
- call `raise_for_status()` or explicitly handle status codes;
- handle `401/403`, `404`, `409/412`, `415`, `429`, and `5xx` differently;
- use ETags/conditional requests where supported to avoid lost updates;
- handle pagination and rate limits;
- redact authorization headers and payload secrets.

## 4.9 gNMI and streaming telemetry

gNMI is a gRPC-based interface for capabilities, get, set, and subscribe. It is
commonly paired with OpenConfig models.

Subscription modes include once, poll, and stream, with sample, on-change, and
target-defined behavior. A collector must handle timestamps, paths, deletes,
sync responses, reconnection, duplicate/out-of-order data, backpressure, and
schema/model versions.

Streaming telemetry is better than polling for many high-frequency signals, but
it does not eliminate data quality or capacity engineering.

## 4.10 SNMP, syslog, and telemetry

SNMP remains useful for counters and compatibility. Prefer SNMPv3 authentication
and privacy, restricted views, and management-plane ACLs. Counter handling must
consider 32/64-bit width, rollover, discontinuities, interface index changes,
and rates derived from timestamps.

Syslog is event-oriented and may be lossy over UDP. Normalize device time with
NTP, include host and sequence where available, and route security logs to
protected storage. Traps/syslog should trigger investigation, not serve as the
only source of current truth.

## 4.11 Parsing libraries

**TextFSM** uses templates with value definitions and state transitions.
`ntc-templates` supplies community templates. Pin/test template versions because
field names can change.

**TTP** uses templates that resemble the text being parsed and can group nested
results.

**Genie** parsers produce deeply structured dictionaries for supported
platform/command combinations. Treat missing parser support as an explicit
error or documented raw fallback, never silent success.

**NAPALM** getters normalize facts, interfaces, LLDP, BGP, and other state
across supported drivers. Platform-specific features still require extensions.

## 4.12 Choosing an interface

Use this decision sequence:

1. Is a stable, authenticated, model-driven interface available? Prefer it.
2. Is a normalized tested library available for the required feature?
3. Is a vendor structured output supported?
4. Is CLI the only practical interface? Use a network-aware CLI library and a
   maintained parser.
5. Is the operation safe and idempotent through that interface?
6. Can the result be independently verified through operational state?

Do not rewrite a reliable vendor/resource module solely to use a fashionable
protocol. Conversely, do not use screen scraping when supported YANG data gives
a stable schema.

