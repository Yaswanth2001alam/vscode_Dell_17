# Network Automation Runbook

## Before execution

- Confirm the authorized devices and maintenance window.
- Confirm console or out-of-band recovery access.
- Validate the inventory and platform/OS values.
- Load credentials from environment variables or an approved secret manager.
- Confirm command support on the target software version.
- Run unit tests and read-only checks.

## Standard workflow

### 1. Precheck

- Resolve and reach the management address.
- Test the required TCP port.
- Confirm authentication and privilege level.
- Record hostname, platform, version, and serial where permitted.

### 2. Plan

- Render every intended command.
- Show target devices and interfaces.
- Detect conflicting scenarios.
- Require an explicit apply flag for changes.

### 3. Backup

- Save running and startup configuration.
- Capture relevant protocol and interface state.
- Timestamp the files.
- Protect the backup as sensitive data.

### 4. Apply

- Limit concurrency for the lab/environment.
- Set connection and command timeouts.
- Stop per device on a meaningful failure.
- Do not report success when only command transmission succeeded.

### 5. Verify

Use measurable acceptance criteria:

- Interfaces are in expected states.
- OSPF neighbors are FULL.
- BGP peers are Established.
- Expected routes and prefixes are present.
- End-to-end probes succeed.
- Error counters and logs show no introduced fault.

### 6. Save or rollback

Save only after validation. If validation fails, collect evidence and execute
the documented rollback rather than sending unreviewed corrective commands.

## Result schema

Every operation should record:

```json
{
  "timestamp": "ISO-8601",
  "operation": "verify",
  "device": "R1",
  "target": "lab",
  "success": true,
  "commands": [],
  "checks": [],
  "errors": []
}
```

## Framework guidance

- Keep connection logic separate from business logic.
- Keep command generation pure and unit-testable.
- Prefer parsed output; retain raw output for troubleshooting.
- Catch expected framework exceptions narrowly.
- Return explicit failed results rather than empty success-shaped data.
- Use per-device logs and a final aggregate exit code.
