from copy import deepcopy
from sys import setrecursionlimit
from typing import Callable

import multiprocessing

with open('day06_input.txt', 'r') as guard_map_contents:
    guard_map: list[str] = [ line.replace('\n', '') for line in guard_map_contents ]

guard_map_rows, guard_map_columns = len(guard_map), len(guard_map[0])
maximum_recursion_depth: int = guard_map_rows * guard_map_columns
setrecursionlimit(maximum_recursion_depth)

guard_orientations: list[str] = ['^', '>', 'v', '<']

def get_guard_location_and_orientation(guard_map: list[str]) -> tuple[int, int, str] | None:
    for row_index, row in enumerate(guard_map):
        for guard_orientation in guard_orientations:
            if guard_orientation in row:
                return (row_index, row.index(guard_orientation), guard_orientation)
    return None

def get_next_coords(guard_map: list[str], orientation: str, coords: tuple[int, int]) -> tuple[int, int]:  
    next_move_diffs: dict = {
        '^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1)
    }
    next_move_diff: tuple[int, int] = next_move_diffs[orientation]
    next_coords: tuple[int, int] = ( coords[0] + next_move_diff[0], coords[1] + next_move_diff[1])

    return next_coords

def get_next_orientation(current_orientation: str):
    current_orientation_index: int = guard_orientations.index(current_orientation)
    if current_orientation_index + 1 == len(guard_orientations):
        return guard_orientations[0]
    return guard_orientations[current_orientation_index + 1]

def get_next_move(guard_map: list[str], current_orientation: str, current_coords: tuple[int, int]) -> str:
    rows, columns = len(guard_map), len(guard_map[0])
    next_coords_contain_barrier: bool = True
    while next_coords_contain_barrier:
        next_coords: tuple[int, int] = get_next_coords(guard_map, current_orientation, current_coords)
        next_row, next_column = next_coords
        next_move_is_exit: bool = next_row < 0 or next_column < 0 or next_row == rows or next_column == columns
        if next_move_is_exit:
            return 'exit'
        next_coords_contain_barrier = guard_map[next_row][next_column] == '#'  
        current_orientation = get_next_orientation(current_orientation) if next_coords_contain_barrier else current_orientation
    return current_orientation

def add_coords_to_visited_set(
    guard_map: list[str], 
    current_coords: tuple[int, int], 
    current_orientation: str, 
    visited: set[tuple[int, int]] = set()
    ) -> set[tuple[int, int]]:

    updated_visited: set[tuple[int, int]] = set(list(visited) + [current_coords])
    next_move: str = get_next_move(guard_map, current_orientation, current_coords)
    if next_move == 'exit':
        return updated_visited
    next_orientation: str = next_move
    next_coords: tuple[int, int] = get_next_coords(guard_map, next_orientation, current_coords)
    return add_coords_to_visited_set(guard_map, next_coords, next_orientation, updated_visited)

initial_guard_location_and_orientation: tuple[int, int, str] | None = get_guard_location_and_orientation(guard_map)
initial_row, initial_column, initial_orientation = initial_guard_location_and_orientation #type: ignore[misc]
visited_coords: set[tuple[int, int]] = add_coords_to_visited_set(guard_map, (initial_row, initial_column), initial_orientation)
visited_positions_count: int = len(visited_coords)

# Part 1 Solution
print(visited_positions_count)

potential_obstacle_locations: tuple[tuple[int,int], ...] = tuple(set( visited_coord for visited_coord in visited_coords if visited_coord != (initial_row, initial_column)))
count_of_potential_obstacle_locations: int = len(potential_obstacle_locations)

def get_updated_guard_map(guard_map: list[str], obstacle_coords: tuple[int, int]) -> list[str]:
    obstacle_row, obstacle_column = obstacle_coords
    guard_map_copy: list[str] = deepcopy(guard_map)
    obstacle_row_contents: list[str] = [ char for char in guard_map_copy[obstacle_row] ]
    obstacle_row_contents[obstacle_column] = '#'
    guard_map_copy[obstacle_row] = ''.join(obstacle_row_contents)

    return guard_map_copy

def get_coords_at_which_obstacle_creates_loop(index: int) -> tuple[int, int] | bool:
    obstacle_coords: tuple[int, int] = potential_obstacle_locations[index]
    if obstacle_coords == (initial_row, initial_column):
        return False
    updated_guard_map: list[str] = get_updated_guard_map(guard_map, obstacle_coords)
    current_state: tuple[tuple[int, int], str] = ((initial_row, initial_column), initial_orientation)
    previous_states: set[tuple[tuple[int, int], str]] = set()
    while current_state not in previous_states:
        previous_states = set( list(previous_states) + [current_state] )
        current_coords, current_orientation = current_state[0], current_state[1]
        next_move: str = get_next_move(updated_guard_map, current_orientation, current_coords)
        if next_move == 'exit':
            return False
        next_coords: tuple[int, int] = get_next_coords(updated_guard_map, next_move, current_coords)
        current_state = (next_coords, next_move) 
    return obstacle_coords

def get_pool() -> Callable:
    try:
        cpu_count: int = multiprocessing.cpu_count()
    except NotImplementedError:
        cpu_count = 2
    pool: Callable = multiprocessing.Pool(processes = cpu_count) #type: ignore[assignment]

    return pool 

pool = get_pool()
coords_at_which_obstacle_creates_loop: list[tuple[int,int] | bool] = pool.map( #type: ignore[attr-defined]
    get_coords_at_which_obstacle_creates_loop, range(count_of_potential_obstacle_locations)
)
unique_obstacle_coords: set[tuple[int,int]] = set([ coord for coord in coords_at_which_obstacle_creates_loop if bool(coord)]) #type: ignore[misc]
count_of_loop_causing_obstacles: int = len(unique_obstacle_coords)

# Part 2 Solution
print(count_of_loop_causing_obstacles)