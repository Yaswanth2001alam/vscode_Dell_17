"""RESTCONF GET and explicitly gated PATCH example."""

from __future__ import annotations

import argparse
import json
import os
from typing import Any

MEDIA_TYPE = "application/yang-data+json"


def request(
    host: str,
    resource: str,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    try:
        import requests
    except ImportError as error:
        raise RuntimeError("Install requirements.txt to use requests") from error

    username = os.getenv("LAB_USERNAME")
    password = os.getenv("LAB_PASSWORD")
    if not username or not password:
        raise RuntimeError("Set LAB_USERNAME and LAB_PASSWORD for a live lab")
    if not resource.startswith("/"):
        raise ValueError("RESTCONF resource must start with '/'")

    response = requests.request(
        method=method,
        url=f"https://{host}/restconf/data{resource}",
        headers={"Accept": MEDIA_TYPE, "Content-Type": MEDIA_TYPE},
        auth=(username, password),
        json=payload,
        timeout=(10, 30),
        verify=True,
    )
    response.raise_for_status()
    if response.status_code == 204 or not response.content:
        return {}
    return response.json()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument(
        "--resource",
        default="/ietf-interfaces:interfaces",
    )
    parser.add_argument("--patch-file")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Send the PATCH. Without this flag, print the payload only.",
    )
    args = parser.parse_args()

    if not args.patch_file:
        output = request(args.host, args.resource)
    else:
        with open(args.patch_file, encoding="utf-8") as file:
            payload = json.load(file)
        output = (
            request(args.host, args.resource, method="PATCH", payload=payload)
            if args.apply
            else {"applied": False, "resource": args.resource, "payload": payload}
        )
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

