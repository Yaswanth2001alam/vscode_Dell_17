import sys


def check_connection(is_connected):
    if is_connected:
        print("Connection successful.")
        return 0

    print("Connection failed.")
    return 1


def main():
    connected = False
    return check_connection(connected)


if __name__ == "__main__":
    sys.exit(main())
    