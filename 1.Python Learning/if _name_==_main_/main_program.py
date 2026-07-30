import network_tools

def main():
    message = network_tools.ping_message("10.0.0.1")
    print(message)

if __name__ == "__main__":
    main()