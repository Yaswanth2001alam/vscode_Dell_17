from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path


KB_ROOT = Path(__file__).resolve().parent
REPO_ROOT = KB_ROOT.parent
CATALOG_ROOT = KB_ROOT / "catalog"
LIBRARY_ROOT = KB_ROOT / "library"

PRIMARY_ROOTS = (
    "1.Python Learning/Network Coding/",
    "EVE-NG-Network-Automation/",
    "Network-Public/",
)

ADDITIONAL_PATH_MARKERS = (
    "3.Notes/BGP Notes/",
    "3.Notes/PyATS",
    "AI & ML/AI Models Networking",
    "AI & ML/SciPy/Network Engineer",
    "Ansible/",
    "VSCODE-INSPIRON-main/Automation.practice/ospf",
)

NETWORK_TERMS = (
    "network",
    "router",
    "routing",
    "switch",
    "cisco",
    "fortinet",
    "pyats",
    "genie",
    "netmiko",
    "napalm",
    "ansible",
    "vlan",
    "bgp",
    "ospf",
    "eigrp",
    "mpls",
    "firewall",
    "subnet",
    "wireshark",
    "packet",
    "tcp",
    "udp",
    "dns",
    "dhcp",
    "snmp",
    "telemetry",
    "eve-ng",
    "inventory",
    "interface",
    "ping",
    "testbed",
    "sonic",
)

TEXT_EXTENSIONS = {
    "",
    ".csv",
    ".example",
    ".gitignore",
    ".ini",
    ".ipynb",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".txt",
    ".yaml",
    ".yml",
}

BINARY_OR_EVIDENCE_EXTENSIONS = {
    ".db",
    ".docx",
    ".har",
    ".jpeg",
    ".jpg",
    ".log",
    ".mp3",
    ".mp4",
    ".pcap",
    ".pdf",
    ".png",
    ".pyc",
    ".wav",
    ".xlsx",
    ".xml",
}

GENERATED_MARKERS = (
    "/__pycache__/",
    "/.ipynb_checkpoints/",
    "/.pytest_cache/",
    "/ping_results/",
    "/outputs/",
    "/back up code/",
    "/backup",
    "system_report",
)

DUPLICATE_MARKERS = (
    " copy",
    "-checkpoint",
    "_draft",
    "draft.",
    "cells.extra",
)

SECRET_ASSIGNMENT_PATTERN = re.compile(
    r"""(?ix)
    (?:password|passwd|secret|token|api[_-]?key)
    \s*[:=]\s*
    \\?["']?
    ([^\s\\"',}]+)
    """
)

SAFE_SECRET_MARKERS = (
    "${",
    "%env{",
    "<openrouter_api_key>",
    "<your",
    "changeme",
    "env(",
    "example",
    "getenv",
    "os.environ",
    "placeholder",
    "replace-with",
)


@dataclass
class CatalogEntry:
    source_path: str
    category: str
    status: str
    reason: str
    extension: str
    size_bytes: int
    concepts: str
    notebook_headings: str
    library_path: str = ""


def git_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )
    return [
        item.decode("utf-8", errors="replace").replace("\\", "/")
        for item in result.stdout.split(b"\0")
        if item
    ]


def is_network_relevant(relative_path: str) -> bool:
    normalized = relative_path.replace("\\", "/")
    lowered = normalized.lower()
    if normalized.startswith("Network-Engineer-Knowledge-Base/"):
        return False
    if normalized.startswith(PRIMARY_ROOTS):
        return True
    if any(marker.lower() in lowered for marker in ADDITIONAL_PATH_MARKERS):
        return True
    filename = Path(normalized).name.lower()
    return any(term in filename for term in NETWORK_TERMS)


def classify(relative_path: str) -> str:
    lowered = relative_path.lower()

    rules = (
        (
            "07-ai-assisted-networking",
            ("gemini", "rag", "ai models networking", "open_router"),
        ),
        (
            "06-testing-and-quality",
            ("pytest", "/test_", "testbed", "fixture", "verification"),
        ),
        (
            "04-observability-and-troubleshooting",
            (
                "wireshark",
                "packet",
                "pcap",
                "tcpdump",
                "monitor",
                "ping",
                "health",
                "capture",
                "dns_testing",
                "speed_test",
                "wifi_status",
                "system_report",
            ),
        ),
        (
            "02-routing-and-switching",
            (
                "bgp",
                "ospf",
                "eigrp",
                "vlan",
                "lldp",
                "routing",
                "route",
                "switch",
                "asic",
                "sonic",
            ),
        ),
        (
            "05-inventory-and-data",
            ("inventory", "devices.yaml", "testbed.yaml", "yaml_files"),
        ),
        (
            "03-labs-and-device-automation",
            (
                "eve-ng",
                "automation",
                "pyats",
                "genie",
                "netmiko",
                "ansible",
                "eapi",
                "connect_router",
                "push_config",
            ),
        ),
        (
            "01-network-fundamentals",
            (
                "subnet",
                "ipaddress",
                "tcp",
                "udp",
                "dns",
                "tls",
                "http",
                "interface",
                "device_information",
            ),
        ),
    )

    for category, terms in rules:
        if any(term in lowered for term in terms):
            return category
    return "08-reference-and-uncategorized"


def concepts_for(relative_path: str, text: str) -> list[str]:
    haystack = f"{relative_path}\n{text[:200_000]}".lower()
    concept_rules = {
        "AI/RAG": ("gemini", "rag", "file search"),
        "Ansible": ("ansible",),
        "ARP": (" arp", "show arp"),
        "BGP": ("bgp",),
        "CDP/LLDP": ("cdp", "lldp"),
        "DNS": ("dns", "nslookup"),
        "EVE-NG": ("eve-ng", "eve_ng"),
        "Genie": ("genie",),
        "HTTP/TLS": ("http", "tls", "ssl"),
        "Interfaces": ("interface", "show ip int"),
        "Inventory": ("inventory", "testbed"),
        "Netmiko": ("netmiko",),
        "OSPF": ("ospf",),
        "Packet analysis": ("wireshark", "pcap", "tcpdump", "scapy"),
        "Ping/reachability": ("ping", "reachability"),
        "pyATS": ("pyats",),
        "pytest": ("pytest",),
        "Routing": ("routing", "route table", "show ip route"),
        "SNMP/telemetry": ("snmp", "telemetry"),
        "Subnetting": ("subnet", "ipaddress", "prefixlen"),
        "TCP/UDP": ("tcp", "udp"),
        "VLAN": ("vlan",),
        "YAML/JSON/CSV": ("yaml", "json", "csv"),
    }
    return [
        concept
        for concept, markers in concept_rules.items()
        if any(marker in haystack for marker in markers)
    ]


def notebook_headings(text: str) -> list[str]:
    try:
        notebook = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return []

    headings: list[str] = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        source = "".join(cell.get("source", []))
        for line in source.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                heading = stripped.lstrip("#").strip()
                if heading and heading not in headings:
                    headings.append(heading)
            if len(headings) >= 12:
                return headings
    return headings


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def contains_likely_secret(text: str) -> bool:
    for line in text.splitlines():
        lowered = line.lower()
        if any(marker in lowered for marker in SAFE_SECRET_MARKERS):
            continue
        if SECRET_ASSIGNMENT_PATTERN.search(line):
            return True
    return False


def review_file(relative_path: str) -> CatalogEntry:
    source = REPO_ROOT / Path(relative_path)
    extension = source.suffix.lower()
    normalized = relative_path.replace("\\", "/")
    lowered = normalized.lower()
    category = classify(normalized)
    status = "copied"
    reason = "Reusable tracked text source"
    text = ""
    headings: list[str] = []

    if not source.is_file():
        size = 0
        status = "reference-only"
        reason = "Tracked directory or Git submodule reference"
    else:
        size = source.stat().st_size

    if status == "reference-only":
        pass
    elif extension in BINARY_OR_EVIDENCE_EXTENSIONS:
        status = "reference-only"
        reason = "Binary, captured evidence, generated output, or office document"
    elif extension not in TEXT_EXTENSIONS:
        status = "reference-only"
        reason = f"Unsupported curated-library extension: {extension or '[none]'}"
    elif any(marker in lowered for marker in GENERATED_MARKERS):
        status = "reference-only"
        reason = "Generated result, backup, cache, or operational evidence"
    elif any(marker in lowered for marker in DUPLICATE_MARKERS):
        status = "reference-only"
        reason = "Duplicate, checkpoint, or draft variant"
    elif size > 2_000_000:
        status = "reference-only"
        reason = "Text source is larger than the 2 MB curated-library limit"
    else:
        text = read_text(source)
        if contains_likely_secret(text):
            status = "sensitive-review"
            reason = "Likely embedded credential or secret; review and sanitize"
        elif extension == ".ipynb":
            headings = notebook_headings(text)

    if (
        source.is_file()
        and not text
        and extension in TEXT_EXTENSIONS
        and size <= 2_000_000
    ):
        text = read_text(source)

    concepts = concepts_for(normalized, text)
    return CatalogEntry(
        source_path=normalized,
        category=category,
        status=status,
        reason=reason,
        extension=extension or "[none]",
        size_bytes=size,
        concepts="; ".join(concepts),
        notebook_headings="; ".join(headings),
    )


def reset_generated_directories() -> None:
    for path in (CATALOG_ROOT, LIBRARY_ROOT):
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True)


def copy_entry(entry: CatalogEntry) -> None:
    if entry.status != "copied":
        return
    source = REPO_ROOT / Path(entry.source_path)
    destination = LIBRARY_ROOT / entry.category / Path(entry.source_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    entry.library_path = destination.relative_to(KB_ROOT).as_posix()


def write_csv(entries: list[CatalogEntry]) -> None:
    destination = CATALOG_ROOT / "network-content-catalog.csv"
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_path",
                "category",
                "status",
                "reason",
                "extension",
                "size_bytes",
                "concepts",
                "notebook_headings",
                "library_path",
            ],
        )
        writer.writeheader()
        writer.writerows(entry.__dict__ for entry in entries)


def write_json(entries: list[CatalogEntry]) -> None:
    destination = CATALOG_ROOT / "network-content-catalog.json"
    destination.write_text(
        json.dumps(
            [entry.__dict__ for entry in entries],
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def write_summary(entries: list[CatalogEntry]) -> None:
    category_counts = Counter(entry.category for entry in entries)
    status_counts = Counter(entry.status for entry in entries)
    concept_counts: Counter[str] = Counter()
    notable_files: defaultdict[str, list[CatalogEntry]] = defaultdict(list)

    for entry in entries:
        concept_counts.update(
            concept for concept in entry.concepts.split("; ") if concept
        )
        if entry.status == "copied" and len(notable_files[entry.category]) < 12:
            notable_files[entry.category].append(entry)

    lines = [
        "# Generated Network Content Summary",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        f"- Network-relevant tracked files: **{len(entries)}**",
        f"- Files copied into the safe library: **{status_counts['copied']}**",
        f"- Reference-only files: **{status_counts['reference-only']}**",
        f"- Files requiring sensitive-data review: "
        f"**{status_counts['sensitive-review']}**",
        "",
        "## Content by domain",
        "",
        "| Domain | Files |",
        "|---|---:|",
    ]
    lines.extend(
        f"| `{category}` | {count} |"
        for category, count in sorted(category_counts.items())
    )
    lines.extend(
        [
            "",
            "## Most represented concepts",
            "",
            "| Concept | Files |",
            "|---|---:|",
        ]
    )
    lines.extend(
        f"| {concept} | {count} |"
        for concept, count in concept_counts.most_common()
    )
    lines.extend(["", "## Reusable files by domain", ""])

    for category in sorted(notable_files):
        lines.extend([f"### `{category}`", ""])
        lines.extend(
            f"- [{Path(entry.source_path).name}]"
            f"(../{entry.library_path.replace(' ', '%20')}) - "
            f"`{entry.source_path}`"
            for entry in notable_files[category]
        )
        lines.append("")

    lines.extend(
        [
            "## Review queues",
            "",
            "Use `network-content-catalog.csv` to filter:",
            "",
            "- `status=sensitive-review` before publishing or copying material;",
            "- `status=reference-only` for captures, backups, generated evidence, "
            "duplicates, and large files;",
            "- `category=08-reference-and-uncategorized` for manual classification.",
            "",
        ]
    )
    (CATALOG_ROOT / "SUMMARY.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    reset_generated_directories()
    entries = [
        review_file(relative_path)
        for relative_path in git_files()
        if is_network_relevant(relative_path)
    ]
    entries.sort(key=lambda entry: (entry.category, entry.source_path.lower()))

    for entry in entries:
        copy_entry(entry)

    write_csv(entries)
    write_json(entries)
    write_summary(entries)

    status_counts = Counter(entry.status for entry in entries)
    print(f"Cataloged {len(entries)} network-relevant tracked files.")
    print(f"Copied {status_counts['copied']} safe reusable files.")
    print(f"Reference-only: {status_counts['reference-only']}.")
    print(f"Sensitive review: {status_counts['sensitive-review']}.")


if __name__ == "__main__":
    main()
