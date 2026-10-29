"""
Note for creating and using a MazeGenerator object:

    generator = MazeGenerator(
        height=20,
        width=20,
        perfect=True,
        start=(0, 0),
        end=(19, 19),
        seed=42
    )

    generator.generator()

Custom parameters can be passed when creating the generator,
such as the maze size, start and end positions, generation mode,
and random seed.

The generated maze structure can be accessed through:

    generator.grid
    generator.grid.cells

The solution can be accessed using:

    solution = shortest_path(generator)
"""
from typing import Optional
from .grid import Grid
import random
from .dfs import generate_perfect
from .imperfect import generate_imperfect


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


        if self.perfect:
            generate_perfect(self)
        else:
            generate_imperfect(self)





