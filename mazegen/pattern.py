from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .maze_generator import MazeGenerator

PAT_H = 5
PAT_W = 7

closed_cells = [
    # 4
    (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 2), (4, 2),
    # 2
    (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (2, 5), (2, 4),
    (3, 4), (4, 4), (4, 5), (4, 6),
]


def pattern_origin(maze: "MazeGenerator") -> tuple[int, int]:
    """
    Calculate the top-left position of the 42 pattern.
    The pattern is positioned approximately in the center of the maze.
    Args: maze: The MazeGenerator containing the maze dimensions.
    Returns: A ``(row, column)`` tuple representing the top-left position of the 42 pattern.
"""
    col0 = round(maze.grid.row - PAT_W )// 2
    row0 = round(maze.grid.colm - PAT_H)// 2
    return row0, col0


def pattern_cells(maze: "MazeGenerator") -> set[tuple[int, int]]:
    """
    Return the maze coordinates occupied by the 42 pattern.
    The coordinates stored in ``closed_cells`` are relative to the pattern's origin.
    They are converted into actual maze coordinates using ``pattern_origin()``.
    Args: maze: The MazeGenerator containing the maze dimensions.
    Returns: A set of ``(row, column)`` coordinates belonging to the 42 pattern.
"""
    row0, col0 = pattern_origin(maze)
    return {(row0 + r, col0 + c) for r, c in closed_cells}


def in_42_pattern(maze: "MazeGenerator", point: tuple[int, int]) -> bool:
    """
    Check whether a coordinate belongs to the 42 pattern.
    Args: maze: The MazeGenerator containing the maze dimensions.
    point: The ``(row, column)`` coordinate to check.
    Returns: ``True`` if the coordinate belongs to the 42 pattern, otherwise ``False``.
"""
    return point in pattern_cells(maze)


def check_42(maze: "MazeGenerator") -> None:
    """
    Check the maze size and reserve the 42 pattern.

    Skips the pattern if the maze is too small and raises an error if
    the entry or exit is inside the pattern. Pattern cells are marked
    as visited so maze generation does not use them.
    """
    row0, col0 = pattern_origin(maze)

    too_small = (
        row0 < 1
        or col0 < 1
        or row0 + PAT_H > maze.grid.row - 1
        or col0 + PAT_W > maze.grid.colm - 1
    )
    if too_small:
        print("Error: maze too small for the 42 pattern, it will be omitted.")
        return

    cells = pattern_cells(maze)
    if maze.start in cells or maze.end in cells:
        raise ValueError(
            "ENTRY or EXIT is inside the 42 pattern, choose other coordinates."
        )

    for r, c in cells:
        maze.grid.cells[r][c].visited = True

