"""Minimal Nornir task showing filtering and per-host result handling."""

from __future__ import annotations

import argparse


def main() -> int:
    try:
        from nornir import InitNornir
        from nornir_netmiko.tasks import netmiko_send_command
    except ImportError as error:
        raise RuntimeError("Install requirements-lab.txt to use Nornir") from error

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--role", help="Only run hosts with this role")
    args = parser.parse_args()

    nr = InitNornir(config_file=args.config)
    if args.role:
        nr = nr.filter(role=args.role)
    if not nr.inventory.hosts:
        raise RuntimeError("No hosts matched the requested inventory filter")

    aggregated = nr.run(
        task=netmiko_send_command,
        command_string="show ip interface brief",
        read_timeout=30,
    )
    failed = False
    for host, multi_result in aggregated.items():
        host_failed = multi_result.failed
        failed = failed or host_failed
        print(f"\n[{host}] status={'ERROR' if host_failed else 'OK'}")
        for result in multi_result:
            print(result.exception if result.exception else result.result)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

