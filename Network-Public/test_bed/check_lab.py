#!/usr/bin/env python3
"""
EVE-NG IOS-XRv Lab — Automated Health Check
============================================
Checks per device:
  1. Interface up/down status
  2. Port-channel (Bundle-Ether) membership & flags
  3. MACsec session state
  4. BGP neighbor summary

Usage:
  export NET_USER=admin
  export NET_PASS=admin
  python check_lab.py

  # Target a single device:
  python check_lab.py --device XRv-PE1

  # Save JSON report:
  python check_lab.py --report report.json
"""

import argparse
import json
import sys
from datetime import datetime

# ── pyATS / Genie ─────────────────────────────────────────────────────────────
try:
    from genie.testbed import load
except ImportError:
    sys.exit("[ERROR] pyATS/Genie not installed. Run: pip install pyats[full] genie")

# ── ANSI colours (stripped if not a TTY) ──────────────────────────────────────
def _c(code, text):
    return f"\033[{code}m{text}\033[0m" if sys.stdout.isatty() else text

OK   = lambda t: _c("32", f"✓  {t}")
WARN = lambda t: _c("33", f"⚠  {t}")
ERR  = lambda t: _c("31", f"✗  {t}")
HDR  = lambda t: _c("1;34", t)
DIM  = lambda t: _c("2",   t)

# ── helpers ───────────────────────────────────────────────────────────────────

def safe_parse(device, cmd):
    """Return parsed dict or None on failure."""
    try:
        return device.parse(cmd)
    except Exception as e:
        print(WARN(f"  parse('{cmd}') failed: {e}"))
        return None

def safe_execute(device, cmd):
    """Return raw CLI output or empty string on failure."""
    try:
        return device.execute(cmd)
    except Exception as e:
        print(WARN(f"  execute('{cmd}') failed: {e}"))
        return ""

# ── Check 1: Interface status ─────────────────────────────────────────────────

def check_interfaces(device, report):
    print(HDR("\n  [1] Interface status"))
    parsed = safe_parse(device, "show interfaces")
    if not parsed:
        report["interfaces"] = {"error": "parse failed"}
        return

    results = {}
    for intf, data in parsed.items():
        oper  = data.get("oper_status", "unknown")
        line  = data.get("line_protocol", "unknown")
        encap = data.get("encapsulations", {}).get("encapsulation", "")
        entry = {"oper": oper, "line": line, "encap": encap}
        results[intf] = entry

        if oper == "up" and line == "up":
            print(OK(f"  {intf:<40} oper={oper}  line={line}"))
        elif "Loopback" in intf or "Management" in intf:
            print(DIM(f"  {intf:<40} oper={oper}  line={line}"))
        else:
            print(ERR(f"  {intf:<40} oper={oper}  line={line}"))

    report["interfaces"] = results

# ── Check 2: Bundle-Ether (port-channel) ──────────────────────────────────────

def check_bundle(device, report):
    print(HDR("\n  [2] Bundle-Ether (port-channel) membership"))
    parsed = safe_parse(device, "show bundle")
    if not parsed:
        # fallback to raw output
        raw = safe_execute(device, "show bundle")
        report["bundle"] = {"raw": raw}
        return

    results = {}
    bundles = parsed.get("interfaces", parsed)   # Genie key varies by version

    for bundle_name, bdata in bundles.items():
        if "Bundle" not in bundle_name:
            continue
        state   = bdata.get("oper_status", bdata.get("state", "unknown"))
        members = bdata.get("members", bdata.get("port", {}))
        b_entry = {"state": state, "members": {}}
        results[bundle_name] = b_entry

        print(f"\n    {bundle_name}  state={state}")

        if not members:
            print(WARN("      No members found"))
            continue

        for mname, mdata in members.items():
            flags  = mdata.get("flags", mdata.get("status", "?"))
            state_ = mdata.get("state", mdata.get("port_state", "?"))
            b_entry["members"][mname] = {"flags": flags, "state": state_}

            # SA = Selected Active (good), NA/Standby = warning, other = error
            if "SA" in str(flags) or state_ in ("active", "up"):
                print(OK(f"      {mname:<36} flags={flags}  state={state_}"))
            elif "standby" in str(state_).lower():
                print(WARN(f"      {mname:<36} flags={flags}  state={state_}"))
            else:
                print(ERR(f"      {mname:<36} flags={flags}  state={state_}"))

    report["bundle"] = results

# ── Check 3: MACsec ───────────────────────────────────────────────────────────

def check_macsec(device, report):
    print(HDR("\n  [3] MACsec session state"))
    raw = safe_execute(device, "show macsec summary")
    if not raw:
        report["macsec"] = {"raw": "no output"}
        return

    lines   = raw.strip().splitlines()
    results = {}

    for line in lines:
        line = line.strip()
        if not line or line.startswith("Interface") or line.startswith("---"):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        intf   = parts[0]
        # Typical columns: Interface  Cipher  Must-Secure  AN  SessionState  KeysUnused
        # Last field with a known state keyword
        session_state = "unknown"
        for keyword in ("Secured", "Unsecured", "Init", "No-MKA", "MKA-Failed"):
            if keyword.lower() in line.lower():
                session_state = keyword
                break

        results[intf] = {"raw_line": line, "session_state": session_state}

        if session_state == "Secured":
            print(OK(f"  {intf:<36} {session_state}"))
        elif session_state == "Unsecured":
            print(WARN(f"  {intf:<36} {session_state}"))
        else:
            print(ERR(f"  {intf:<36} {session_state}"))

    if not results:
        print(DIM("  No MACsec interfaces found — MACsec may not be configured"))

    # Also pull per-interface detail for any Secured sessions
    for intf, data in results.items():
        if data["session_state"] == "Secured":
            detail = safe_execute(device, f"show macsec detail interface {intf}")
            data["detail"] = detail

    report["macsec"] = results

# ── Check 4: BGP summary ──────────────────────────────────────────────────────

def check_bgp(device, report):
    print(HDR("\n  [4] BGP neighbor summary"))
    parsed = safe_parse(device, "show bgp summary")
    if not parsed:
        raw = safe_execute(device, "show bgp ipv4 unicast summary")
        report["bgp"] = {"raw": raw}
        return

    results   = {}
    vrf_block = parsed.get("instance", {})

    for inst_name, inst_data in vrf_block.items():
        for vrf_name, vrf_data in inst_data.get("vrf", {}).items():
            neighbors = vrf_data.get("neighbor", {})
            for nbr_ip, nbr_data in neighbors.items():
                state    = nbr_data.get("session_state", "unknown")
                prefixes = nbr_data.get("prefixes", {}).get("received", {}).get("total_entries", "?")
                asn      = nbr_data.get("remote_as", "?")
                key      = f"{vrf_name}/{nbr_ip}"
                results[key] = {"state": state, "remote_as": asn, "prefixes_rx": prefixes}

                if state.lower() == "established":
                    print(OK(f"  {nbr_ip:<20} AS {asn:<8} state={state:<15} pfx_rx={prefixes}"))
                else:
                    print(ERR(f"  {nbr_ip:<20} AS {asn:<8} state={state:<15}"))

    if not results:
        print(DIM("  No BGP neighbors found — BGP may not be configured"))

    report["bgp"] = results

# ── Main ──────────────────────────────────────────────────────────────────────

def run_checks(device, device_name):
    report = {"device": device_name, "timestamp": datetime.utcnow().isoformat()}
    print("\n" + "=" * 60)
    print(HDR(f"  Device: {device_name}"))
    print("=" * 60)

    check_interfaces(device, report)
    check_bundle(device, report)
    check_macsec(device, report)
    check_bgp(device, report)

    return report


def main():
    parser = argparse.ArgumentParser(description="IOS-XRv EVE-NG lab health check")
    parser.add_argument("--testbed", default="testbed.yaml", help="Path to testbed.yaml")
    parser.add_argument("--device",  default=None,           help="Run against one device only")
    parser.add_argument("--report",  default=None,           help="Save JSON report to file")
    args = parser.parse_args()

    print(HDR(f"\nLoading testbed: {args.testbed}"))
    testbed = load(args.testbed)

    devices_to_check = (
        {args.device: testbed.devices[args.device]}
        if args.device
        else testbed.devices
    )

    all_reports = []

    for name, device in devices_to_check.items():
        print(f"\nConnecting to {name} ...")
        try:
            device.connect(
                log_stdout=False,
                learn_hostname=True,
                connection_timeout=30,
            )
        except Exception as e:
            print(ERR(f"Could not connect to {name}: {e}"))
            all_reports.append({"device": name, "error": str(e)})
            continue

        try:
            report = run_checks(device, name)
            all_reports.append(report)
        finally:
            device.disconnect()

    # ── Summary ────────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(HDR("  Summary"))
    print("=" * 60)
    for r in all_reports:
        if "error" in r:
            print(ERR(f"  {r['device']}: connection failed"))
        else:
            intf_up = sum(
                1 for v in r.get("interfaces", {}).values()
                if isinstance(v, dict) and v.get("oper") == "up"
            )
            bgp_est = sum(
                1 for v in r.get("bgp", {}).values()
                if isinstance(v, dict) and v.get("state", "").lower() == "established"
            )
            mac_sec = sum(
                1 for v in r.get("macsec", {}).values()
                if isinstance(v, dict) and v.get("session_state") == "Secured"
            )
            print(OK(
                f"  {r['device']:<20} "
                f"interfaces_up={intf_up}  "
                f"bgp_established={bgp_est}  "
                f"macsec_secured={mac_sec}"
            ))

    if args.report:
        with open(args.report, "w") as f:
            json.dump(all_reports, f, indent=2)
        print(f"\n  Report saved → {args.report}")

    print()


if __name__ == "__main__":
    main()
