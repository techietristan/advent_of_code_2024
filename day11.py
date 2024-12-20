from functools import cache

with open('day11_input.txt', 'r') as line_of_stones:
    stones: list[str] = [ line for line in line_of_stones ][0].split()

def blink(stone: str) -> str:
    if int(stone) == 0:
        return '1'
    if len(stone) % 2 == 0:
        stone_size: int = int(len(stone) / 2)
        stone_1: str = str(int(stone[:stone_size]))
        stone_2: str = str(int(stone[stone_size:]))
        return(f'{stone_1} {stone_2}')
    return str( 2024 * int(stone) )

def get_stones_after_blink(stones: list[str]) -> str:
    stone_configuration: list[str] = [ blink(stone) for stone in stones ]
    new_stone_configuration: str = ' '.join(stone_configuration)

    return new_stone_configuration

def get_stones_after_blinks(stones: list[str], blinks: int) -> list[str]:
    if blinks == 0:
        return stones
    new_stone_configuration: str = get_stones_after_blink(stones)
    return get_stones_after_blinks(new_stone_configuration.split(), blinks - 1)

count_of_stones_after_blinking_25_times: int = len(get_stones_after_blinks(stones, 25))

# # Part 1 Solution
print(count_of_stones_after_blinking_25_times)

@cache
def get_stone_count_after_blinks(stone: int, remaining_blinks: int) -> int:
    if remaining_blinks == 0:
        return 1
    if stone == 0:
        return get_stone_count_after_blinks(1, remaining_blinks - 1)
    stone_string: str = str(stone)
    if len(stone_string) % 2 == 0:
        stone_size: int = int(len(stone_string) / 2)
        stone_1: int = int(stone_string[:stone_size])
        stone_2: int = int(stone_string[stone_size:])
        return get_stone_count_after_blinks(stone_1, remaining_blinks - 1) + get_stone_count_after_blinks(stone_2, remaining_blinks - 1)
    return get_stone_count_after_blinks(stone * 2024, remaining_blinks - 1)
        
stone_ints: list[int] = [ int(stone) for stone in stones ]
stone_counts: list[int] = [ get_stone_count_after_blinks(stone, 75) for stone in stone_ints ]
sum_of_stone_counts: int = sum(stone_counts)
# Part 2 Solution

print(sum_of_stone_counts)

