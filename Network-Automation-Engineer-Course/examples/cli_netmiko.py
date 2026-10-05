"""Netmiko read-only collection and explicitly gated configuration example."""

from __future__ import annotations

import argparse
import json
import os
from typing import Any


def credentials() -> tuple[str, str]:
    username = os.getenv("LAB_USERNAME")
    password = os.getenv("LAB_PASSWORD")
    if not username or not password:
        raise RuntimeError("Set LAB_USERNAME and LAB_PASSWORD for a live lab")
    return username, password


def collect(host: str, device_type: str) -> dict[str, str]:
    try:
        from netmiko import ConnectHandler
    except ImportError as error:
        raise RuntimeError("Install requirements.txt to use Netmiko") from error

    username, password = credentials()
    params: dict[str, Any] = {
        "device_type": device_type,
        "host": host,
        "username": username,
        "password": password,
        "conn_timeout": 10,
        "banner_timeout": 15,
        "auth_timeout": 15,
    }
    commands = ["show clock", "show version", "show ip interface brief"]
    with ConnectHandler(**params) as connection:
        return {
            command: connection.send_command(command, read_timeout=30)
            for command in commands
        }


def configure_description(
    host: str,
    device_type: str,
    interface: str,
    description: str,
    apply: bool,
) -> dict[str, Any]:
    commands = [f"interface {interface}", f"description {description}"]
    if not apply:
        return {"applied": False, "host": host, "commands": commands}

    try:
        from netmiko import ConnectHandler
    except ImportError as error:
        raise RuntimeError("Install requirements.txt to use Netmiko") from error

    username, password = credentials()
    with ConnectHandler(
        device_type=device_type,
        host=host,
        username=username,
        password=password,
        conn_timeout=10,
    ) as connection:
        before = connection.send_command(
            f"show running-config interface {interface}", read_timeout=30
        )
        output = connection.send_config_set(commands, read_timeout=30)
        if "% Invalid input" in output or "% Incomplete command" in output:
            raise RuntimeError(f"Device rejected configuration: {output}")
        after = connection.send_command(
            f"show running-config interface {interface}", read_timeout=30
        )
    return {
        "applied": True,
        "host": host,
        "commands": commands,
        "before": before,
        "configuration_output": output,
        "after": after,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("--device-type", default="cisco_ios")
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--interface", default="Loopback123")
    parser.add_argument("--description", default="NETWORK-AUTOMATION-LAB")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the description. Without this flag the configuration is a dry-run.",
    )
    args = parser.parse_args()

    if args.collect:
        result: dict[str, Any] = collect(args.host, args.device_type)
    else:
        result = configure_description(
            args.host,
            args.device_type,
            args.interface,
            args.description,
            args.apply,
        )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

