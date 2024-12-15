from math import gcd

with open('day08_input.txt', 'r') as antenna_map_lines:
    antenna_map: list[str] = [ line.replace('\n', '') for line in antenna_map_lines ]

def get_frequencies(antenna_map: list[str]) -> set[str]:
    frequencies: set[str] = set()
    for line in antenna_map:
        frequencies = set( set(line) | frequencies )

    return set( frequency for frequency in frequencies if frequency != '.')

def get_antenna_locations_by_frequency(antenna_map: list[str], frequency: str) -> tuple[tuple[int, int]]:
    antenna_locations: list = []
    for row_index, line in enumerate(antenna_map):
        for column_index, char in enumerate(list(line)):
            if char == frequency:
                antenna_locations = [ (row_index, column_index) ] + antenna_locations
                
    return tuple(antenna_locations)

def get_antinode_locations(ant1: tuple[int, int], ant2: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    ant1_row, ant1_column = ant1
    ant2_row, ant2_column = ant2
    vector: tuple[int, int] = ( ant1_row - ant2_row, ant1_column - ant2_column )
    inverse_vector: tuple[int, int] = ( -1 * vector[0], -1 * vector[1] )

    antinode1_location: tuple[int, int] = (ant1_row + vector[0], ant1_column + vector[1])
    antinode2_location: tuple[int, int] = (ant2_row + inverse_vector[0], ant2_column + inverse_vector[1])

    return (antinode1_location, antinode1_location)

def location_is_on_map(antenna_map: list[str], antinode_location: tuple[int, int]) -> bool:
    rows, columns = len(antenna_map), len(antenna_map[0])
    row, column = antinode_location
    in_row: bool = 0 <= row < rows
    in_column: bool = 0<= column < columns

    return in_row and in_column

frequencies: set[str] = get_frequencies(antenna_map)

def get_all_antinode_locations(antenna_map: list[str]) -> set[tuple[int, int]]:
    antinode_locations: set[tuple[int, int]] = set()
    for frequency in frequencies:
        antenna_locations: tuple[tuple[int, int]] = get_antenna_locations_by_frequency(antenna_map, frequency)
        for ant1 in antenna_locations:
            for ant2 in antenna_locations:
                if ant1 != ant2:
                    antinode_locations = set(set(get_antinode_locations(ant1, ant2)) | antinode_locations)
    
    return antinode_locations

antinode_locations: set[tuple[int, int]] = get_all_antinode_locations(antenna_map)
valid_antinode_locations: tuple[tuple[int, int], ...] = tuple( 
    antinode_location for antinode_location in antinode_locations 
    if location_is_on_map(antenna_map, antinode_location))
count_of_valid_antinode_locations: int = len(valid_antinode_locations)

# Part 1 Solution
print(count_of_valid_antinode_locations)

def get_antenna_vector(ant1: tuple[int, int], ant2: tuple[int, int]) -> tuple[int, int]:
    ant1_row, ant1_column = ant1
    ant2_row, ant2_column = ant2
    vector: tuple[int, int] = ( ant1_row - ant2_row, ant1_column - ant2_column )

    return vector

def get_antinodes_on_vector(antenna_map: list[str], vector: tuple[int, int], antenna: tuple[int, int]) -> set[tuple[int, int]]:
    antinodes_on_vector: set[tuple[int, int]] = set()
    row, column = antenna
    y_diff, x_diff = vector
    vector_gcd: int = gcd(y_diff, x_diff)
    next_diff: tuple[int, int] = (int(y_diff/vector_gcd), int(x_diff/vector_gcd))
    next_coord: tuple[int, int] = (row + next_diff[0], column + next_diff[1])
    while location_is_on_map(antenna_map, next_coord):
        antinodes_on_vector.add(next_coord)
        row, column = next_coord
        next_coord = (row + next_diff[0], column + next_diff[1])
    
    return antinodes_on_vector

def get_harmonic_antinodes(antenna_map: list[str]) -> set[tuple[int, int]]:
    harmonic_antinodes: set[tuple[int, int]] = set()
    for frequency in get_frequencies(antenna_map):
        antenna_locations: tuple[tuple[int, int]] = get_antenna_locations_by_frequency(antenna_map, frequency)
        if len(antenna_locations) > 1:
            harmonic_antinodes = set( harmonic_antinodes | set(antenna_locations) )
        for ant1 in antenna_locations:
            for ant2 in antenna_locations:
                if ant1 != ant2:
                    vector: tuple[int, int] = get_antenna_vector(ant1, ant2)
                    harmonic_antinodes = set( harmonic_antinodes | get_antinodes_on_vector(antenna_map, vector, ant1)) #type: ignore[arg-type]
    return harmonic_antinodes

harmonic_antinodes: set[tuple[int, int]] = get_harmonic_antinodes(antenna_map)
count_of_all_antinodes: int = len(harmonic_antinodes)

# Part 2 Solution
print(count_of_all_antinodes)