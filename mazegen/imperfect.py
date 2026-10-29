import random
from typing import Tuple, List, TYPE_CHECKING
from .cell import Cell
from .grid import Grid
from .dfs import generate_perfect
from .pattern import check_42
if TYPE_CHECKING:
    from .maze_generator import MazeGenerator

OPPO = {"N": "S", "E": "W", "S": "N", "W": "E"}


def is_42(cell: Cell) -> bool:
    """
  Return True if the cell is part of the closed 42 pattern."""
    return all(cell.walls.values())


def open_count(cell: Cell) -> int:
    """
   Return the number of open walls in a cell
   """
    return sum(1 for w in cell.walls.values() if not w)


def window_open(grid: Grid, top: int, left: int) -> bool:
    """
    True if the 3x3 window starting at (top, left) has no inner walls."""
    for r in range(top, top + 3):
        for c in range(left, left + 3):
            cell = grid.cells[r][c]
            if c < left + 2 and cell.walls["E"]:
                return False
            if r < top + 2 and cell.walls["S"]:
                return False
    return True


def has_3x3_open(grid: Grid, r: int, c: int) -> bool:
    """Check every 3x3 window that contains cell (r, c)."""
    for top in range(r - 2, r + 1):
        for left in range(c - 2, c + 1):
            if top < 0 or left < 0:
                continue
            if top + 2 >= grid.row or left + 2 >= grid.colm:
                continue
            if window_open(grid, top, left):
                return True
    return False


def try_break(grid: Grid, cell: Cell, nb: Cell, direct: str) -> bool:
    """Remove the wall only if it is safe. Returns True on success."""
    if not cell.walls[direct] or is_42(nb) or is_42(cell):
        return False
    cell.walls[direct] = False
    nb.walls[OPPO[direct]] = False
    if has_3x3_open(grid, cell.row, cell.colm) or \
       has_3x3_open(grid, nb.row, nb.colm):
        cell.walls[direct] = True          # undo
        nb.walls[OPPO[direct]] = True
        return False
    return True


def count_loops(grid: Grid) -> int:
    """Counts maze loops, excluding cells belonging to the 42 pattern."""
    edges = 0
    free = 0
    for row in grid.cells:
        for cell in row:
            if is_42(cell):
                continue
            free += 1
            if not cell.walls["E"] and cell.colm + 1 < grid.colm:
                edges += 1
            if not cell.walls["S"] and cell.row + 1 < grid.row:
                edges += 1
    return edges - (free - 1)   # 0 = perfect maze


def generate_imperfect(maze: "MazeGenerator") -> None:
    """
   Generate an imperfect maze while preserving maze constraints."""
    check_42(maze)
    generate_perfect(maze)
    grid = maze.grid
    rng = maze.rng

    # 1) kill dead-ends
    for row in grid.cells:
        for cell in row:
            if is_42(cell) or open_count(cell) != 1:
                continue
            cands = []
            for r, c, d in grid.get_neighbors(cell):
                if cell.walls[d]:
                    cands.append((grid.cells[r][c], d))
            rng.shuffle(cands)
            # prefer neighbours that are dead-ends too (fixes two at once)
            cands.sort(key=lambda t: open_count(t[0]) != 1)
            for nb, d in cands:
                if try_break(grid, cell, nb, d):
                    break

    # 2) guarantee at least 2 independent loops
    attempts = 0
    while count_loops(grid) < 2 and attempts < 10000:
        attempts += 1
        cell = grid.cells[rng.randrange(grid.row)][rng.randrange(grid.colm)]
        nbs = grid.get_neighbors(cell)
        if not nbs:
            continue
        r, c, d = rng.choice(nbs)
        try_break(grid, cell, grid.cells[r][c], d)





