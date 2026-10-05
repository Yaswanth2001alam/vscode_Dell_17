# 5. Testing, Security, and Production Operations

## 5.1 Define intent as testable statements

Weak check: "run `show ip bgp summary`."

Strong checks:

- Neighbor `192.0.2.2` in VRF `blue` is Established.
- Remote AS is 64501.
- IPv4 unicast accepted prefixes are between 1 and 500.
- Prefix `203.0.113.0/24` is accepted with local preference 200 and community
  `64500:100`.
- Default route is not accepted from this neighbor.
- The selected next hop resolves and a data-plane probe succeeds.

Each check needs device, scope, expected value/range, observation, status, and
evidence. Boolean-only results are inadequate for diagnosis.

## 5.2 Unit tests

Unit tests must not contact routers. Test:

- inventory and schema validation;
- IPv4/IPv6 calculations and overlap detection;
- configuration/payload generation;
- pure parsers using sanitized fixtures;
- protocol policies and thresholds;
- report serialization;
- device-selection and dry-run logic;
- exception classification and redaction.

Use boundary-value and parameterized tests. For a prefix threshold of 1..500,
test 0, 1, 500, and 501, not only 100.

## 5.3 Mocks and contract tests

Mock at the transport boundary, not every internal function. A fake connector
should return representative raw/structured device responses or raise specific
timeouts/authentication errors.

Contract fixtures should include:

- normal healthy response;
- empty but valid response;
- partial/missing field;
- malformed response;
- permission denied;
- command/API error;
- alternate platform/release output;
- stale/unexpected neighbor;
- IPv4 and IPv6.

Mocks prove your reaction to known contracts; they do not prove compatibility
with real devices.

## 5.4 Integration and system tests

Mark tests that require a lab and require an explicit opt-in such as
`RUN_LIVE_TESTS=1`. Default test discovery must be offline and safe.

Integration sequence:

1. deploy a known virtual topology;
2. wait for boot/readiness with bounded timeout;
3. verify baseline;
4. apply intent;
5. verify configuration and operational state;
6. generate traffic or active probes;
7. inject one controlled fault;
8. verify detection/convergence;
9. restore and verify recovery;
10. archive sanitized evidence and destroy/reset the lab.

## 5.5 Protocol test catalog

### Physical and interfaces

- Admin/oper state, expected speed/duplex/media.
- MTU with small and near-MTU payloads.
- Input/output errors, CRC, discards, carrier changes.
- Optics power/temperature against platform thresholds.
- Description and peer mapping.
- Failure and recovery time.

### LLDP/LACP/STP

- Expected LLDP chassis/port and no unauthorized neighbor.
- LACP partner, key, member flags, minimum links, member failure.
- Intended STP root, port roles, protections, topology-change stability.

### OSPF/IS-IS/BFD

- Exact expected adjacency set and no unexpected neighbor.
- State, level/area, interface, timers, authentication, BFD binding.
- Expected topology prefixes and no forbidden leaks.
- Route count/LSDB stability and convergence on link loss.
- RIB/FIB consistency and data-plane path.

### BGP

- FSM, AS, router ID, AFI/SAFI, source, capabilities.
- Accepted/advertised count ranges and maximum-prefix.
- Required and forbidden prefixes.
- Next-hop reachability and attributes/community policy.
- Withdrawal and failover behavior.
- Route-reflector and RPKI policy behavior.

### MACsec/IPsec

- Correct secure association and algorithms/policy.
- Bidirectional protected packet counters.
- No replay/integrity errors.
- Rekey without excess loss.
- Plaintext/untrusted/wrong-key rejection.
- MTU and fragmentation behavior.

### Services and applications

- DNS positive/negative answer and latency.
- NTP sync/offset and source.
- AAA allowed and denied authorization.
- TLS identity/expiry and API schema.
- End-to-end transaction, not only ping.

## 5.6 Pre-checks and stop conditions

Pre-checks should include:

- exact device identity, site, role, serial/model/image;
- management and console/rollback availability;
- current configuration backup/checkpoint;
- redundancy and protocol health;
- CPU, memory, interface errors, alarms;
- expected active traffic/path and maintenance constraints;
- configuration lock or competing change detection;
- available storage and commit/checkpoint capacity;
- NTP/time correctness for evidence.

Stop if identity differs, backup fails, baseline is already unhealthy without an
approved exception, redundancy is unavailable, or the proposed diff exceeds
the approved scope.

## 5.7 Deployment strategies

- **Dry-run:** display commands/payload and semantic intent.
- **Canary:** one low-risk representative device.
- **Serial/batched:** proceed only after each batch passes.
- **Blue/green:** build and validate alternate infrastructure, then shift.
- **Maintenance mode:** drain or raise IGP/BGP preference before work.
- **Confirmed commit:** auto-revert unless confirmed after validation.

Separate "push accepted" from "service healthy." Define maximum failure count,
latency/loss threshold, adjacency/prefix variance, and rollback decision before
starting.

## 5.8 Rollback

A rollback is more than loading an old text file. It must account for:

- configuration syntax and dependencies;
- stateful protocols and convergence;
- schema/database migrations in controllers;
- secrets/certificates;
- out-of-band access;
- downstream systems that reacted to the first change.

Test rollback in the lab. Save checkpoint IDs, not just filenames. After
rollback, run the same operational and data-plane checks used after deployment.

## 5.9 Security baseline

- Use per-user/service identities and least privilege.
- Store secrets in environment variables for labs and an approved secret
  manager in production.
- Rotate credentials and use short-lived tokens/certificates where possible.
- Verify SSH host keys and TLS certificates.
- Restrict management interfaces by network and AAA policy.
- Prefer NETCONF/RESTCONF/SSH encryption; avoid Telnet/HTTP/SNMPv1/v2c.
- Validate all inventory and API input.
- Escape/structure commands; do not concatenate untrusted input into shell or
  device commands.
- Pin/scan dependencies and container images.
- Sign/review changes and protect CI credentials.
- Redact evidence and apply retention/access controls.

Never place credentials in sample inventories. Environment variables are
acceptable for a personal lab but are not a complete enterprise secret
management strategy.

## 5.10 Observability

### Logs

Record run ID, code revision, user/service identity, device, action, duration,
status, and error category. Do not log secrets.

### Metrics

Useful metrics:

- task success/error/timeout duration;
- connection/auth failures;
- neighbor state and flap count;
- prefix count and route churn;
- interface utilization/error/discard rate;
- configuration drift count;
- telemetry age;
- change failure and rollback rates.

### Traces

Trace a workflow across inventory lookup, credential retrieval, device/API
calls, validation, and report storage. Correlation IDs should connect all
events for one run.

Alert on user impact and actionable symptoms, with deduplication and runbook
links. Avoid one alert per poll/device if a common dependency failed.

## 5.11 CI/CD pipeline

A safe automation pipeline can contain:

```text
format/lint
-> type check
-> unit tests
-> schema + policy checks
-> secret/dependency scan
-> generate and publish candidate diff
-> virtual lab integration
-> manual approval
-> canary
-> automated health gate
-> batches
-> post-change observation
```

Production credentials should only become available to the protected deployment
stage. Pull-request tests should run with sanitized fixtures.

## 5.12 Troubleshooting method

1. Restate expected and observed behavior.
2. Establish scope: one flow, host, VLAN, site, protocol, or all traffic.
3. Check recent changes and timestamps.
4. Follow the packet hop by hop in both directions.
5. Compare control plane, forwarding plane, counters, logs, and capture.
6. Change one variable in a lab or use a bounded diagnostic.
7. Record evidence before clearing counters or restarting.
8. Fix root cause and add a regression test.

Automation should improve this process by collecting consistent evidence, not
by replacing reasoning with a large command dump.

