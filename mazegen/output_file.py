from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .maze_generator import MazeGenerator


def convert_path(path: list[tuple[int, int]]) -> str:

    """
    Convert a coordinate path into movement directions.
    The function compares each cell with the next cell in the path and determines
    whether the movement is North, South, East, or West.
    Args: path: A list of ``(row, column)`` coordinates representing
    the path through the maze. Returns: A string containing the movement directions
    using ``N``, ``S``, ``E``, and ``W``. Example: A path such as 
    ``[(0, 0), (0, 1), (1, 1)]`` returns ``"ES"``. 
"""

    direction: str = ""
    for coor in range(len(path) - 1):
        r1, c1 = path[coor]
        r2, c2 = path[coor + 1]
        if r2 == r1 - 1:
                direction += "N"
        if r2 == r1 + 1:
                direction += "S"
        if c2 == c1 - 1:
                direction += "W"
        if c2 == c1 + 1:
                direction += "E"
    return direction
            

def output_file(maze: "MazeGenerator", mazefile: str, path: list[tuple[int, int]]) -> None:

    """
Write the generated maze and its solution to a file.
The maze cells are encoded from their wall values into binary,
converted to a hexadecimal digit, and written row by row.
After the maze data, the function writes the entry coordinates,
exit coordinates, and the solution path as movement directions.
Args: maze: The MazeGenerator object containing the generated grid,
start position, and end position. mazefile: The path of the file where the maze will be written.
path: The shortest path represented as a list of ``(row, column)`` coordinates.
The MazeGenerator import is placed under ``TYPE_CHECKING``
so it is available to type checkers without importing it at runtime.
This helps avoid circular import problems between modules.
Raises: OSError: If the output file cannot be opened or written.
"""

    try:
        with open(mazefile, "w") as file:
            for row in maze.grid.cells:
                for cell in row:
                    cells = cell.walls                    
                    digit = []
                    for value in cells.values():
                        if value == False:
                            digit.append(0)
                        if value == True:
                            digit.append(1)
                    output = "".join(str(i) for i in digit)
                    number = int(output, 2)
                    dec = hex(number)[-1]
                    file.write(dec.upper())
                file.write("\n")
            shortest_path = convert_path(path)
            file.write("\n")
            file.write(f"({maze.start[0]}, {maze.start[1]})")
            file.write("\n")
            file.write(f"({maze.end[0]}, {maze.end[1]})")
            file.write("\n")
            file.write(shortest_path)
    except OSError as e:
        print(f"Error writing to file{mazefile}: {e}")

