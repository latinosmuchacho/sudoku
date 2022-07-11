import typing as tp
import pathlib

T = tp.TypeVar("T")
NUMBERS = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
STEP = 0


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """
        Reading sudoku from the specified file
    """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)

def print_answer(grid: tp.List[tp.List[str]]) -> None:
    result_text = ""
    for line in grid:
        for elem in line:
            result_text += f"{elem} "
        result_text += "\n"
    path = pathlib.Path("output.txt")
    with open("output.txt", "w") as f:
        f.write(result_text)




def group(values: tp.List[T], n: int) -> tp.List[tp.List[str]]:
    result_list = []
    number_line = len(values) // n
    for i in range(number_line):
        result_line = []
        for j in range(n):
            result_line.append(values[i * n + j])
        result_list.append(result_line)
    return result_list


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    result_col = []
    for line in grid:
        result_col.append(line[pos[1]])
    return result_col


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    start_row = pos[0] // 3 * 3
    start_col = pos[1] // 3 * 3
    end_row = start_row + 3
    end_col = start_col + 3
    # print(f"start_row:  {start_row}")
    # print(f"start_col:  {start_col}")
    # print(f"end_row:  {end_row}")
    # print(f"end_col:  {end_col}")
    block = []
    for i in range(start_row, end_row):
        for j in range(start_col, end_col):
            block.append(grid[i][j])
    return block


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    global STEP
    STEP += 1
    print(STEP)
    pos = find_empty_positions(grid)
    if pos == (10, 10):
        return grid
    possible_values = find_possible_values(grid, pos)
    if len(possible_values) == 0:
        return -1
    for possible_value in possible_values:
        grid[pos[0]][pos[1]] = possible_value
        result_solve = solve(grid)
        if result_solve == -1:
            continue
        else:
            return grid
    grid[pos[0]][pos[1]] = "."
    return -1


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """
    Find the first free position in the puzzle
    """
    row = 0
    col = 0
    for line in grid:
        for element in line:
            if element == '.':
                return (row, col)
            else:
                col += 1
        row += 1
        col = 0
    return 10, 10


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """
    Return the set of all possible values for the specified position
    """
    row = set(get_row(grid, pos))
    col = set(get_col(grid, pos))
    block = set(get_block(grid, pos))
    return NUMBERS - row - col - block

grid = read_sudoku("input.txt")
result = solve(grid)
print_answer(result)


