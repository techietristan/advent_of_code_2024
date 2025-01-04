with open('day12_input.txt', 'r') as garden_map_file:
    garden_map: list[str] = [ line.strip() for line in garden_map_file ]

rows, columns = len(garden_map), len(garden_map[0])    

def get_coords_if_on_map(row: int, column: int) -> tuple[int, int] | None:
    if 0 <= row < rows and 0 <= column < columns:
        return row, column
    else:
        return None

def get_neighbors(row: int, column: int) -> tuple[tuple[int, int], ...]:
    neighbors: tuple[tuple[int, int] | None, ...] = tuple( neighbor for neighbor in 
        (
            get_coords_if_on_map(row - 1,   column),
            get_coords_if_on_map(row,       column + 1),
            get_coords_if_on_map(row + 1,   column),
            get_coords_if_on_map(row,       column - 1)
        ) 
        if bool(neighbor)
    )

    return neighbors #type: ignore[return-value]

def get_plot_attributes(row: int, column: int) -> dict:
    name: str = f'{row}-{column}'
    plant_type: str = garden_map[row][column]
    region: str | None = None
    neighbors: tuple[tuple[int, int], ...] = get_neighbors(row, column)
    return {
        'name': name,
        'coords': (row, column),
        'plant_type': plant_type,
        'region': region,
        'neighbors': neighbors
    }

def get_plots() -> dict:
    plots: dict = {}
    for row in range(rows):
        for column in range(columns):
            name: str = f'{row}-{column}'
            plots[name] = get_plot_attributes(row, column)

    return plots

plots: dict = get_plots()

def get_neighbor_attributes(neighbor_coords: tuple[int, int]):
    row, column = neighbor_coords
    return plots[f'{row}-{column}']

def get_region(plot: dict) -> str:
    neighbors: tuple[tuple[int, int], ...] = plot['neighbors']
    plant_type: str = plot['plant_type']
    for neighbor_coords in neighbors:
        neighbor: dict = get_neighbor_attributes(neighbor_coords)
        if neighbor['plant_type'] == plant_type and bool(neighbor['region']):
            return neighbor['region']
    return f'{plot['plant_type']}-{plot['name']}'

def update_region(plot: dict) -> None:
    name: str = plot['name']
    region: str = plot['region']
    if not bool(region):
        plots[name]['region'] = get_region(plot)

def remove_plot(region_queue: list[dict], plot: dict) -> list[dict]:
    plot_name: str = plot['name']
    return [ plot for plot in region_queue if plot['name'] != plot_name ]

def search_region(plot_attrs: dict) -> None:
    region_queue: list[dict] = [plot_attrs]
    while True:
        if not bool(region_queue):
            break
        for plot in region_queue:
            neighbors = plot['neighbors']
            plant_type: str = plot['plant_type']
            region_queue = remove_plot(region_queue, plot)
            for neighbor_coords in neighbors:
                neighbor: dict = get_neighbor_attributes(neighbor_coords)
                neighbor_name: str = neighbor['name']
                neighbor_region: str = neighbor['region']
                neighbor_plant_type: str = neighbor['plant_type']
                if not bool(neighbor_region) and neighbor_plant_type == plant_type:
                    region_queue.append(neighbor)
                    plots[neighbor_name]['region'] = get_region(neighbor)            
            
def assign_regions() -> None:
    for key, value in plots.items():
        plot: dict = plots[key]
        update_region(plot)
        search_region(plot)

def get_regions() -> set[str]:
    regions: set[str] = set( plot['region'] for plot in plots.values() )

    return regions

def get_region_coords(region: str) -> tuple[tuple[int, int], ...]:
    region_coords: list[tuple[int, int]] = []
    for plot in plots.values():
        plot_region: str = plot['region']
        if plot_region == region:
            plot_coords: tuple[int, int] = plot['coords'] 
            region_coords.append(plot_coords)

    return tuple(region_coords)

def get_plot_boundaries(plot: tuple[int, int]) -> dict:
    plot_row, plot_column = plot
    north: tuple[int, int, int, int, str] = ( plot_row -1 , plot_column, plot_row, plot_column, 'north' )
    west: tuple[int, int, int, int, str] = ( plot_row, plot_column, plot_row, plot_column + 1, 'west' )
    south: tuple[int, int, int, int, str] = ( plot_row, plot_column, plot_row + 1, plot_column, 'south' )
    east: tuple[int, int, int, int, str] = ( plot_row, plot_column - 1, plot_row, plot_column, 'east' )

    return {
        'north': north,
        'west': west,
        'south': south,
        'east': east
    }

def plot_boundary_is_shared(first_plot_boundary: tuple[int, int, int, int, str], second_plot_boundary: tuple[int, int, int, int, str]) -> bool:
    return bool(first_plot_boundary[0:4] != second_plot_boundary[0:4])

def get_region_boundaries(region_name: str) -> list[tuple[int, int, int, int, str]]:
    region_coords: tuple[tuple[int, int], ...] = get_region_coords(region_name)
    region_boundaries: list[tuple[int, int, int, int, str]] = []
    for plot in region_coords:
        plot_boundaries: dict = get_plot_boundaries(plot)
        for plot_boundary in plot_boundaries.values():
            region_boundaries.append(plot_boundary)
    region_boundary_coords: tuple[tuple[int, int, int, int], ...] = tuple([ region_boundary[0:4] for region_boundary in region_boundaries ])
    
    for region_boundary in region_boundaries:
        if region_boundary_coords.count(region_boundary[0:4]) > 1:
            region_boundaries = [ boundary for boundary in region_boundaries if boundary[0:4] != region_boundary[0:4] ]

    return region_boundaries

def get_region_area(region: str) -> int:
    region_coords: tuple[tuple[int, int], ...] = get_region_coords(region)

    return len(region_coords)

def get_region_perimeter(region: str) -> int:
    region_boundaries: list[tuple[int, int, int, int, str]] = get_region_boundaries(region)
    return len(region_boundaries)

def get_region_fencing_cost(region: str) -> int:
    region_area: int = get_region_area(region)
    region_perimeter: int = get_region_perimeter(region)

    return region_area * region_perimeter

def get_total_fencing_cost() -> int:
    regions: set[str] = get_regions()
    region_fencing_costs: tuple[int, ...] = tuple([ get_region_fencing_cost(region) for region in regions ])
    total_fencing_cost: int = sum(region_fencing_costs)

    return total_fencing_cost

assign_regions()
total_fencing_cost: int = get_total_fencing_cost()

# Part 1 Solution
print(total_fencing_cost)

def get_boundary_orientation(boundary: tuple[int, int, int, int, str]) -> str:
    return 'vertical' if boundary[0] == boundary[2] else 'horizontal'

def get_boundaries_by_orientation(boundaries: list[tuple[int, int, int, int, str]], orientation: str) -> list[tuple[int, int, int, int, str]]:
    sort_index: int = 0 if orientation == 'horizontal' else 1
    return sorted([ 
        boundary for boundary in boundaries 
        if get_boundary_orientation(boundary) == orientation ], 
        key = lambda boundary: boundary[sort_index])

def get_distinct_edge_count(boundaries: list[tuple[int, int, int, int, str]], axis: int) -> int:
    edge_count: int = 0
    edge_coords: list[tuple[int, str]] = [ (boundary[axis], boundary[4]) for boundary in boundaries ] #type: ignore[misc]
    for edge_coord in edge_coords:
        if (edge_coord[0] + 1, edge_coord[1]) not in edge_coords:
            edge_count += 1

    return edge_count

def get_edge_count(boundaries: list[tuple[int, int, int, int, str]]) -> int:
    edge_count: int = 0
    horizontal_boundaries: list[tuple[int, int, int, int, str]] = get_boundaries_by_orientation(boundaries, 'horizontal')
    vertical_boundaries: list[tuple[int, int, int, int, str]] = get_boundaries_by_orientation(boundaries, 'vertical')
    horizontal_edge_axes: list[int] = sorted(list(set( boundary[0] for boundary in horizontal_boundaries )))
    vertical_edge_axes: list[int] = sorted(list(set( boundary[1] for boundary in vertical_boundaries )))
    horizontal_edge_count, vertical_edge_count = 0, 0

    for horizontal_edge_axis in horizontal_edge_axes:
        potential_horizontal_edges = [ boundary for boundary in horizontal_boundaries if boundary[0] == horizontal_edge_axis ]
        horizontal_edge_count += get_distinct_edge_count(potential_horizontal_edges, 1)
    
    for vertical_edge_axis in vertical_edge_axes:
        potential_vertical_edges = [ boundary for boundary in vertical_boundaries if boundary[1] == vertical_edge_axis ]
        vertical_edge_count += get_distinct_edge_count(potential_vertical_edges, 2)
    
    return horizontal_edge_count + vertical_edge_count

def get_discounted_fence_cost() -> int:
    fence_cost: int = 0
    regions: set[str] = get_regions()
    for region in regions:
        region_area: int = len([ plot for plot in plots.values() if plot['region'] == region ])
        region_boundaries: list[tuple[int, int, int, int, str]] = get_region_boundaries(region)
        region_edge_count: int = get_edge_count(region_boundaries)
        fence_cost += region_edge_count * region_area
    
    return fence_cost

discounted_fence_cost: int = get_discounted_fence_cost()

# Part 2 Solution
print(discounted_fence_cost)