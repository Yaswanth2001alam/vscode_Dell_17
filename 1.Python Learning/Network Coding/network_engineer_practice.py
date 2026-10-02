import csv
import ipaddress
from io import StringIO


def is_valid_ipv4_address(value: str) -> bool:
    """Return True if value is a valid IPv4 address."""
    try:
        return ipaddress.IPv4Address(value) is not None
    except ipaddress.AddressValueError:
        return False


def summarize_ipv4_network(cidr: str) -> dict[str, str | int]:
    """Summarize an IPv4 subnet, including traditional usable host addresses."""
    network = ipaddress.IPv4Network(cidr, strict=False)

    if network.prefixlen <= 30:
        first_host = network.network_address + 1
        last_host = network.broadcast_address - 1
        usable_hosts = network.num_addresses - 2
    elif network.prefixlen == 31:
        first_host = network.network_address
        last_host = network.broadcast_address
        usable_hosts = 2
    else:  # A /32 contains one address.
        first_host = network.network_address
        last_host = network.network_address
        usable_hosts = 1

    return {
        "network": str(network.network_address),
        "prefix": network.prefixlen,
        "broadcast": str(network.broadcast_address),
        "first_usable": str(first_host),
        "last_usable": str(last_host),
        "usable_hosts": usable_hosts,
    }


def parse_interface_csv(csv_text: str) -> list[dict[str, str]]:
    """Read interface records from CSV with interface, ip, status, protocol columns."""
    reader = csv.DictReader(StringIO(csv_text))
    required_columns = {"interface", "ip", "status", "protocol"}
    if reader.fieldnames is None or not required_columns.issubset(
        {name.strip().lower() for name in reader.fieldnames}
    ):
        raise ValueError("CSV must have interface, ip, status, and protocol columns.")

    return [
        {key.strip().lower(): value.strip() for key, value in row.items() if key and value}
        for row in reader
    ]


def find_interfaces_not_up(interfaces: list[dict[str, str]]) -> list[str]:
    """Return interface names whose status or line protocol is not up."""
    return [
        interface["interface"]
        for interface in interfaces
        if interface.get("status", "").lower() != "up"
        or interface.get("protocol", "").lower() != "up"
    ]


def main() -> None:
    print("IPv4 address validation:")
    for address in ("192.168.1.10", "300.1.2.3"):
        print(f"  {address}: {is_valid_ipv4_address(address)}")

    print("\nSubnet summary for 192.168.10.42/24:")
    for label, value in summarize_ipv4_network("192.168.10.42/24").items():
        print(f"  {label}: {value}")

    sample_csv = """interface,ip,status,protocol
GigabitEthernet0/0,192.0.2.1,up,up
GigabitEthernet0/1,unassigned,administratively down,down
"""
    interfaces = parse_interface_csv(sample_csv)
    print("\nInterfaces needing attention:")
    for name in find_interfaces_not_up(interfaces):
        print(f"  {name}")


if __name__ == "__main__":
    main()
