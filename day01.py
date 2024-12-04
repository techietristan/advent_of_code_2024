with open('./day01_input.txt', 'r') as input_file:
    input_file_contents: list[str] = [ input_line.rstrip() for input_line in input_file ]

def get_sorted_list_by_column(column_index: int) -> list[int]:
    return sorted([ int(location.split()[column_index]) for location in input_file_contents ])

left_list: list[int] = get_sorted_list_by_column(0)
right_list: list[int] = get_sorted_list_by_column(1)
combined_list: list[tuple] = [ location_pair for location_pair in zip(right_list, left_list) ]
difference_list: list[int] = [ abs(location[1] - location[0]) for location in combined_list ]
total_distance: int = sum(difference_list)

# Part 1 Answer
print(total_distance)

def get_similarity_score(location: int, locations: list[int]) -> int:
    location_count: int = locations.count(location)
    similarity_score: int = location_count * location
    return similarity_score

similarity_scores: list[int] = [ get_similarity_score(location, right_list) for location in left_list ]
sum_of_similarity_scores: int = sum(similarity_scores)

# Part 2 Answer
print(sum_of_similarity_scores)