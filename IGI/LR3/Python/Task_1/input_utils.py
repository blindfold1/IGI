from typing import Generator

def get_float_input(prompt: str, min_val: float = None, max_val: float = None) -> float:
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                raise ValueError(f"Value must be greater than or equal to {min_val}")
            if max_val is not None and value > max_val:
                raise ValueError(f"Value must be less than or equal to {max_val}")
            return value
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

def initialize_sequence_with_generator(start: float, end: float, step: float) -> Generator[float, None, None]:
    for i in range(int((end - start) / step) + 1):
        yield round(start + i * step, 1)

def initialize_sequence_with_user_input(size: int) -> list:
    sequence = []
    for i in range(size):
        value = get_float_input(f"Enter value {i+1} (between -1 and 1): ", -1, 1)
        sequence.append(value)
    return sequence