
class ListAnalysisResult:
    __slots__ = ('max_abs_value', 'sum_between_positives', 'first_positive', 'second_positive')

    def __init__(self, max_abs_value: float, sum_between_positives: float, first_positive: tuple, second_positive: tuple):
        self.max_abs_value = max_abs_value
        self.sum_between_positives = sum_between_positives
        self.first_positive = first_positive
        self.second_positive = second_positive

def input_list() -> list[float]:

    numbers = []
    size = 0
    while size <= 0:
        try:
            size = int(input("Enter the number of elements in the list: "))
            if size <= 0:
                print("Error: Number of elements must be greater than 0.")
        except ValueError:
            print("Error: Please enter a valid integer for the number of elements.")

    for i in range(size):
        while True:
            try:
                num = float(input(f"Enter element {i+1}: "))
                numbers.append(num)
                break
            except ValueError:
                print("Error: Please enter a valid float number.")

    return numbers

def find_max_abs_and_sum_between_positives(numbers: list[float]) -> ListAnalysisResult:

    if not numbers:
        return ListAnalysisResult(0.0, 0.0, (None, -1), (None, -1))


    max_abs_value = max(abs(num) for num in numbers)


    positive_elements = [(num, i) for i, num in enumerate(numbers) if num > 0]
    sum_between_positives = 0.0
    first_positive = (None, -1)
    second_positive = (None, -1)


    for i in range(len(positive_elements) - 1):
        if positive_elements[i + 1][1] > positive_elements[i][1] + 1:
            first_positive = positive_elements[i]
            second_positive = positive_elements[i + 1]
            start_idx = first_positive[1] + 1
            end_idx = second_positive[1]
            sum_between_positives = sum(numbers[start_idx:end_idx])
            break
    else:
        if len(positive_elements) >= 2:
            first_positive = positive_elements[0]
            second_positive = positive_elements[1]
        elif len(positive_elements) == 1:
            first_positive = positive_elements[0]

    return ListAnalysisResult(max_abs_value, sum_between_positives, first_positive, second_positive)

def display_list(numbers: list[float]):
    print("List of numbers:")
    print(numbers)