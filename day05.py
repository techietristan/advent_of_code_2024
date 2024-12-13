import math

with open('day05_input.txt', 'r') as print_queue:
    print_queue_contents: list[str] = [ line.replace('\n', '') for line in print_queue ]#[1150:1250]

def get_updates(print_queue_line) -> list[int] | None:
    if ',' not in print_queue_line:
        return None
    page_order: list[int] = [ int(page) for page in print_queue_line.split(',') ]
    return page_order

def update_is_valid(update: list[int], rules: tuple[tuple[int, int], ...]) -> bool:
    for order_rule in rules:
        first_page, second_page = order_rule[0], order_rule[1]
        if first_page in update and second_page in update:
            first_page_index, second_page_index = update.index(first_page), update.index(second_page)
            if not bool(first_page_index < second_page_index):
                return False
    return True

def get_valid_and_invalid_updates(print_queue_contents: list[str], rules) -> tuple[list[list[int]], ...]:
    updates: list[list[int]] = [ get_updates(line) for line in print_queue_contents if ',' in line ] #type: ignore [misc]
    valid_updates: list[list[int]] = [ update for update in updates if update_is_valid(update, rules) ]
    invalid_updates: list[list[int]] = [ update for update in updates if not update_is_valid(update, rules) ]

    return valid_updates, invalid_updates

def get_middle_value(values: list[int]) -> int:
    value_count: int = len(values)
    middle_value_index: int = math.floor(value_count / 2)

    return values[middle_value_index]

rules: tuple[tuple[int, int], ...] = tuple( (int(line.split('|')[0]), int(line.split('|')[1])) for line in print_queue_contents if '|' in line )
valid_updates: list[list[int]] = get_valid_and_invalid_updates(print_queue_contents, rules)[0]
middle_values: list[int] = [ get_middle_value(values) for values in valid_updates ]
sum_of_middle_values: int = sum(middle_values)

# Part 1 Solution
print(sum_of_middle_values)

invalid_updates: list[list[int]] = get_valid_and_invalid_updates(print_queue_contents, rules)[1]

def rule_applies(pages: list[int], rule: tuple[int, int]) -> bool:
    first_page, second_page = rule
    return first_page in pages and second_page in pages

def get_page_priority(page: int, rules: list[tuple[int, int]]) -> int:
    priority_list: list[int] = [ rule[0] for rule in rules ]
    depriority_list: list[int] = [ rule[1] for rule in rules ]
    page_priority: int = depriority_list.count(page) - priority_list.count(page) 

    return page_priority

def get_page_priorities(pages: list[int], rules: list[tuple[int, int]]) -> list[tuple[int, int]]:
    page_priorities: list[tuple[int, int]] = [ (page, get_page_priority(page, rules)) for page in pages ]

    return page_priorities

def prioritize_pages(pages: list[int], rules: tuple[tuple[int, int], ...]) -> list[int]:
    applicable_rules = [ rule for rule in rules if rule_applies(pages, rule) ]
    page_priorities: list[tuple[int, int]] = get_page_priorities(pages, applicable_rules)
    prioritized_pages: list[int] = sorted(pages, key = lambda page: get_page_priority(page, applicable_rules))

    return prioritized_pages

prioritized_pages: list[list[int]] = [ prioritize_pages(pages, rules) for pages in invalid_updates ]
middle_prioritized_values: list[int] = [ get_middle_value(pages) for pages in prioritized_pages ]
sum_of_middle_prioritized_values: int = sum(middle_prioritized_values)

# Part 2 Solution
print(sum_of_middle_prioritized_values)