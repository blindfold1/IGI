def count_even_numbers() -> int:
    even_count = 0
    while True:
        try:
            number = int(input("Enter an integer (number > 99 to stop): "))
            if number > 99:
                break
            if number % 2 == 0:
                even_count += 1
        except ValueError:
            print("Error: Please enter a valid integer.")
    return even_count