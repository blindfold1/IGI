from Task_1.math_functions import compute_function_with_precision
from Task_1.input_utils import get_float_input, initialize_sequence_with_generator, initialize_sequence_with_user_input
from decorators.decorator import log_computation
from Task_2.number_processing import count_even_numbers
from Task_3.string_processing import count_spaces_and_punctuation
from Task_4.text_analysis import analyze_text
from Task_5.list_processing import input_list, find_max_abs_and_sum_between_positives, display_list

def display_results(results: list, eps: float):

    print("\nResults:")
    print("x\t\tn\t\tF(x)\t\tMath F(x)\t\teps")
    print("-" * 60)
    for x, n, f_x, math_f_x in results:
        print(f"{x:.1f}\t\t{n}\t\t{f_x:.6f}\t\t{math_f_x:.6f}\t\t{eps}")

@log_computation
def run_computation(sequence: list, eps: float) -> list:

    results = []
    for x in sequence:
        n, f_x, math_f_x = compute_function_with_precision(x, eps)
        results.append((x, n, f_x, math_f_x))
    return results

@log_computation
def run_number_processing() -> int:

    return count_even_numbers()

@log_computation
def run_string_processing(text: str):
    return count_spaces_and_punctuation(text)

@log_computation
def run_text_analysis(text: str):
    return analyze_text(text)

@log_computation
def run_list_processing(numbers: list[float]):
    return find_max_abs_and_sum_between_positives(numbers)

def main():
    while True:
        print("\n=== Lab Work #3 Program ===")
        print("1. Task 1: Compute Function with Series Expansion")
        print("2. Task 2: Count Even Numbers (Stop when number > 99)")
        print("3. Task 3: Count Spaces and Punctuation Marks")
        print("4. Task 4: Text Analysis (Variant 30)")
        print("5. Task 5: List Processing (Max Abs and Sum Between Positives)")
        print("6. Exit")

        choice = get_float_input("Enter your choice (1-6): ", 1, 6)

        if choice == 6:
            print("Exiting program. Goodbye!")
            break

        if choice == 1:
            print("\n=== Task 1: Function Computation ===")
            print("1. Use generator to initialize sequence (-1 to 1 with step 0.2)")
            print("2. Use user input to initialize sequence")
            print("3. Back to main menu")

            sub_choice = get_float_input("Enter your choice (1-3): ", 1, 3)

            if sub_choice == 3:
                continue

            eps = get_float_input("Enter precision (eps, e.g., 0.001): ", 0)

            if sub_choice == 1:
                sequence = initialize_sequence_with_generator(-1, 1, 0.2)
            else:
                size = int(get_float_input("Enter the number of values in the sequence: ", 1))
                sequence = initialize_sequence_with_user_input(size)

            try:
                results = run_computation(sequence, eps)
                display_results(results, eps)
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == 2:
            print("\n=== Task 2: Count Even Numbers ===")
            try:
                even_count = run_number_processing()
                print(f"\nNumber of even numbers entered: {even_count}")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == 3:
            print("\n=== Task 3: Count Spaces and Punctuation Marks ===")
            try:
                text = input("Enter a string: ")
                if not text:
                    raise ValueError("Input string cannot be empty.")

                result = run_string_processing(text)

                print("\nResults:")
                print(f"Number of spaces: {result.space_count}")
                print(f"Number of punctuation marks: {result.punctuation_count}")

            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == 4:
            print("\n=== Task 4: Text Analysis (Variant 30) ===")
            default_text = (
                "So she was considering in her own mind, as well as she could, for the hot day made her feel "
                "very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble "
                "of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
            )
            print("Default text:")
            print(default_text)
            print("\nYou can use the default text or enter your own text.")
            use_default = input("Use default text? (y/n): ").lower()

            if use_default == 'y':
                text = default_text
            else:
                text = input("Enter your text: ")
                if not text.strip():
                    print("Error: Input text cannot be empty. Using default text.")
                    text = default_text

            try:
                result = run_text_analysis(text)

                print("\nResults:")
                print(f"Number of words with maximum length: {result.max_length_count}")

                print("\nWords followed by a comma or period:")
                if result.words_with_punctuation:
                    for word in result.words_with_punctuation:
                        print(word)
                else:
                    print("No words followed by a comma or period found.")

                print("\nModify the longest word ending with 'e' to start with 'е':")
                if result.modified_longest_word:
                    print(f"Modified word: {result.modified_longest_word}")
                else:
                    print("No word ending with 'e' found.")

            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == 5:
            print("\n=== Task 5: List Processing (Max Abs and Sum Between Positives) ===")
            try:
                numbers = input_list()
                display_list(numbers)

                result = run_list_processing(numbers)

                print("\nResults:")
                print(f"Maximum absolute value: {result.max_abs_value}")
                print(f"Sum of elements between the first and second positive elements: {result.sum_between_positives}")

            except Exception as e:
                print(f"An error occurred: {e}")

        continue_choice = input("\nDo you want to continue? (y/n): ").lower()
        if continue_choice != 'y':
            print("Exiting program. Goodbye!")
            break

if __name__ == "__main__":
    main()