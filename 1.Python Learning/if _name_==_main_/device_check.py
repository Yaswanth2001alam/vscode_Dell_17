def check_device_status(device_name, status):
    if status == "up":
        return f"{device_name} is reachable"
    else:
        return f"{device_name} is not rechable"
    
def main():
    device_name = "router1"
    device_status = "up"

    result = check_device_status(device_name, device_status)
    print(result)

if __name__ == "__main__":
    main()