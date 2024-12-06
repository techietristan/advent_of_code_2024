import re

with open('./day03_input.txt', 'r') as input_file:
    input_file_contents: list[str] = [ line for line in input_file ]

instruction_lines: list[str] = input_file_contents
valid_instructions: list[list[str]] = [ re.findall(r'mul\(\d+,\d+\)', instruction_line) for instruction_line in instruction_lines ]
all_valid_instructions: list[str] = [ instruction for instruction_list in valid_instructions for instruction in instruction_list ]

def apply_multiply_instruction(instruction: str) -> int:
    numbers: list[str] = re.findall(r'\d+', instruction)
    first_number: int = int(numbers[0])
    second_number: int = int(numbers[1])

    return first_number * second_number

multiples: list[int] = [ apply_multiply_instruction(instruction) for instruction in all_valid_instructions ]
sum_of_multiples: int = sum(multiples)

# Part 1 Solution
print(sum_of_multiples)

all_instructions: list[str] = re.findall(r"don\'t\(\)|do\(\)|mul\(\d+,\d+\)", ''.join(input_file_contents))

def get_sum_of_enabled_multiples(instructions: list[str], current_index: int = 0, current_sum: int = 0, enabled: bool = True) -> int:
    number_of_instructions: int = len(instructions)
    if current_index == number_of_instructions - 1:
        return current_sum
    current_instruction: str = instructions[current_index]
    if current_instruction == 'do()':
        enabled = True
        return get_sum_of_enabled_multiples(instructions, current_index + 1, current_sum, enabled)
    if current_instruction == 'don\'t()':
        enabled = False
        return get_sum_of_enabled_multiples(instructions, current_index + 1, current_sum, enabled)
    if bool(enabled):
        current_multiple: int = apply_multiply_instruction(current_instruction)
        return get_sum_of_enabled_multiples(instructions, current_index + 1, current_sum + current_multiple, enabled)
    else:
        return get_sum_of_enabled_multiples(instructions, current_index + 1, current_sum, enabled)

sum_of_enabled_multiples: int = get_sum_of_enabled_multiples(all_instructions)

# Part 2 Solution
print(sum_of_enabled_multiples)