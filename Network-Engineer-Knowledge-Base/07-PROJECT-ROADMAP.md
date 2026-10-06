# Project Roadmap

## Priority 1: Consolidate the three-router lab

Use `EVE-NG_3_Router_Automation` as the main portfolio project.

- Keep one inventory schema.
- Add schema validation.
- Add expected-state assertions for every scenario.
- Add rollback commands and rollback verification.
- Add sanitized sample reports.
- Add a topology diagram.
- Run linting, typing, unit tests, and read-only lab tests.

## Priority 2: Strengthen BGP validation

- Validate expected neighbors, remote AS values, and minimum prefix counts.
- Support IOS-XE parser variations.
- Distinguish collection failure from an empty BGP table.
- Remove broad exception handling where framework-specific exceptions exist.
- Add JSON schema/version fields to reports.
- Reconfirm all documentation metrics from current test output.

## Priority 3: Build a unified health-check CLI

Combine the best read-only checks:

- management reachability;
- interfaces and errors;
- OSPF and BGP;
- route and reachability matrix;
- CPU, memory, logs, NTP, and configuration drift.

Output terminal, JSON, and optional CSV summaries with meaningful exit codes.

## Priority 4: Clean the learning workspace

- Remove committed caches and compiled files.
- Move generated results to ignored output directories.
- Keep one canonical notebook where duplicates exist.
- Extract reusable notebook logic into modules.
- Archive old backups outside the source tree.
- Sanitize or remove credentials and sensitive evidence.

## Priority 5: Add CI

CI should run only offline-safe checks:

- formatting and linting;
- type checking;
- unit tests;
- notebook syntax/metadata validation;
- YAML/JSON validation;
- secret scanning.

Live-device tests should require an explicitly configured private runner and
must default to read-only behavior.
