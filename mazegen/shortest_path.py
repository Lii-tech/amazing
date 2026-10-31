from collections import deque
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .maze_generator import MazeGenerator


def shortest_path(maze: "MazeGenerator") -> list[tuple[int, int]]:
    """
    Find the shortest path between the maze start and end positions.
    This function uses Breadth-First Search (BFS) to explore the maze.
    BFS visits positions level by level, which guarantees
    that the first time the end position is reached,
    the discovered path contains the minimum number of moves.
    The function only moves through open walls and ignores positions
    that are outside the maze or have already been visited.
    Args: maze: The MazeGenerator containing
    the maze grid, start position, and end position.
    Returns: A list of ``(row, column)`` coordinates representing
    the shortest path from the start position to the end position.
    The start and end positions are included in the returned list.
    Raises: ValueError: If there is no path
    between the start and end positions.
    """

    queue = deque([maze.start])
    previous = {maze.start: None}

    directions = {
        "N": (-1, 0),
        "E": (0, 1),
        "S": (1, 0),
        "W": (0, -1),
    }
    while queue:
        current = queue.popleft()
        if current == maze.end:
            break

        current_row, current_colm = current
        current_cell = maze.grid.cells[current_row][current_colm]
        for direction, (row_change, colm_change) in directions.items():
            if current_cell.walls[direction]:
                continue

            next_position = (
                current_row + row_change,
                current_colm + colm_change,
            )
            if not (0 <= next_position[0] < maze.grid.row
                    and 0 <= next_position[1] < maze.grid.colm):
                continue
            if next_position in previous:
                continue
            previous[next_position] = current
            queue.append(next_position)
    if maze.end not in previous:
        raise ValueError(f"no path exist between the start:{maze.start}"
                         f"and the end:{maze.end}")
    path = []
    current = maze.end

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()
    return path
