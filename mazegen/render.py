from typing import TYPE_CHECKING
from enum import Enum
from .output_file import output_file
from .pattern import pattern_cells

if TYPE_CHECKING:
    from .maze_generator import MazeGenerator


RESET = "\033[0m"
BOLD = "\033[1m"



#naming the unicode characters for the usability
class Chars(Enum):
    MD = "\u2533"   # ┳ middle, down
    MU = "\u253B"   # ┻ middle, up

    RRC = "\u250F"  # ┏ right upper corner
    LRC = "\u2513"  # ┓ left upper corner

    RDC = "\u2517"  # ┗ right lower corner
    LDC = "\u251B"  # ┛ left lower filecorner

    VL = "\u2503"   # ┃ vertical line
    HL = "\u2501"   # ━ horizontal line

    RHC = "\u2523"  # ┣ right half cross / vertical
    LHC = "\u252B"  # ┫ left half cross / vertical

    CC = "\u254B"   # ╋ cross

#to fix corners in the maze
JUNCTIONS = {
    "": " ",

    "N": Chars.VL.value,
    "S": Chars.VL.value,
    "E": Chars.HL.value,
    "W": Chars.HL.value,

    "NS": Chars.VL.value,
    "EW": Chars.HL.value,

    "NE": Chars.RDC.value,
    "NW": Chars.LDC.value,
    "SE": Chars.RRC.value,
    "SW": Chars.LRC.value,

    "NSE": "┣",
    "NSW": "┫",
    "NEW": "┻",
    "SEW": "┳",

    "NSEW": Chars.CC.value,
}

#taking the outfile output to decode it lol and use it to rendering the maze
def convert_to_binary(output_file: str):
    with open(output_file, "r") as file:
        binary = []
        for line in file:
            #print("READ:", repr(line))
            if line.startswith("("):
                break
            for digit in line.strip():
                #print("DIGIT:", repr(line))
                b = int(digit, 16)
                b = bin(b)[2:]
                binary.append(b.zfill(4))
    return binary


def print_canvas(canvas):
    for row in canvas:
        print("".join(cell * 2 for cell in row) + RESET)
    print(RESET, end="") 



#putting the walls in the border instead of building it then breaking it 
def put_the_walls(binary):
    walls = []
    i = 0
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


#fixing corners after rendering the border and tha walls 
def fix_junctions(canvas: list) -> list:
    rows = len(canvas)
    cols = len(canvas[0])

    for r in range(2, rows - 1, 2):
        for c in range(2, cols - 1, 2):

            directions = ""

            if canvas[r - 1][c] == Chars.VL.value:
                directions += "N"

            if canvas[r + 1][c] == Chars.VL.value:
                directions += "S"

            if canvas[r][c + 1] == Chars.HL.value:
                directions += "E"

            if canvas[r][c - 1] == Chars.HL.value:
                directions += "W"

            if directions in JUNCTIONS:
                canvas[r][c] = JUNCTIONS[directions]

    return canvas


def coloring_42(canvas: list[list[str]], maze: "MazeGenerator",color: str,
    MAZE_BG: str):
    pattern = set(pattern_cells(maze))
    for row, col in pattern_cells(maze):
        canvas_row = row * 2 + 1
        canvas_col = col * 2 + 1
        canvas[canvas_row][canvas_col] = f"{MAZE_BG}{color} {RESET}{MAZE_BG}"

        # Connect to the cell on the right, but never paint over a wall
        if (row, col + 1) in pattern and canvas[canvas_row][canvas_col + 1] != Chars.HL.value:
            canvas[canvas_row][canvas_col + 1] = f"{color} {RESET}{MAZE_BG}"

        # Connect to the cell below, but never paint over a wall
        if (row + 1, col) in pattern and canvas[canvas_row + 1][canvas_col] != Chars.VL.value:
            canvas[canvas_row + 1][canvas_col] = f"{color} {RESET}{MAZE_BG}"

    return canvas

def colored_path(
    canvas: list[list[str]],
    path: list[tuple[int, int]],
    color: str,
    MAZE_BG: str
) -> list[list[str]]:
    BLUE = "\033[48;2;175;215;255m"

    for i in range(len(path)):
        row, col = path[i]

        canvas_row = row * 2 + 1
        canvas_col = col * 2 + 1

        # Color the cell
        canvas[canvas_row][canvas_col] = f"{color} {MAZE_BG}"

        # Connect to the next cell
        if i + 1 < len(path):
            next_row, next_col = path[i + 1]

            # Moving right
            if next_col == col + 1:
                canvas[canvas_row][canvas_col + 1] = f"{color} {MAZE_BG}"

            # Moving left
            elif next_col == col - 1:
                canvas[canvas_row][canvas_col - 1] = f"{color} {MAZE_BG}"

            # Moving down
            elif next_row == row + 1:
                canvas[canvas_row + 1][canvas_col] = f"{color} {MAZE_BG}"

            # Moving up
            elif next_row == row - 1:
                canvas[canvas_row - 1][canvas_col] = f"{color} {MAZE_BG}"

    return canvas 

def color_walls(canvas: list[list[str]], color: list[list[str]], MAZE_BG: str) -> list[list[str]]:
    for r in range(len(canvas)):
        for c in range(len(canvas[r])):
            if canvas[r][c] != " ":
                canvas[r][c] = f"{color}{canvas[r][c]}{RESET}{MAZE_BG}"

    return canvas

def coloring_entry_exit(canvas: list[list[str]], maze: "MazeGenerator",color: str,
    MAZE_BG: str):
    entr_row = maze.start[0] * 2 + 1
    entr_col = maze.start[1] * 2 + 1

    exit_row = maze.end[0] * 2 + 1
    exit_col = maze.end[1] * 2 + 1

    canvas[entr_row][entr_col] = f"{color} {RESET}{MAZE_BG}"
    canvas[exit_row][exit_col] = f"{color} {RESET}{MAZE_BG}"

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
def colored_cells(
    canvas: list[list[str]],
    maze: "MazeGenerator",
    path: list[tuple[int, int]]
) -> list[list[str]]:

    protected = set(path)

    protected.add(maze.start)
    protected.add(maze.end)
    protected.update(pattern_cells(maze))

    for row in range(maze.grid.row):
        for col in range(maze.grid.colm):

            if (row, col) in protected:
                continue

            canvas_row = row * 2 + 1
            canvas_col = col * 2 + 1
            canvas[canvas_row][canvas_col] = (
                f"{color} {RESET}{MAZE_BG}"
            )

    return canvas

#rendering the border first
def border(maze: "MazeGenerator", path: list[tuple[int, int]],directions: list[list[str]], file: str, color: list[list[str]],
           theme: int, value: int) -> list:
    rows = maze.grid.row * 2 + 1 
    cols = maze.grid.colm * 2 + 1
    
    if cols % 2 == 0:
        cols = cols + 1
    
    canvas = [[" "] * cols for _ in range(rows)]
        # top
    
    canvas[0][0] = Chars.RRC.value
    for col in range(1, cols):
        canvas[0][col] = Chars.HL.value
    canvas[0][cols - 1] = Chars.LRC.value

    # bottom
    canvas[rows - 1][0] = Chars.RDC.value
    for col in range(1, cols - 1):
        canvas[rows - 1][col] = Chars.HL.value
    canvas[rows - 1][cols - 1] = Chars.LDC.value

    # left + right
    for row in range(1, rows - 1):
        canvas[row][0] = Chars.VL.value
        canvas[row][cols - 1] = Chars.VL.value
    
    wall = color[0][theme]  # wall
    bg = color[5][theme]
    binary = convert_to_binary(file)
    draw_wall = put_the_walls(binary)
    canvas = rendering(canvas, maze, path, draw_wall,
                        maze.grid.row, maze.grid.colm,
                        color, theme, value)
    canvas = fix_junctions(canvas)
    canvas = color_walls(canvas, wall, bg)

    '''
    binray = convert_to_binary(file)
    draw_wall = put_the_walls(binray)
    canvas = rendering(canvas, maze, path, draw_wall, maze.grid.row, maze.grid.colm)
    canvas = fix_junctions(canvas)
    canvas = color_walls(canvas)
'''
    return canvas

def rendering(canvas: list[list[str]], maze: "MazeGenerator", path: list[tuple[int, int]],draw_wall: list[list[str]],
              rows: int, cols: int, color: str, theme: int, value: int) -> list[list[str]]:
    #cell_number tells you WHICH cell
    #walls tells you WHICH directions
    maze_cols = cols
    for cell_number, walls in enumerate(draw_wall):
        cell_row = cell_number // maze_cols
        cell_col = cell_number % maze_cols
        canvas_row = cell_row * 2 + 1
        canvas_col = cell_col * 2 + 1

        for direct in walls:
            if direct == "N":
                canvas[canvas_row - 1][canvas_col] = Chars.HL.value
                #canvas[canvas_row - 1][canvas_col] = Chars.MU.value
            if direct == "S":
                canvas[canvas_row + 1][canvas_col] = Chars.HL.value
            if direct == "E":
                canvas[canvas_row][canvas_col + 1] = Chars.VL.value
            if direct == "W":
                canvas[canvas_row][canvas_col - 1] = Chars.VL.value

    
    ft = color[1][theme]      # 42 pattern
    pc = color[2][theme]      # path
    points = color[3][theme]  # entry/exit
    cells = color[4][theme]   # cells
    bg = color[5][theme]

    # Always box every cell with the normal cell color first, so a hidden
    # path looks identical to the rest of the maze instead of leaving
    # unboxed/uncolored gaps where the solution cells are.
    canvas = colored_cell(canvas, maze, cells, bg)
    if value:
        canvas = colored_path(canvas, path, pc, bg)

   
    canvas = coloring_42(canvas, maze, ft, bg)
    canvas = coloring_entry_exit(canvas, maze, points, bg)
    '''
#   canvas = colored_path(canvas, path)
    canvas = coloring_42(canvas, maze)
    canvas = coloring_entry_exit(canvas, maze)
    canvas = colored_cells(canvas, maze, path)
   '''
    return canvas



