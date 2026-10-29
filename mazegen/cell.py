""" Represent a single cell in the maze.
    A cell stores its position in the maze,
    whether it has been visited during maze generation,
    the state of its four walls,
    and the coordinates of its neighboring cells.

    Attributes : 
    1]row : The row index of the cell in the maze grid.
    2]colm : The column index of the cell in the maze grid.
    3]visited : Whether the cell has been visited during maze generation.
    4]walls : A dictionary containing the four walls of the cell.

    ``True`` means the wall is closed and ``False`` means the wall is open.
    neighbors : A dictionary mapping each direction to
    the coordinates of the neighboring cell.
    Directions : ``N``: North, one row above.
    ``E`` : East, one column to the right.
    ``S`` : South, one row below. 
    ``W`` : West, one column to the left.
"""


class Cell:
    def __init__(self, row: int, colm: int):
        self.row= row
        self.colm=colm
        self.visited= False
        self.walls={
        "N": True,
        "E": True,
        "S": True,
        "W": True
            }
        self.neighbors: dict[str, tuple[int, int]]= {
            "N": (self.row - 1, self.colm),
            "E": (self.row, self.colm + 1),
            "S": (self.row + 1, self.colm),
            "W": (self.row, self.colm - 1)
            }

