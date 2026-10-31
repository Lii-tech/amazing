from .cell import Cell
from typing import TYPE_CHECKING
from .pattern import check_42


if TYPE_CHECKING:
    from .maze_generator import MazeGenerator


def breaker(cell: Cell, neighbor: Cell, direct: str) -> None:
    """Open the shared wall between two neighboring cells."""
    oppo = {
        "N": "S",
        "E": "W",
        "S": "N",
        "W": "E"
    }
    cell.walls[direct] = False
    neighbor.walls[oppo[direct]] = False

# MazeGenerator is only needed for type checking to avoid a circular import.


def generate_perfect(maze: "MazeGenerator") -> None:
    """
    Generate a perfect maze using depth-first search.
    The algorithm randomly selects unvisited neighboring cells,
    opens the shared wall, and backtracks when no unvisited neighbor remains.
    """
    check_42(maze)
    rng = maze.rng
    start_cell = maze.grid.cells[maze.start[0]][maze.start[1]]
    start_cell.visited = True

    stack: list[Cell] = [start_cell]

    while stack:
        current_cell = stack[-1]
        neighbors = maze.grid.get_neighbors(current_cell)
        unvisited: list[tuple[Cell, str]] = []

        for row, colm, direction in neighbors:
            neighbor = maze.grid.cells[row][colm]
            if not neighbor.visited:
                unvisited.append((neighbor, direction))
        if unvisited:
            neighbor, direction = rng.choice(unvisited)
            neighbor.visited = True
            breaker(current_cell, neighbor, direction)
            stack.append(neighbor)
        else:
            stack.pop()
