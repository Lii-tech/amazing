from typing import TYPE_CHECKING
from enum import Enum
from .pattern import pattern_cells

if TYPE_CHECKING:
    from .maze_generator import MazeGenerator

RESET = "\033[0m"
BOLD = "\033[1m"
#MAZE_BG = "\033[48;2;255;242;204m"


class Chars(Enum):
    """Every wall/junction glyph renders as a solid block; there is no
    real distinction between corner/edge/cross types, so this is the
    single source of truth instead of 12 aliased names for one value."""
    WALL = "█"
    EMPTY = " "


def print_canvas(canvas: list[list[str]]) -> None:
    # Terminal fonts are roughly 2x taller than they are wide, so a
    # square-ish character grid prints visibly taller than it is wide.
    # Doubling every cell horizontally corrects the aspect ratio.
    # Doubling the full (possibly ANSI-wrapped) cell string is safe:
    # the escape codes just re-apply the same color state twice.
    for row in canvas:
        print("".join(cell * 2 for cell in row) + RESET)
    print(RESET, end="")


def coloring_entry_exit(canvas: list[list[str]], maze: "MazeGenerator", color: str, MAZE_BG: str):
    entr_row = maze.start[0] * 2 + 1
    entr_col = maze.start[1] * 2 + 1

    exit_row = maze.end[0] * 2 + 1
    exit_col = maze.end[1] * 2 + 1

    canvas[entr_row][entr_col] = f"{color} {RESET}{MAZE_BG}"
    canvas[exit_row][exit_col] = f"{color} {RESET}{MAZE_BG}"

    return canvas


def coloring_42(
    canvas: list[list[str]],
    maze: "MazeGenerator",
    color: str,
    MAZE_BG: str
) -> list[list[str]]:

    pattern = set(pattern_cells(maze))

    for row, col in pattern:
        canvas_row = row * 2 + 1
        canvas_col = col * 2 + 1

        # Color the cell itself
        canvas[canvas_row][canvas_col] = f"{color} {RESET}{MAZE_BG}"

        # Connect to the cell on the right, but never paint over a wall
        if (row, col + 1) in pattern and canvas[canvas_row][canvas_col + 1] != Chars.WALL.value:
            canvas[canvas_row][canvas_col + 1] = f"{color} {RESET}{MAZE_BG}"

        # Connect to the cell below, but never paint over a wall
        if (row + 1, col) in pattern and canvas[canvas_row + 1][canvas_col] != Chars.WALL.value:
            canvas[canvas_row + 1][canvas_col] = f"{color} {RESET}{MAZE_BG}"

    return canvas


def color_walls(canvas: list[list[str]], color: str, MAZE_BG: str) -> list[list[str]]:
    rows = len(canvas)
    cols = len(canvas[0])
    for r in range(rows):
        for c in range(cols):
            is_cell_center = (r % 2 == 1 and c % 2 == 1)
            if is_cell_center:
                continue
            if canvas[r][c]:
                canvas[r][c] = f"{color}{canvas[r][c]}{RESET}{MAZE_BG}"
    return canvas


def colored_path(
    canvas: list[list[str]],
    path: list[tuple[int, int]],
    color: str,
    MAZE_BG: str
) -> list[list[str]]:

    for i in range(len(path)):
        row, col = path[i]

        canvas_row = row * 2 + 1
        canvas_col = col * 2 + 1

        # Color the cell
        canvas[canvas_row][canvas_col] = f"{color} {RESET}{MAZE_BG}"

        # Connect to the next cell
        if i + 1 < len(path):
            next_row, next_col = path[i + 1]

            if next_col == col + 1:      # moving right
                canvas[canvas_row][canvas_col + 1] = f"{color} {RESET}{MAZE_BG}"
            elif next_col == col - 1:    # moving left
                canvas[canvas_row][canvas_col - 1] = f"{color} {RESET}{MAZE_BG}"
            elif next_row == row + 1:    # moving down
                canvas[canvas_row + 1][canvas_col] = f"{color} {RESET}{MAZE_BG}"
            elif next_row == row - 1:    # moving up
                canvas[canvas_row - 1][canvas_col] = f"{color} {RESET}{MAZE_BG}"

    return canvas


def colored_cell(
    canvas: list[list[str]],
    maze: "MazeGenerator",
    color: str,
    MAZE_BG: str
) -> list[list[str]]:

    for row in range(maze.grid.row):
        for col in range(maze.grid.colm):
            canvas_row = row * 2 + 1
            canvas_col = col * 2 + 1
            canvas[canvas_row][canvas_col] = f"{MAZE_BG}{color} {RESET}{MAZE_BG}"

    return canvas


def convert_to_binary(path: str):
    with open(path, "r") as file:
        binary = []
        for line in file:
            if line.startswith("("):
                break
            for digit in line.strip():
                b = int(digit, 16)
                b = bin(b)[2:]
                binary.append(b.zfill(4))
    return binary


def put_the_walls(binary):
    walls = []
    for i in binary:
        cell = []
        if i[0] == "1":
            cell.append("N")
        if i[1] == "1":
            cell.append("E")
        if i[2] == "1":
            cell.append("S")
        if i[3] == "1":
            cell.append("W")
        walls.append(cell)
    return walls


def fix_junctions(canvas: list) -> list:
    rows = len(canvas)
    cols = len(canvas[0])

    for r in range(2, rows - 1, 2):
        for c in range(2, cols - 1, 2):

            directions = ""

            if canvas[r - 1][c] == Chars.WALL.value:
                directions += "N"
            if canvas[r + 1][c] == Chars.WALL.value:
                directions += "S"
            if canvas[r][c + 1] == Chars.WALL.value:
                directions += "E"
            if canvas[r][c - 1] == Chars.WALL.value:
                directions += "W"

            # Any wall meeting here is still just a block; an empty
            # junction (no adjoining walls) stays blank.
            canvas[r][c] = Chars.WALL.value if directions else Chars.EMPTY.value

    return canvas


def border(maze: "MazeGenerator", path: list[tuple[int, int]],
           directions: list[list[str]], file: str,
           color: list[list[str]],
           theme: int, value: int) -> list:

    rows = maze.grid.row * 2 + 1
    cols = maze.grid.colm * 2 + 1

    if cols % 2 == 0:
        cols = cols + 1

    canvas = [[" "] * cols for _ in range(rows)]

    # top
    canvas[0][0] = Chars.WALL.value
    for col in range(1, cols):
        canvas[0][col] = Chars.WALL.value
    canvas[0][cols - 1] = Chars.WALL.value

    # bottom
    canvas[rows - 1][0] = Chars.WALL.value
    for col in range(1, cols - 1):
        canvas[rows - 1][col] = Chars.WALL.value
    canvas[rows - 1][cols - 1] = Chars.WALL.value

    # left + right
    for row in range(1, rows - 1):
        canvas[row][0] = Chars.WALL.value
        canvas[row][cols - 1] = Chars.WALL.value

    wall = color[0][theme]  # wall
    bg = color[5][theme]
    binary = convert_to_binary(file)
    draw_wall = put_the_walls(binary)
    canvas = rendering(canvas, maze, path, draw_wall,
                        maze.grid.row, maze.grid.colm,
                        color, theme, value)
    canvas = fix_junctions(canvas)
    canvas = color_walls(canvas, wall, bg)
    return canvas


def rendering(canvas: list[list[str]], maze: "MazeGenerator",
              path: list[tuple[int, int]],
              draw_wall: list[list[str]],
              rows: int, cols: int, color: str,
              theme: int, value: int) -> list[list[str]]:
    # cell_number tells you WHICH cell, walls tells you WHICH directions
    maze_cols = cols
    for cell_number, walls in enumerate(draw_wall):
        cell_row = cell_number // maze_cols
        cell_col = cell_number % maze_cols
        canvas_row = cell_row * 2 + 1
        canvas_col = cell_col * 2 + 1

        for direct in walls:
            if direct == "N":
                canvas[canvas_row - 1][canvas_col] = Chars.WALL.value
            if direct == "S":
                canvas[canvas_row + 1][canvas_col] = Chars.WALL.value
            if direct == "E":
                canvas[canvas_row][canvas_col + 1] = Chars.WALL.value
            if direct == "W":
                canvas[canvas_row][canvas_col - 1] = Chars.WALL.value

    ft = color[1][theme]      # 42 pattern
    pc = color[2][theme]      # path
    points = color[3][theme]  # entry/exit
    cells = color[4][theme]   # cells
    bg = color[5][theme]

    # Always box every cell with the normal cell color first, so a hidden
    # path looks identical to the rest of the maze instead of leaving
    # unboxed/uncolored gaps where the solution cells are.
    canvas = colored_cell(canvas, maze, bg, bg)
    if value:
        canvas = colored_path(canvas, path, pc, bg)

    canvas = coloring_entry_exit(canvas, maze, points, bg)
    canvas = coloring_42(canvas, maze, ft, bg)
    return canvas
