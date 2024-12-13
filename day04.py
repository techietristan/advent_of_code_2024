import re

with open('day04_input.txt', 'r') as word_search_content:
    word_search_array: list[str] = [ line.replace('\n', '') for line in word_search_content ][1174:1180] 

def get_xmas_count(line: str) -> int:
    xmas_matches = re.findall(r'xmas', line.lower())
    return len(xmas_matches)

def get_next_coords(row: int, column: int, rows: int, columns: int, go_to_next_row: bool = False) -> tuple[int, int,  bool] | None:
    at_top: bool = row - 1 < 0
    at_end: bool = column + 1 == columns
    go_to_next_row = True if at_top or at_end else False
    reached_last_row: bool = column + 1 == rows
    is_final_coord: bool = row +1 == rows and column + 1 == columns
    next_row =      row - 1     if not go_to_next_row else rows - 1 if reached_last_row else column + 1
    next_column =   column + 1  if not go_to_next_row else row + 1  if reached_last_row else 0

    if is_final_coord:
        return None
    return next_row, next_column, go_to_next_row

def get_next_line(input_array: list[str], current_row: int = 0, current_column: int = 0, current_line: str = '') -> str:
    rows, columns = len(input_array), len(input_array[0])
    current_char: str = input_array[current_row][current_column]
    next_coords: tuple[int, int, bool] | None = get_next_coords(current_row, current_column, rows, columns)
    if not bool(next_coords):
        return current_char
    next_row, next_column, go_to_next_row = next_coords # type: ignore
    next_line: str = f'{current_line}{current_char}'
    if go_to_next_row:
        return next_line

    return get_next_line(input_array, next_row, next_column, next_line)

def rotate_array_45(input_array: list[str]) -> list[str]:
    rows, columns = len(input_array), len(input_array[0])
    line_beginnings: list[tuple] = [ (row, 0) for row in range(rows) ] + [ (columns - 1, column) for column in range(1, columns) ]
    rotated_array: list[str] = [ get_next_line(input_array, row, column) for row, column in line_beginnings ]

    return rotated_array

def rotate_array_90(input_array: list[str]) -> list[str]:
    return [ ''.join(line) for line in zip(*input_array[::-1]) ]
    
def get_total_xmas_count(input_array: list[str]) -> int:
    original_array: list[str] = input_array
    array_45: list[str] = rotate_array_45(original_array)
    array_90: list[str] = rotate_array_90(original_array)
    array_135: list[str] = rotate_array_45(array_90)
    array_180: list[str] = rotate_array_90(array_90)
    array_225: list[str] = rotate_array_45(array_180)
    array_270: list[str] = rotate_array_90(array_180)
    array_315: list[str] = rotate_array_45(array_270)
    all_lines: list[str] = original_array + array_45 + array_90 + array_135 + array_180 + array_225 + array_270 + array_315
    total_xmas_count: int = sum([get_xmas_count(line) for line in all_lines])

    return total_xmas_count

total_xmas_count: int = get_total_xmas_count(word_search_array)

# Part 1 Solution
print(total_xmas_count)

def tips_contain_m_and_s(tips: str) -> bool:
    return 'm' in tips and 's' in tips

def is_center_of_x_mas(input_array: list[str], row: int, column: int):
    rows, columns = len(input_array), len(input_array[0])
    tip_coords: tuple[tuple[int, int], ...] = (
        (row - 1, column - 1),
        (row - 1, column + 1),
        (row + 1, column - 1),
        (row + 1, column + 1)
    )
    is_edge_row: bool = row == 0 or row + 1 == rows
    is_edge_column: bool = column == 0 or column + 1 == columns
    if is_edge_row or is_edge_column:
        return False

    upper_left, upper_right, lower_left, lower_right = ( input_array[row][column] for row, column in tip_coords )
    first_slash: str = f'{upper_left}{lower_right}'.lower()
    second_slash: str = f'{upper_right}{lower_left}'.lower()

    return bool(tips_contain_m_and_s(first_slash) and tips_contain_m_and_s(second_slash))

def get_a_coords(input_array: list[str]) -> tuple[tuple[int, int], ...]:
    rows, columns = len(input_array), len(input_array[0])
    a_coords: list = []
    
    for row in range(rows):
        for column in range(columns):
            if input_array[row][column].lower() == 'a':
                a_coords.append((row, column))

    return tuple(a_coords)

def get_total_x_masses(input_array: list[str]) -> int:
    a_coords: tuple[tuple[int, int], ...] = get_a_coords(input_array)
    x_mass_coords: list = [ (row, column) for (row, column) in a_coords if is_center_of_x_mas(input_array, row, column) ]
    total_x_masses: int = len(x_mass_coords)

    return total_x_masses

total_x_masses: int = get_total_x_masses(word_search_array)

# Part 2 Solution:
print(total_x_masses)


# class TestGetNextCoords(TestCase):
 
#     def test_get_next_coords_top_1(self):
#         row, column, rows, columns, expected_result = (0, 0, 10, 10, (1, 0, True))
#         result = get_next_coords(row, column, rows, columns)
#         self.assertEqual(result, expected_result)
    
#     def test_get_next_coords_top_2(self):
#         row, column, rows, columns, expected_result = (0, 9, 10, 10, (9, 1, True))
#         result = get_next_coords(row, column, rows, columns)
#         self.assertEqual(result, expected_result)
    
#     def test_get_next_coords_middle_1(self):
#         row, column, rows, columns, expected_result = (1, 1, 10, 10, (0, 2, False))
#         result = get_next_coords(row, column, rows, columns)
#         self.assertEqual(result, expected_result)
    
#     def test_get_next_coords_middle_2(self):
#         row, column, rows, columns, expected_result = (1, 0, 10, 10, (0, 1, False))
#         result = get_next_coords(row, column, rows, columns)
#         self.assertEqual(result, expected_result)
    
#     def test_get_next_coords_end_1(self):
#         row, column, rows, columns, expected_result = (1, 9, 10, 10, (9, 2, True))
#         result = get_next_coords(row, column, rows, columns)
#         self.assertEqual(result, expected_result)
    
#     def test_get_next_coords_end_2(self):
#         row, column, rows, columns, expected_result = (8, 9, 10, 10, (9, 9, True))
#         result = get_next_coords(row, column, rows, columns)
#         self.assertEqual(result, expected_result)

#     def test_get_next_coords_end_3(self):
#         row, column, rows, columns, expected_result = (7, 9, 10, 10, (9, 8, True))
#         result = get_next_coords(row, column, rows, columns)
#         self.assertEqual(result, expected_result)

#     def test_get_next_coords_final_coord(self):
#         row, column, rows, columns = (9, 9, 10, 10)
#         result = get_next_coords(row, column, rows, columns)
#         self.assertIsNone(result)
            
# class TestGetNextLine(TestCase):
#     test_input: str = """
#         MMMSXXMASM
#         MSAMXMSMSA
#         AMXSXMAAMM
#         MSAMASMSMX
#         XMASAMXAMM
#         XXAMMXXAMA
#         SMSMSASXSS
#         SAXAMASAAA
#         MAMMMXMMMM
#         MXMXAXMASX
#     """

#     test_array: list[str] = [ line.strip() for line in test_input.split('\n') if bool(line.strip()) ]

#     def test_get_next_line_first(self):
#         result = get_next_line(self.test_array, 0, 0, '')
#         self.assertEqual(result, 'M')
    
#     def test_get_next_line_second(self):
#         result = get_next_line(self.test_array, 1, 0, '')
#         self.assertEqual(result, 'MM')
    
#     def test_get_next_line_last_before_corner(self):
#         result = get_next_line(self.test_array, 8, 0, '')
#         self.assertEqual(result, 'MASMASAMS')
    
#     def test_get_next_line_corner(self):
#         result = get_next_line(self.test_array, 9, 0, '')
#         self.assertEqual(result, 'MAXMMMMASM')
    
#     def test_get_next_line_first_after_corner(self):
#         result = get_next_line(self.test_array, 9, 1, '')
#         self.assertEqual(result, 'XMASXXSMA')
    
#     def test_get_next_line_second_to_last(self):
#         result = get_next_line(self.test_array, 9, 8, '')
#         self.assertEqual(result, 'SM')

#     def test_get_next_line_last(self):
#         result = get_next_line(self.test_array, 9, 9, '')
#         self.assertEqual(result, 'X')

# class TestRotateArray45(TestCase):

#     test_input: str = """
#         MMM
#         MSA
#         AMX
#     """
#     test_array: list[str] = [ line.strip() for line in test_input.split('\n') if bool(line.strip()) ]

#     def test_rotate_array_45(self):
#         expected_array = [
#             'M',
#             'MM',
#             'ASM',
#             'MA',
#             'X'
#         ]
#         returned_array = rotate_array_45(self.test_array)
#         self.assertEqual(expected_array, returned_array)

# class Test_Get_Total_Xmas_count(TestCase):

#     test_input: str = """
#         MMMSXXMASM
#         MSAMXMSMSA
#         AMXSXMAAMM
#         MSAMASMSMX
#         XMASAMXAMM
#         XXAMMXXAMA
#         SMSMSASXSS
#         SAXAMASAAA
#         MAMMMXMMMM
#         MXMXAXMASX
#     """

#     test_array: list[str] = [ line.strip() for line in test_input.split('\n') if bool(line.strip()) ]

#     def test_get_total_xmas_count(self):
#         expected_xmas_count = 18
#         total_xmas_count = get_total_xmas_count(self.test_array)

#         self.assertEqual(expected_xmas_count, total_xmas_count)

# class TestIsCenterOfXMas(TestCase):

#     test_input: str = """
#         MMMSXXMASM
#         MSAMXMSMSA
#         AMXSXMAAMM
#         MSAMASMSMX
#         XMASAMXAMM
#         XXAMMXXAMA
#         SMSMSASXSS
#         SAXAMASAAA
#         MAMMMXMMMM
#         MXMXAXMASX
#     """

#     test_array: list[str] = [ line.strip() for line in test_input.split('\n') if bool(line.strip()) ]

#     def test_is_center_of_x_mas(self):
#         result: bool = is_center_of_x_mas(self.test_array, 1, 2)

#         self.assertTrue(result)
    
#     def test_is_not_center_of_x_mas(self):
#         corner_result_1: bool = is_center_of_x_mas(self.test_array, 0, 0)
#         corner_result_2: bool = is_center_of_x_mas(self.test_array, 0, 9)
#         corner_result_3: bool = is_center_of_x_mas(self.test_array, 9, 0)
#         corner_result_4: bool = is_center_of_x_mas(self.test_array, 9, 9)
#         edge_result: bool = is_center_of_x_mas(self.test_array, 5, 0)
#         negative_result: bool = is_center_of_x_mas(self.test_array, 8, 7)

#         self.assertFalse(corner_result_1)
#         self.assertFalse(corner_result_2)
#         self.assertFalse(corner_result_3)
#         self.assertFalse(corner_result_4)
#         self.assertFalse(edge_result)
#         self.assertFalse(negative_result)

# class TestGetACoords(TestCase):

#     test_input: str = """
#         MMMS
#         MSAM
#         AMXS
#     """

#     test_array: list[str] = [ line.strip() for line in test_input.split('\n') if bool(line.strip()) ]

#     def test_get_a_coords(self):
#         a_coords_result: tuple(tuple[int, int], ...) = get_a_coords(self.test_array)
#         expected_a_coords: tuple(tuple[int, int], ...) = ((1, 2), (2, 0))

#         self.assertTupleEqual(a_coords_result, expected_a_coords)

# class TestGetTotalXMasses(TestCase):

#     test_input: str = """
#         MMMSXXMASM
#         MSAMXMSMSA
#         AMXSXMAAMM
#         MSAMASMSMX
#         XMASAMXAMM
#         XXAMMXXAMA
#         SMSMSASXSS
#         SAXAMASAAA
#         MAMMMXMMMM
#         MXMXAXMASX
#     """

#     test_array: list[str] = [ line.strip() for line in test_input.split('\n') if bool(line.strip()) ]

#     def test_get_total_x_masses(self):
#         expected_xmases_count: int = 9
#         xmases_count: int = get_total_x_masses(self.test_array)
        
#         self.assertEqual(expected_xmases_count, xmases_count)