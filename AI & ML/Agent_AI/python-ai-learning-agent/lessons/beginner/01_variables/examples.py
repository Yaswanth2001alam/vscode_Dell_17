"""Seven deterministic demonstrations. Run: python examples.py. No input required."""


def parse_count(raw_count: str) -> int:
    """Parse a nonnegative count, e.g. '24' -> 24; reject invalid text."""
    try:
        count = int(raw_count)
    except ValueError:
        raise ValueError("Count must be an integer written as text.") from None
    if count < 0:
        raise ValueError("Count must not be negative.")
    return count


def main() -> None:
    """Print reproducible examples; expected output is documented in notes.md."""
    count = 3
    previous = count
    count = 4
    print("1. Rebinding:", count, previous)

    values = [3, 2.5, "router", True, None]
    print("2. Types:", [type(value).__name__ for value in values])
    print("3. Conversion:", parse_count("24") + 1)

    devices = ["r1"]
    alias = devices
    alias.append("r2")
    print("4. Shared list:", devices)

    devices = ["r1"]
    independent = devices.copy()
    independent.append("r2")
    print("5. Copied list:", devices, independent)

    left = [1, 2]
    right = [1, 2]
    print("6. Equality and identity:", left == right, left is right)
    try:
        parse_count("twenty-four")
    except ValueError as error:
        print("7. Invalid input:", error)


if __name__ == "__main__":
    main()
