from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import lab_automation as lab


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs" / "verification"


def _safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", value).strip("_").lower()


def _save(check_name: str, results: list[dict[str, Any]]) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = OUTPUT_DIR / f"{timestamp}_{_safe_name(check_name)}.json"
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return path


def _selected_devices(device_names: list[str] | None = None) -> list[dict[str, Any]]:
    lab.load_env_file()
    inventory = lab.load_inventory()
    return lab.select_devices(inventory, device_names)


def verify(
    check_name: str,
    commands: list[str],
    device_names: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Run read-only IOS show commands and save/print their raw output."""
    devices = _selected_devices(device_names)
    results = lab.execute_parallel(
        devices, lambda device: lab.run_show_commands(device, commands)
    )

    for result in results:
        print(f"\n{'=' * 20} {result['device']} {'=' * 20}")
        if "error" in result:
            print(f"ERROR: {result['error']}")
            continue
        for command, output in result["commands"].items():
            print(f"\n{result['device']}# {command}")
            print(output or "<no output>")

    path = _save(check_name, results)
    print(f"\nSaved report: {path}")
    return results


def verify_management_reachability(
    device_names: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Test TCP/22 reachability without changing or logging into routers."""
    devices = _selected_devices(device_names)
    results = lab.execute_parallel(devices, lab.run_precheck)
    for result in results:
        print(
            f"{result['device']} ({result['host']}): "
            f"SSH {result['ssh']}"
        )
    path = _save("management_reachability", results)
    print(f"\nSaved report: {path}")
    return results


def verify_ping_matrix(
    device_names: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Ping every router loopback from every selected router."""
    lab.load_env_file()
    inventory = lab.load_inventory()
    devices = lab.select_devices(inventory, device_names)
    targets = [device["router_id"] for device in inventory.values()]
    commands = [f"ping {target} repeat 5 timeout 1" for target in targets]
    return verify("loopback_ping_matrix", commands, [d["name"] for d in devices])


def summarize_protocols(
    device_names: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Show a compact OSPF/BGP status summary and save the supporting output."""
    results = verify(
        "protocol_summary",
        ["show ip ospf neighbor", "show ip bgp summary"],
        device_names,
    )
    print("\nProtocol summary")
    print("-" * 72)
    for result in results:
        if "error" in result:
            print(f"{result['device']}: connection failed")
            continue
        ospf = result["commands"]["show ip ospf neighbor"]
        bgp = result["commands"]["show ip bgp summary"]
        ospf_full = sum("FULL/" in line for line in ospf.splitlines())
        bgp_peers = [
            line
            for line in bgp.splitlines()
            if re.match(r"^\d+\.\d+\.\d+\.\d+\s+", line)
        ]
        established = sum(
            line.split()[-1].isdigit() for line in bgp_peers if line.split()
        )
        print(
            f"{result['device']}: OSPF FULL={ospf_full}, "
            f"BGP Established={established}/{len(bgp_peers)}"
        )
    return results
