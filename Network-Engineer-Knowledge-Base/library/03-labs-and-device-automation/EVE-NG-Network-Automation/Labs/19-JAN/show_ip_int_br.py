from netmiko import ConnectHandler

routers = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.54.136",
        "username": "admin",
        "password": "admin123",
        "secret": "admin123"
    },
    
    {
        "device_type": "cisco_ios",
        "host": "192.168.54.137",  
        "username": "admin",
        "password": "admin123",
        "secret": "admin123",
    }
]

for router in routers:
    print(f"\n connecting to {router['host']}")
    conn = ConnectHandler(**router)
    conn.enable

    output = conn.send_command("show ip interface brief")
    print(output)
    conn.disconnect()