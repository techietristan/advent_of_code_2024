with open('day07_input.txt', 'r') as calibrations_file:
    calibration_lines: list[str] = [ line.replace('\n', '') for line in calibrations_file ]

def get_calibration(line: str) -> tuple[int, tuple[int, ...]]:
    result_str, inputs_str = line.split(':')
    result: int = int(result_str)
    inputs: tuple[int, ...] = tuple( int(input_str) for input_str in inputs_str.split())

    return result, inputs

calibrations: tuple[tuple[int, tuple[int, ...]], ...] = tuple( get_calibration(line) for line in calibration_lines )

def calibration_is_valid(calibration: tuple[int, tuple[int, ...]]) -> bool:
    result, inputs = calibration
    results: list[int] = [ inputs[0] ]

    for current_input in inputs[1:]:
        sums: list[int] = list( [current_input + result for result in results] )
        multiples: list[int] = list( [current_input * result for result in results] )
        results = sums + multiples

    if result in results:
        return True
    return False

valid_calibrations: list[int] = [ calibration[0] for calibration in calibrations if calibration_is_valid(calibration) ]
sum_of_valid_calibrations: int = sum(valid_calibrations)

# Part 1 Solution
print(sum_of_valid_calibrations)

def concat(first: int, second: int) -> int:
    first_str, second_str = str(first), str(second)
    concated: int = int(f'{first_str}{second_str}')

    return concated

def calibration_is_valid_concat(calibration: tuple[int, tuple[int, ...]]) -> bool:
    result, inputs = calibration
    results: list[int] = [ inputs[0] ]

    for current_input in inputs[1:]:
        sums: list[int] = list( [current_input + result for result in results] )
        multiples: list[int] = list( [current_input * result for result in results] )
        concats: list[int] = list( [concat(result, current_input) for result in results] )
        results = sums + multiples + concats

    if result in results:
        return True
    return False

valid_calibrations_concat: list[int] = [ calibration[0] for calibration in calibrations if calibration_is_valid_concat(calibration) ]
sum_of_valid_calibrations_concat: int = sum(valid_calibrations_concat)

# Part 2 Solution
print(sum_of_valid_calibrations_concat)

