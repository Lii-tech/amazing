"""
Represent the two-dimensional grid containing all maze cells.
The grid creates and stores a Cell object for every position in the maze.
It also provides methods for determining which directions are outside the grid
and for retrieving the valid neighboring cells.
Attributes: row: The height of the grid, measured in number of rows.
colm: The width of the grid, measured in number of columns.
cells: A two-dimensional list containing the Cell objects.
Each cell can be accessed using ``cells[row][colm]``.
"""

from .cell import Cell


class Grid:
    def __init__(self, height: int, width: int):
        self.row = height
        self.colm = width
        self.cells = []

        for r in range(height):
            curr_row = []

            for col in range(width):
                cell = Cell(r, col)
                curr_row.append(cell)

            self.cells.append(curr_row)

    def get_forbid(self, cell: Cell) -> list[str]:
        """Returns directions that lead outside the maze boundaries."""

        forbidden = []

        if cell.row == 0:
            forbidden.append("N")
        if cell.colm == 0:
            forbidden.append("W")
        if cell.row == self.row - 1:
            forbidden.append("S")
        if cell.colm == self.colm - 1:
            forbidden.append("E")

        return forbidden

    def get_neighbors(
        self, cell: Cell
    ) -> list[tuple[int, int, str]]:
        """Returns valid neighboring cell coordinates and their directions."""
        nb: list[tuple[int, int, str]] = []
        directions = cell.neighbors
        forbid = self.get_forbid(cell)

        for direct, (row, colm) in directions.items():
            if direct in forbid:
                continue
            nb.append((row, colm, direct))

        return nb
