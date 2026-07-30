import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Display information about a network device."
    )

    parser.add_argument(
        "--hostname",
        required=True,
        help="Hostname of the device",
    )

    parser.add_argument(
        "--ip",
        required=True,
        help="Management IP address",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    print(f"Hostname: {args.hostname}")
    print(f"Management IP: {args.ip}")


if __name__ == "__main__":
    main()