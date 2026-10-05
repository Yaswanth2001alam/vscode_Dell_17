"""NETCONF get plus candidate/confirmed-commit workflow for a lab device."""

from __future__ import annotations

import argparse
import os

INTERFACE_FILTER = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
</filter>
""".strip()


def connect(host: str, port: int):
    try:
        from ncclient import manager
    except ImportError as error:
        raise RuntimeError("Install requirements.txt to use ncclient") from error

    username = os.getenv("LAB_USERNAME")
    password = os.getenv("LAB_PASSWORD")
    if not username or not password:
        raise RuntimeError("Set LAB_USERNAME and LAB_PASSWORD for a live lab")
    return manager.connect(
        host=host,
        port=port,
        username=username,
        password=password,
        hostkey_verify=True,
        allow_agent=False,
        look_for_keys=False,
        timeout=30,
    )


def read_interfaces(host: str, port: int) -> str:
    with connect(host, port) as session:
        return session.get(INTERFACE_FILTER).xml


def apply_candidate(
    host: str,
    port: int,
    candidate_xml: str,
    apply: bool,
) -> str:
    if not apply:
        return candidate_xml

    with connect(host, port) as session:
        capabilities = {str(item) for item in session.server_capabilities}
        if not any(":candidate" in item for item in capabilities):
            raise RuntimeError("Server does not advertise the candidate datastore")
        if not any(":confirmed-commit" in item for item in capabilities):
            raise RuntimeError("Server does not advertise confirmed commit")

        with session.locked(target="candidate"):
            session.edit_config(
                target="candidate",
                config=candidate_xml,
                default_operation="merge",
                test_option="test-then-set",
                error_option="rollback-on-error",
            )
            session.validate(source="candidate")
            session.commit(confirmed=True, timeout=120)
            try:
                operational = session.get(INTERFACE_FILTER).xml
                if "<interfaces" not in operational:
                    raise RuntimeError("Operational post-check returned no interfaces")
                session.commit()
            except Exception:
                session.cancel_commit()
                raise
    return operational


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("--port", type=int, default=830)
    parser.add_argument("--candidate-file")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    if args.candidate_file:
        with open(args.candidate_file, encoding="utf-8") as file:
            print(apply_candidate(args.host, args.port, file.read(), args.apply))
    else:
        print(read_interfaces(args.host, args.port))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
