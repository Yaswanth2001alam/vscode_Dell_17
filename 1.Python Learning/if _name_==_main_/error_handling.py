def divide(first_number, second_number):
    return first_number / second_number

def main():
    try:
        first_number = 100
        second_number = 0

        result = divide(first_number , second_number)
        print(f":result: {result}")

    except ZeroDivisionError:
        print("Error: You cannot divide by Zero")

if __name__ == "__main__":
    main()
            
