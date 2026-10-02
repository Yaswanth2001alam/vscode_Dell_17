from __future__ import annotations

import argparse
import ipaddress
import json
import os
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_INVENTORY = BASE_DIR / "inventory.json"
DEFAULT_OUTPUT_DIR = BASE_DIR / "outputs"
SCENARIOS = ("baseline", "ospf", "ebgp", "bgp-only", "ospf-ebgp", "ibgp-rr")


def load_env_file(path: Path = BASE_DIR / ".env") -> None:
    if not path.exists():
        return
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"Invalid .env entry on line {line_number}")
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if not key:
            raise ValueError(f"Missing .env key on line {line_number}")
        os.environ.setdefault(key, value)


def load_inventory(path: Path = DEFAULT_INVENTORY) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    defaults = data.get("defaults", {})
    devices = data.get("devices", {})
    if not devices:
        raise ValueError("Inventory must contain at least one device")

    for name, device in devices.items():
        device["name"] = name
        device["device_type"] = device.get(
            "device_type", defaults.get("device_type", "cisco_ios")
        )
        device["port"] = int(device.get("port", defaults.get("port", 22)))
        device["host"] = os.getenv(f"{name.upper()}_HOST", device["host"])
    validate_inventory(devices)
    return devices


def validate_inventory(devices: dict[str, Any]) -> None:
    required = {"host", "router_id", "loopback", "asn", "links"}
    for name, device in devices.items():
        missing = required - device.keys()
        if missing:
            raise ValueError(f"{name} is missing inventory fields: {sorted(missing)}")
        ipaddress.ip_address(device["host"])
        ipaddress.ip_address(device["router_id"])
        ipaddress.ip_interface(device["loopback"])
        for link in device["links"]:
            ipaddress.ip_interface(link["address"])
            ipaddress.ip_address(link["peer_address"])
            if link["peer"] not in devices:
                raise ValueError(f"{name} references unknown peer {link['peer']}")


def ios_address(cidr: str) -> tuple[str, str]:
    interface = ipaddress.ip_interface(cidr)
    return str(interface.ip), str(interface.netmask)


def baseline_config(device: dict[str, Any]) -> list[str]:
    loopback_ip, loopback_mask = ios_address(device["loopback"])
    commands = [
        f"hostname {device['name']}",
        "no ip domain-lookup",
        "ip cef",
        "interface Loopback0",
        " description ROUTER-ID-AND-TEST-NETWORK",
        f" ip address {loopback_ip} {loopback_mask}",
        " no shutdown",
    ]
    for link in device["links"]:
        address, mask = ios_address(link["address"])
        commands.extend(
            [
                f"interface {link['interface']}",
                f" description {link['description']}",
                f" ip address {address} {mask}",
                " ip ospf network point-to-point",
                " no shutdown",
            ]
        )
    return commands


def ospf_config(device: dict[str, Any]) -> list[str]:
    commands = [
        "router ospf 1",
        f" router-id {device['router_id']}",
        " passive-interface default",
        f" network {device['router_id']} 0.0.0.0 area 0",
    ]
    for link in device["links"]:
        commands.extend(
            [
                f" no passive-interface {link['interface']}",
                f" network {ios_address(link['address'])[0]} 0.0.0.0 area 0",
            ]
        )
    return commands


def ebgp_config(device: dict[str, Any], devices: dict[str, Any]) -> list[str]:
    commands = [
        f"router bgp {device['asn']}",
        " bgp log-neighbor-changes",
        f" bgp router-id {device['router_id']}",
        f" network {device['router_id']} mask 255.255.255.255",
    ]
    for link in device["links"]:
        peer = devices[link["peer"]]
        commands.extend(
            [
                f" neighbor {link['peer_address']} remote-as {peer['asn']}",
                f" neighbor {link['peer_address']} description {link['peer']}",
            ]
        )
    return commands


def ibgp_rr_config(device: dict[str, Any], devices: dict[str, Any]) -> list[str]:
    common_as = 65000
    commands = [
        f"router bgp {common_as}",
        " bgp log-neighbor-changes",
        f" bgp router-id {device['router_id']}",
        f" network {device['router_id']} mask 255.255.255.255",
    ]
    if device["name"] == "R2":
        peers = [devices["R1"], devices["R3"]]
        for peer in peers:
            commands.extend(
                [
                    f" neighbor {peer['router_id']} remote-as {common_as}",
                    f" neighbor {peer['router_id']} update-source Loopback0",
                    f" neighbor {peer['router_id']} route-reflector-client",
                    f" neighbor {peer['router_id']} description RR-CLIENT-{peer['name']}",
                ]
            )
    else:
        rr = devices["R2"]
        commands.extend(
            [
                f" neighbor {rr['router_id']} remote-as {common_as}",
                f" neighbor {rr['router_id']} update-source Loopback0",
                f" neighbor {rr['router_id']} description ROUTE-REFLECTOR-R2",
            ]
        )
    return commands


def scenario_config(
    scenario: str, device: dict[str, Any], devices: dict[str, Any]
) -> list[str]:
    if scenario == "bgp-only":
        return ebgp_config(device, devices)

    commands = baseline_config(device)
    if scenario in {"ospf", "ospf-ebgp", "ibgp-rr"}:
        commands.extend(ospf_config(device))
    if scenario in {"ebgp", "ospf-ebgp"}:
        commands.extend(ebgp_config(device, devices))
    if scenario == "ibgp-rr":
        commands.extend(ibgp_rr_config(device, devices))
    return commands


def cleanup_config(device: dict[str, Any]) -> list[str]:
    return [
        "no router ospf 1",
        f"no router bgp {device['asn']}",
        "no router bgp 65000",
    ]


def verification_commands(scenario: str) -> list[str]:
    commands = [
        "show clock",
        "show ip interface brief",
        "show cdp neighbors",
        "show ip route",
    ]
    if scenario in {"ospf", "bgp-only", "ospf-ebgp", "ibgp-rr"}:
        commands.extend(
            ["show ip ospf neighbor", "show ip ospf interface brief", "show ip route ospf"]
        )
    if scenario in {"ebgp", "bgp-only", "ospf-ebgp", "ibgp-rr"}:
        commands.extend(
            ["show ip bgp summary", "show ip bgp", "show ip route bgp"]
        )
    commands.extend(
        [
            "ping 10.255.0.1 repeat 3 timeout 1",
            "ping 10.255.0.2 repeat 3 timeout 1",
            "ping 10.255.0.3 repeat 3 timeout 1",
        ]
    )
    return commands


def health_commands() -> list[str]:
    return [
        "show clock",
        "show version",
        "show inventory",
        "show processes cpu sorted 5sec",
        "show memory statistics",
        "show ip interface brief",
        "show interfaces counters errors",
        "show logging | last 50",
        "show cdp neighbors detail",
    ]


def credentials() -> dict[str, str]:
    username = os.getenv("LAB_USERNAME")
    password = os.getenv("LAB_PASSWORD")
    if not username or not password:
        raise RuntimeError(
            "Set LAB_USERNAME and LAB_PASSWORD before a live device action"
        )
    return {
        "username": username,
        "password": password,
        "secret": os.getenv("LAB_SECRET", password),
    }


def connect(device: dict[str, Any]):
    try:
        from netmiko import ConnectHandler
    except ImportError as exc:
        raise RuntimeError("Install dependencies with: pip install -r requirements.txt") from exc

    params = {
        "device_type": device["device_type"],
        "host": device["host"],
        "port": device["port"],
        **credentials(),
    }
    connection = ConnectHandler(**params)
    if connection.check_enable_mode() is False:
        connection.enable()
    return connection


def run_precheck(device: dict[str, Any]) -> dict[str, Any]:
    try:
        with socket.create_connection((device["host"], device["port"]), timeout=3):
            return {"device": device["name"], "host": device["host"], "ssh": "reachable"}
    except OSError as exc:
        return {
            "device": device["name"],
            "host": device["host"],
            "ssh": "unreachable",
            "error": str(exc),
        }


def run_show_commands(device: dict[str, Any], commands: list[str]) -> dict[str, Any]:
    connection = connect(device)
    try:
        return {
            "device": device["name"],
            "host": device["host"],
            "commands": {
                command: connection.send_command(command, read_timeout=60)
                for command in commands
            },
        }
    finally:
        connection.disconnect()


def run_config(
    device: dict[str, Any], commands: list[str], save: bool
) -> dict[str, Any]:
    connection = connect(device)
    try:
        output = connection.send_config_set(commands, read_timeout=90)
        save_output = connection.save_config() if save else "not requested"
        return {
            "device": device["name"],
            "host": device["host"],
            "config_output": output,
            "save_output": save_output,
        }
    finally:
        connection.disconnect()


def execute_parallel(devices: list[dict[str, Any]], worker) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=len(devices)) as executor:
        futures = {executor.submit(worker, device): device for device in devices}
        for future in as_completed(futures):
            device = futures[future]
            try:
                results.append(future.result())
            except Exception as exc:
                results.append(
                    {
                        "device": device["name"],
                        "host": device["host"],
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
    return sorted(results, key=lambda item: item["device"])


def save_results(
    action: str, scenario: str, results: list[dict[str, Any]], output_dir: Path
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"{timestamp}_{action}_{scenario}.json"
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return path


def select_devices(
    devices: dict[str, Any], requested: list[str] | None
) -> list[dict[str, Any]]:
    if not requested:
        return list(devices.values())
    unknown = sorted(set(requested) - devices.keys())
    if unknown:
        raise ValueError(f"Unknown devices: {', '.join(unknown)}")
    return [devices[name] for name in requested]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Safe Netmiko automation for the EVE-NG three-router lab"
    )
    parser.add_argument(
        "action",
        choices=("plan", "precheck", "apply", "verify", "health", "backup", "cleanup"),
    )
    parser.add_argument("--scenario", choices=SCENARIOS, default="ospf")
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--devices", nargs="+", metavar="ROUTER")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Required confirmation for actions that change device configuration",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save running configuration to startup configuration after apply/cleanup",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        load_env_file()
        inventory = load_inventory(args.inventory)
        selected = select_devices(inventory, args.devices)

        if args.action == "plan":
            results = [
                {
                    "device": device["name"],
                    "host": device["host"],
                    "commands": scenario_config(args.scenario, device, inventory),
                }
                for device in selected
            ]
        elif args.action == "precheck":
            results = execute_parallel(selected, run_precheck)
        elif args.action == "verify":
            commands = verification_commands(args.scenario)
            results = execute_parallel(
                selected, lambda device: run_show_commands(device, commands)
            )
        elif args.action == "health":
            results = execute_parallel(
                selected, lambda device: run_show_commands(device, health_commands())
            )
        elif args.action == "backup":
            results = execute_parallel(
                selected,
                lambda device: run_show_commands(
                    device, ["show running-config", "show startup-config"]
                ),
            )
        elif args.action in {"apply", "cleanup"}:
            if not args.apply:
                raise RuntimeError(
                    f"{args.action} changes routers; repeat the command with --apply"
                )
            results = execute_parallel(
                selected,
                lambda device: run_config(
                    device,
                    scenario_config(args.scenario, device, inventory)
                    if args.action == "apply"
                    else cleanup_config(device),
                    args.save,
                ),
            )
        else:
            raise AssertionError(f"Unhandled action {args.action}")

        path = save_results(args.action, args.scenario, results, args.output_dir)
        print(json.dumps(results, indent=2))
        print(f"\nSaved report: {path}")
        return 1 if any("error" in result for result in results) else 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
