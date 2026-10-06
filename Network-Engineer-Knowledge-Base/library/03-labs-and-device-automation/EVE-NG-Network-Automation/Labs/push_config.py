from netmiko import ConnectHandler

routers = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.54.135",  
        "username": "admin",
        "password": "admin123",
        "secret": "admin123",
    }
]

for router in routers:
    print(f"\n connecting to {router['host']}")
    conn = ConnectHandler(**router)
    conn.enable

    commands = [
        "interface loopback0",
        "ip address 1.1.1.1 255.255.255.255",
        "description Automated_by_python"
    ]

    output = conn.send_config_set(commands)
    print(output)
    conn.disconnect()