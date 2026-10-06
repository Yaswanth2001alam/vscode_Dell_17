# Network Engineer Knowledge Base

This folder organizes the network-engineering material in `vscode_Dell_17-1`
without moving or deleting the original files.

Generated on October 5, 2026.

## Start here

1. Read [01-LEARNING-PATH.md](01-LEARNING-PATH.md).
2. Use [02-REPOSITORY-REVIEW.md](02-REPOSITORY-REVIEW.md) to understand what is
   already in the repository.
3. Use [03-CONCEPT-MAP.md](03-CONCEPT-MAP.md) as the technical index.
4. Follow [04-AUTOMATION-RUNBOOK.md](04-AUTOMATION-RUNBOOK.md) before changing
   a lab or device.
5. Follow [05-TROUBLESHOOTING-RUNBOOK.md](05-TROUBLESHOOTING-RUNBOOK.md) during
   an incident or lab failure.
6. Review [06-SAFETY-AND-SECRETS.md](06-SAFETY-AND-SECRETS.md) before sharing,
   committing, or reusing any inventory.
7. Use [07-PROJECT-ROADMAP.md](07-PROJECT-ROADMAP.md) to turn the learning
   material into portfolio-quality projects.

## Folder layout

| Path | Purpose |
|---|---|
| `catalog/` | Complete inventory of network-relevant files, classifications, and review status |
| `library/` | Safe copies of reusable code, notebooks, notes, and configuration examples |
| `templates/` | Clean starting templates for inventories, changes, and incident notes |
| `build_knowledge_base.py` | Rebuilds the catalog and curated library from tracked repository files |

The generated library uses these domains:

| Domain | Includes |
|---|---|
| `01-network-fundamentals` | IP addressing, subnetting, TCP/UDP, DNS, HTTP/TLS, Wi-Fi |
| `02-routing-and-switching` | BGP, OSPF, VLANs, LLDP/CDP, routes, interfaces |
| `03-labs-and-device-automation` | EVE-NG, pyATS/Genie, Netmiko, Ansible, eAPI |
| `04-observability-and-troubleshooting` | Ping, packet analysis, Wireshark, health checks, monitoring |
| `05-inventory-and-data` | YAML/JSON/CSV inventories, testbeds, structured device data |
| `06-testing-and-quality` | pytest, read-only verification, validation, fixtures |
| `07-ai-assisted-networking` | Gemini/RAG and AI-assisted network analysis |
| `08-reference-and-uncategorized` | Relevant material that needs manual classification |

## Rebuild

From the repository root:

```powershell
python .\Network-Engineer-Knowledge-Base\build_knowledge_base.py
```

The rebuild is deterministic. It replaces only the generated `catalog` and
`library` directories. It does not alter source material elsewhere in the
repository.

## Important limitation

This is a repository-content review, not a live-device health assessment. Live
device state must be collected from the actual lab or production environment
with approved read-only commands before drawing operational conclusions.
