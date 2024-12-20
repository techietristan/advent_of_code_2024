with open('day10_input.txt', 'r') as map_file:
    topo_map: list[str] = [ line.strip() for line in map_file ]

def get_trailhead_coords(topo_map: list[str]) -> tuple[tuple[int, int], ...]:
    trailheads: list[tuple[int, int]] = []
    for row_index, row in enumerate(topo_map):
        for column_index, column in enumerate(row):
            if column == '0':
                trailheads.append((int(row_index), int(column_index)))
    return tuple(trailheads)

def get_next_coords(topo_map: list[str], current_coords: tuple[int, int], target_value: int) -> tuple[tuple[int, int], ...]:
    current_row, current_column = current_coords
    next_coords: list[tuple[int, int]] = []
    search_deltas: tuple[tuple[int, int], ...] = ((-1, 0), (0, 1), (1, 0), (0, -1))
    for search_delta in search_deltas:
        row_delta, column_delta = search_delta
        search_row, search_column = (current_row + row_delta, current_column + column_delta)
        search_is_valid: bool = 0 <= search_row < len(topo_map) and 0 <= search_column < len(topo_map[0])
        if search_is_valid:
            search_char: str = topo_map[search_row][search_column]
            if int(search_char) == target_value:
                next_coords.append((search_row, search_column))
    return tuple(next_coords)

def get_next_paths(topo_map: list[str], current_paths: list[list[tuple[int, int]]], target_value: int = 1) -> tuple[list[tuple[int, int]], ...]:
    if target_value == 10:
        return tuple(current_paths)
    next_paths: list[list[tuple[int, int]]] = []
    for current_path in current_paths:
        next_coords = get_next_coords(topo_map, current_path[-1], target_value)
        for next_coord in next_coords:
            path: list[tuple[int, int]] = current_path + [next_coord]
            next_paths.append(path)

    return get_next_paths(topo_map, next_paths, target_value + 1)

def get_all_paths_to_peak_from_trailhead(topo_map: list[str], trailhead: tuple[int, int]) -> tuple[list[tuple[int, int]], ...]:
    current_paths: list[list[tuple[int, int]]] = [[trailhead]]
    all_paths: tuple[list[tuple[int, int]], ...] = get_next_paths(topo_map, current_paths)

    return all_paths

def get_peaks_accessible_from_trailhead(topo_map: list[str], trailhead: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    all_paths = get_all_paths_to_peak_from_trailhead(topo_map, trailhead)
    accessible_peaks: set[tuple[int, int]] = set([ path[-1] for path in all_paths ])

    return tuple(accessible_peaks)

def get_count_of_accessible_peaks(topo_map: list[str]) -> int:
    trailheads: tuple[tuple[int, int], ...] = get_trailhead_coords(topo_map)
    accessible_peaks: tuple[int, ...] =  tuple( len(get_peaks_accessible_from_trailhead(topo_map, trailhead)) for trailhead in trailheads )

    return sum(accessible_peaks)

count_of_accessible_peaks: int = get_count_of_accessible_peaks(topo_map)

# Part 1 Solution
print(count_of_accessible_peaks)

def get_all_paths(topo_map: list[str]) -> tuple[tuple[list[tuple[int, int]], ...], ...]:
    trailheads: tuple[tuple[int, int], ...] = get_trailhead_coords(topo_map)
    paths: tuple[tuple[list[tuple[int, int]], ...], ...] = tuple( get_all_paths_to_peak_from_trailhead(topo_map, trailhead) for trailhead in trailheads )

    return paths

all_paths: tuple[tuple[list[tuple[int, int]], ...], ...] = get_all_paths(topo_map)
count_of_all_paths: int = sum([ len(paths) for paths in all_paths ])

# Part 2 Solution
print(count_of_all_paths)