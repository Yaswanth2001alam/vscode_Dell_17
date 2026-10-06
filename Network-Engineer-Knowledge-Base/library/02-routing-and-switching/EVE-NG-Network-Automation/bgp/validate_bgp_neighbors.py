#!/usr/bin/env python3
"""
BGP Neighbor Validation CLI Workflow

Standalone executable script to validate BGP neighbors on one or more devices
in an EVE-NG lab environment.

Usage:
    python validate_bgp_neighbors.py --testbed testbed.yaml --device router1
    python validate_bgp_neighbors.py --testbed testbed.yaml --report report.json
    python validate_bgp_neighbors.py --help
"""

import argparse
import json
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

try:
    from genie.testbed import load
except ImportError:
    sys.exit("[ERROR] Genie not installed. Run: pip install pyats[full] genie")

from bgp_neighbor_validator import BGPNeighborValidator, BGPValidationResult


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def _color(code: str, text: str) -> str:
    """Add ANSI color to text if output is a TTY."""
    if sys.stdout.isatty():
        return f"\033[{code}m{text}\033[0m"
    return text


OK = lambda t: _color("32", f"✓  {t}")
WARN = lambda t: _color("33", f"⚠  {t}")
ERR = lambda t: _color("31", f"✗  {t}")
HDR = lambda t: _color("1;34", t)


def validate_device_neighbors(
    device, device_name: str, vrf: str = "default"
) -> BGPValidationResult:
    """Validate BGP neighbors on a device."""
    logger.info(f"Connecting to {device_name}...")
    
    try:
        device.connect(
            log_stdout=False,
            learn_hostname=True,
            connection_timeout=30,
        )
    except Exception as e:
        logger.error(f"Failed to connect to {device_name}: {e}")
        result = BGPValidationResult(device_name=device_name, vrf=vrf)
        result.errors.append(f"Connection failed: {str(e)}")
        return result
    
    try:
        validator = BGPNeighborValidator(device, vrf=vrf)
        result = validator.validate_neighbors()
        return result
    
    finally:
        try:
            device.disconnect()
        except Exception as e:
            logger.warning(f"Error disconnecting from {device_name}: {e}")


def print_result(result: BGPValidationResult):
    """Print validation result in human-readable format."""
    print("\n" + "=" * 70)
    print(HDR(f"  Device: {result.device_name} | VRF: {result.vrf}"))
    print("=" * 70)
    
    if result.errors and result.total_neighbors == 0:
        for error in result.errors:
            print(ERR(f"  {error}"))
        return
    
    print(f"\n  {HDR('Summary:')}")
    print(f"    Total Neighbors: {result.total_neighbors}")
    print(OK(f"    Established: {result.established_count}"))
    
    if result.down_count > 0:
        print(ERR(f"    Down: {result.down_count}"))
    else:
        print(f"    Down: {result.down_count}")
    
    if result.error_neighbors > 0:
        print(ERR(f"    Error/Other: {result.error_neighbors}"))
    else:
        print(f"    Error/Other: {result.error_neighbors}")
    
    if not result.neighbors:
        print(WARN("  No neighbors found"))
        return
    
    print(f"\n  {HDR('Neighbors:')}")
    print(f"    {'-' * 66}")
    print(
        f"    {'IP Address':<20} {'AS':<10} {'State':<15} "
        f"{'RX Pfx':<10} {'TX Pfx':<10}"
    )
    print(f"    {'-' * 66}")
    
    for neighbor in result.neighbors:
        line = (
            f"    {neighbor.ip_address:<20} "
            f"{neighbor.remote_as:<10} "
            f"{neighbor.state.value:<15} "
            f"{neighbor.prefixes_received:<10} "
            f"{neighbor.prefixes_advertised:<10}"
        )
        
        if neighbor.is_healthy():
            print(OK(line))
        else:
            print(ERR(line))
    
    # Show unhealthy neighbors details
    unhealthy = result.get_unhealthy_neighbors()
    if unhealthy:
        print(f"\n  {HDR('Unhealthy Neighbors:')}")
        for neighbor in unhealthy:
            print(WARN(
                f"    {neighbor.ip_address} ({neighbor.state.value})"
            ))


def main():
    parser = argparse.ArgumentParser(
        description="BGP Neighbor Validation Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate all devices in testbed
  python validate_bgp_neighbors.py --testbed testbed.yaml
  
  # Validate specific device
  python validate_bgp_neighbors.py --testbed testbed.yaml --device router1
  
  # Save results to JSON report
  python validate_bgp_neighbors.py --testbed testbed.yaml --report report.json
  
  # Validate specific VRF
  python validate_bgp_neighbors.py --testbed testbed.yaml --vrf management
        """
    )
    
    parser.add_argument(
        "--testbed",
        default="testbed.yaml",
        help="Path to Genie testbed YAML file (default: testbed.yaml)"
    )
    parser.add_argument(
        "--device",
        default=None,
        help="Validate specific device only (if not specified, validates all)"
    )
    parser.add_argument(
        "--vrf",
        default="default",
        help="VRF to validate (default: default)"
    )
    parser.add_argument(
        "--report",
        default=None,
        help="Save JSON report to specified file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Verify testbed file exists
    if not Path(args.testbed).exists():
        print(ERR(f"Testbed file not found: {args.testbed}"))
        sys.exit(1)
    
    logger.info(f"Loading testbed: {args.testbed}")
    try:
        testbed = load(args.testbed)
    except Exception as e:
        print(ERR(f"Failed to load testbed: {e}"))
        sys.exit(1)
    
    # Select devices to validate
    if args.device:
        if args.device not in testbed.devices:
            print(ERR(f"Device '{args.device}' not found in testbed"))
            sys.exit(1)
        devices_to_check = {args.device: testbed.devices[args.device]}
    else:
        devices_to_check = testbed.devices
    
    # Validate each device
    all_results = []
    
    print(HDR("\n" + "=" * 70))
    print(HDR("  BGP Neighbor Validation"))
    print(HDR("=" * 70))
    
    for device_name, device in devices_to_check.items():
        result = validate_device_neighbors(device, device_name, vrf=args.vrf)
        all_results.append(result)
        print_result(result)
    
    # Print summary
    print("\n" + "=" * 70)
    print(HDR("  Validation Summary"))
    print("=" * 70)
    
    total_devices = len(all_results)
    successful = sum(1 for r in all_results if not r.errors)
    total_neighbors = sum(r.total_neighbors for r in all_results)
    total_established = sum(r.established_count for r in all_results)
    total_down = sum(r.down_count for r in all_results)
    
    print(f"  Devices validated: {successful}/{total_devices}")
    print(f"  Total neighbors: {total_neighbors}")
    print(OK(f"  Established: {total_established}"))
    
    if total_down > 0:
        print(ERR(f"  Down: {total_down}"))
    else:
        print(f"  Down: {total_down}")
    
    # Save report if requested
    if args.report:
        report_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "testbed": args.testbed,
            "vrf": args.vrf,
            "summary": {
                "devices_validated": successful,
                "total_devices": total_devices,
                "total_neighbors": total_neighbors,
                "established": total_established,
                "down": total_down,
            },
            "devices": [r.to_dict() for r in all_results],
        }
        
        try:
            with open(args.report, "w") as f:
                json.dump(report_data, f, indent=2)
            print(f"\n  Report saved to: {args.report}")
        except Exception as e:
            print(ERR(f"Failed to save report: {e}"))
            sys.exit(1)
    
    print()
    
    # Exit with appropriate code
    if any(r.errors for r in all_results):
        sys.exit(1)
    
    if total_down > 0:
        sys.exit(2)  # Warning exit code
    
    sys.exit(0)


if __name__ == "__main__":
    main()
