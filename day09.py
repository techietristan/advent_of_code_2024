with open('day09_input.txt', 'r') as disk_map_file:
    disk_map: str = [ line for line in disk_map_file ][0]

def get_alternating_blocks(remainder: int) -> tuple[int, ...]:
    alternating_blocks: tuple[int, ...] = tuple([ 
        int(block) for index, block in enumerate(disk_map) 
        if index % 2 == remainder and bool(block)
    ])
    return alternating_blocks

def get_file_blocks(block_lengths: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:

    file_blocks: tuple[tuple[int, ...], ...] = tuple([ 
        tuple( index for _ in range(block_length))
        for index, block_length in enumerate(block_lengths)
    ])
    return file_blocks

def get_block_indices(file_blocks: tuple[int, ...]) -> tuple:
    pointer: int = 0
    block_indices: list[tuple[int, int]] = list()
    for file_block in file_blocks:
        start, end = pointer, pointer + file_block
        block_index: tuple[int, int] = (start, end)
        block_indices.append(block_index)
        pointer = end
    return tuple(block_indices)

def get_block_from_indices(indices: tuple[int, int], block_indices: tuple) -> tuple[int, ...]:
    start, end = indices
    return block_indices[start : end] #type: ignore

def get_non_contiguous_file_blocks(file_blocks: tuple[int, ...], reversed_file_ids: tuple) -> tuple:
    block_indices: tuple = get_block_indices(file_blocks)
    non_contiguous_file_blocks: tuple[tuple[int, ...], ...] = tuple([
        get_block_from_indices(block_index, reversed_file_ids)
        for index, block_index in enumerate(block_indices)
    ])
    return non_contiguous_file_blocks

def unnest(file_ids: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    unnested: list[int] = list()
    for indices in file_ids:
        for index in indices:
            unnested.append(index)
    return tuple(unnested)

def reverse(file_ids: tuple) -> tuple:
    reversed_file_ids: tuple[int, ...] = tuple(file_ids[::-1]) #type: ignore[index]
    return reversed_file_ids

def fill_alternating(file_ids: tuple[tuple[int, ...], ...], reversed_file_ids: tuple) -> tuple[int, ...]:
    least_blocks: int = min(len(file_ids), len(reversed_file_ids))
    alternating: list[tuple[int, ...]] = list()
    for index in range(least_blocks):
        alternating.append(file_ids[index]) #type: ignore[arg-type]
        alternating.append(reversed_file_ids[index]) #type: ignore[arg-type]
    return (unnest(tuple(alternating)))

file_blocks: tuple[int, ...] = get_alternating_blocks(0)
empty_blocks: tuple[int, ...] = get_alternating_blocks(1)
contiguous_file_blocks: tuple[tuple[int, ...], ...] = get_file_blocks(file_blocks)
reversed_file_ids: tuple = reverse(unnest(contiguous_file_blocks))
non_contiguous_file_blocks: tuple = get_non_contiguous_file_blocks(empty_blocks, reversed_file_ids)
contiguous_data_length: int = sum(len(file_block) for file_block in contiguous_file_blocks)
alternating: tuple[int, ...] = fill_alternating(contiguous_file_blocks, non_contiguous_file_blocks)[:contiguous_data_length]
checksums: tuple[int, ...] = tuple( index * int(id) for index, id in enumerate(alternating))
sum_of_checksums: int = sum(checksums)

# Part 1 Solution
print(sum_of_checksums)

reversed_nested_file_ids: tuple[tuple[int, ...], ...] = reverse(contiguous_file_blocks)

def fill_empty_block(empty_block: int, file_ids: list[tuple[int, ...]], empty_block_index: int) -> tuple[tuple[int, ...], list[tuple[int, ...]]]:
    block_contents: list[int] = []
    empty_space_remaining: int = empty_block
    for index, file_id in enumerate(file_ids):
        number_of_file_ids: int = len(file_id)
        file_will_fit: bool = number_of_file_ids <= empty_space_remaining
        file_has_contents: bool = any(file_id)
        file_moves_left: bool = index + 1 < len(file_ids) - empty_block_index
        if file_will_fit and file_has_contents and file_moves_left:
            empty_space_remaining -= number_of_file_ids
            block_contents.extend(file_id)
            file_ids[index] = tuple([ 0 for _ in range(len(file_id))])
            if empty_space_remaining == 0:
                return tuple(block_contents), file_ids
    block_contents.extend([ 0 for _ in range(empty_space_remaining)])
    return tuple(block_contents), file_ids

def fill_empty_blocks(empty_blocks: tuple[int, ...], file_ids: tuple[tuple[int, ...], ...]) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    filled_blocks: list[tuple[int, ...]] = []
    current_file_ids: list[tuple[int,...]] = list(file_ids)
    for empty_block_index, empty_block in enumerate(empty_blocks):
        filled_block, file_ids = fill_empty_block(empty_block, current_file_ids, empty_block_index) #type: ignore[assignment]
        filled_blocks.append(filled_block)
    return tuple(filled_blocks), file_ids
        
filled_blocks, file_ids = fill_empty_blocks(empty_blocks, reversed_nested_file_ids)

def alternate_filled_blocks(filled_blocks: tuple[tuple[int, ...], ...], file_ids: tuple[tuple[int, ...], ...]):
    file_layout: list[tuple[int, ...]] = []
    reversed_remaining: tuple[tuple[int,...]] = tuple([ remaining_id for remaining_id in reverse(file_ids) ]) #type: ignore[arg-type]
    more_remaining: bool = len(reversed_remaining) > len(filled_blocks)
    for index, filled_block in enumerate(filled_blocks):
        file_layout.append(reversed_remaining[index])
        file_layout.append(filled_block)
    if more_remaining:
        file_layout.append(reversed_remaining[-1])

    return unnest(tuple(file_layout))

file_layout: tuple[int, ...] = alternate_filled_blocks(filled_blocks, file_ids)
sum_of_checksums_compacted = sum([ index * value for index, value in enumerate(file_layout)])

# Part 2 Solution
print(sum_of_checksums_compacted)
