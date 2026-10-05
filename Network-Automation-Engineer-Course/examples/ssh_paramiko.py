"""Paramiko example using the user's known-hosts database."""

from __future__ import annotations

import argparse
import os


def run_command(host: str, command: str) -> tuple[str, str, int]:
    try:
        import paramiko
    except ImportError as error:
        raise RuntimeError("Install requirements.txt to use Paramiko") from error

    username = os.getenv("LAB_USERNAME")
    password = os.getenv("LAB_PASSWORD")
    if not username or not password:
        raise RuntimeError("Set LAB_USERNAME and LAB_PASSWORD for a live lab")

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    try:
        client.connect(
            hostname=host,
            username=username,
            password=password,
            timeout=10,
            banner_timeout=15,
            auth_timeout=15,
            look_for_keys=False,
        )
        _, stdout, stderr = client.exec_command(command, timeout=30)
        exit_status = stdout.channel.recv_exit_status()
        return (
            stdout.read().decode("utf-8", errors="replace"),
            stderr.read().decode("utf-8", errors="replace"),
            exit_status,
        )
    finally:
        client.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("command", help="Read-only command supported by the SSH server")
    args = parser.parse_args()
    stdout, stderr, status = run_command(args.host, args.command)
    print(stdout)
    if stderr:
        print(stderr)
    return status


if __name__ == "__main__":
    raise SystemExit(main())

