def add(first_number, second_number):
    return first_number + second_number

def subtract(first_number , second_number):
    return first_number - second_number

def main():
    first_number = 100
    second_number = 200

    addition_result = add(first_number , second_number)
    subtraction_result = subtract(first_number, second_number)

    print(f"Addition result: {addition_result}")
    print(f"Subtraction_result: {subtraction_result}")


if __name__ == "__main__":
    main()
