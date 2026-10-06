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

    print(conn.send_command("show run interface loopback0"))
    conn.disconnect()