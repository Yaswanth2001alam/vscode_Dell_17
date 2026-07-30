def ping_message(device_ip):
    return f"Pinging {device_ip}.......................,,,,,,,,,"

def main():
    print("network_tools.py was executed directly")
    print(ping_message("192.168.1.1"))

if __name__ == "__main__":
    main()