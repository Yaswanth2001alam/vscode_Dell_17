def display_device(device):
    print(f"Hostname: {device['hostname']}")
    print(f"IP address: {device['ip_address']}")
    print(f"vendor: {device['vendor']}")
    print("-" * 30)

def main():
    devices = [
        {
            "hostname": "router1",
            "ip_address": "192.168.1.1",
            "vendor": "Cisco",
        },
        {
            "hostname": "router2",
            "ip_address": "192.168.1.2",
            "vendor": "Juniper",
        },
        {
            "hostname": "switch1",
            "ip_address": "192.168.1.3",
            "vendor": "Arista",
        },

    ]

    for device in devices:
        display_device(device)

if __name__ == "__main__":
    main()