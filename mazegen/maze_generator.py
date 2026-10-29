
from typing import Optional
from .grid import Grid
import random
from .dfs import generate_perfect
from .imperfect import generate_imperfect

"""
    Initializes the maze grid, start and end positions,
    generation type,
    and random number generator.

    Args:
        height: Number of rows in the maze.
        width: Number of columns in the maze.
        perfect: Whether to generate a perfect maze.
        start: Starting cell coordinates.
        end: Ending cell coordinates.
        seed: Optional seed for reproducible random generation.
"""
class MazeGenerator:
    def __init__(
        self,
        height: int,
        width: int,
        perfect: bool,
        start:tuple[int, int],
        end: tuple[int, int],
        seed: int | None = None
    ) -> None:

        self.grid=Grid(height, width)
        self.start=start
        self.end=end
        self.perfect=perfect
        self.seed=seed
        self.rng = random.Random(seed)

    def generator(self) -> None:

        """
    The generation functions are imported inside the method
    to avoid circular imports between the maze generator and the generation modules.
    Generate the maze according to the selected generation mode.
    Uses the perfect maze generator when ``self.perfect`` is ``True``.
    Otherwise, uses the imperfect maze generator.
    The generated maze is stored in ``self.grid``.
    from .pattern import check_42
    from .dfs import generate_perfect
    from .imperfect import generate_imperfect
    """

        self.grid = Grid(self.grid.row, self.grid.colm)
        if self.perfect:
            generate_perfect(self)
        else:
            generate_imperfect(self)





