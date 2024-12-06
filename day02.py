with open('./day02_input.txt', 'r') as input_file:
    input_file_contents: list[str] = [ line.rstrip() for line in input_file ]

levels: list[list[int]] = [ 
    [ int(level) for level in level_line.split() ] 
    for level_line in 
    input_file_contents 
]

def get_level_diffs(levels: list[int]) -> list[int]:
    level_diffs: list[int]  = [ level - levels[index] 
    for index, level in enumerate(levels[1:]) ]
    return level_diffs

def all_diffs_are_same_sign(diffs: list[int]) -> bool:
    diffs_are_negative: list[bool] = [ bool(diff > 0) for diff in diffs ]
    diffs_are_positive: list[bool] = [ bool(diff < 0) for diff in diffs ]

    if all(diffs_are_negative) or all(diffs_are_positive):
        return True
    return False

def all_diffs_are_small(diffs: list[int]) -> bool:
    diffs_are_small: list[bool] = [ bool(0 < abs(diff) < 4) for diff in diffs ]
    return all(diffs_are_small)

def all_diffs_are_safe(diffs: list[int]) -> bool:
    safe_diffs: list[bool] = [ bool(all_diffs_are_same_sign(diffs) and all_diffs_are_small(diffs)) ]
    return all(safe_diffs)

safe_levels: list[list[int]] = [ level for level in levels if all_diffs_are_safe(get_level_diffs(level)) ]
count_of_safe_levels: int = len(safe_levels)

# Part 1 Answer
print(count_of_safe_levels)

def get_possible_levels(levels: list[int]) -> list[list[int]]:
    possible_levels: list[list[int]] = [
        levels[:index] + levels[index + 1 :]
        for index, level in enumerate(levels)
    ]
    return possible_levels

def most_levels_are_safe(levels: list[int]) -> bool:
    level_count: int = len(levels)
    possible_levels: list[list[int]] = get_possible_levels(levels)
    safe_levels: list[list[int]] = [
        levels for levels in possible_levels
        if all_diffs_are_safe(get_level_diffs(levels))
    ]
    most_levels_are_safe: bool = bool(safe_levels)

    return most_levels_are_safe

potentially_unsafe_levels: list[list[int]] = [ level for level in levels if not all_diffs_are_safe(get_level_diffs(level)) ]
mostly_safe_levels: list[list[int]] = [ levels for levels in potentially_unsafe_levels if most_levels_are_safe(levels) ]
count_of_mostly_safe_levels: int = len(mostly_safe_levels)
count_of_safe_or_mostly_safe_levels: int = count_of_safe_levels + count_of_mostly_safe_levels

# Part 2 Answer
print(count_of_safe_or_mostly_safe_levels)