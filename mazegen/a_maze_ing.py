import sys
from parser import parsing
from .maze_generator import MazeGenerator
from .shortest_path import shortest_path
from .output_file import output_file
from .render import convert_to_binary, put_the_walls, border
from .render import print_canvas

# CHRISMAS theme
WHITE = "\033[48;2;255;251;247m"
DARK_GREEN = "\033[48;2;50;78;38m"
BEIGE = "\033[48;2;189;161;134m"
DARK_RED = "\033[48;2;94;28;35m"
DUSTY_PINK = "\033[48;2;223;115;149m"
# SUMMER theme
VIOLET = "\033[48;2;113;25;113m"
ORANGE = "\033[48;2;255;165;0m"
GRASS = "\033[48;2;160;156;51m"
LAVENDER = "\033[48;2;180;167;214m"
GREEN = "\033[48;2;161;148;127m"
DARK_GREY = "\033[48;2;96;82;70m"
# SEA-PEACHE theme
BABY_BLUE = "\033[48;2;175;215;255m"
CREAM = "\033[48;2;255;242;204m"
BABY_PINK = "\033[48;2;223;115;149m"
LIGHT_GREEN = "\033[48;2;182;215;168m"
LIGHT_RED = "\033[38;2;255;215;215m"
DARK_BROWN = "\033[48;2;96;54;12m"
BABY_GRASS = "\033[48;2;219;243;195m"
# givin values
MAZE_BG = [CREAM, GREEN, GRASS]
WALL_COLORS = [CREAM, GREEN, GRASS]
FTCOLOR = [BABY_PINK, DARK_RED, VIOLET]
PATHCOLOR = [BABY_BLUE, DARK_GREEN, ORANGE]
POINTSCOLOR = [BABY_GRASS, DARK_BROWN, LAVENDER]
CELLSCOLOR = [CREAM, GREEN, GRASS]

color = [
    WALL_COLORS,
    FTCOLOR,
    PATHCOLOR,
    POINTSCOLOR,
    CELLSCOLOR,
    MAZE_BG
    ]


def main_maze() -> None:
    config_file = sys.argv[1]
    config = parsing(config_file)
    entry = (config["ENTRY"][1], config["ENTRY"][0])
    exit = (config["EXIT"][1], config["EXIT"][0])

    maze = MazeGenerator(
        config["HEIGHT"],
        config["WIDTH"],
        config["PERFECT"],
        entry,
        exit,
        config.get("SEED"),
        )
    show = False
    theme = 0
    value = 0
    try:
        maze.generator()

        path = shortest_path(maze)
        output_file(maze, "output_maze.txt", path)

        binary = convert_to_binary("output_maze.txt")
        draw_wall = put_the_walls(binary)

        borde = border(
            maze,
            path,
            draw_wall,
            "output_maze.txt",
            color,
            theme,
            value
        )
        print("\033[0m\033[H\033[2J", end="")
        print_canvas(borde)

        while True:
            user = input("1] press 1 to Re-generate a new maze\n"
                         "2] press 2 to show/Hide the shortest path\n"
                         "3] press 3 to change the maze colour\n"
                         "4] press 4 to exit\n")
            if user == "1":
                maze.generator()

                path = shortest_path(maze)
                output_file(maze, "output_maze.txt", path)

                binary = convert_to_binary("output_maze.txt")
                draw_wall = put_the_walls(binary)
                show = False
                value = 0

                borde = border(
                    maze,
                    path,
                    draw_wall,
                    "output_maze.txt",
                    color,
                    theme,
                    value
                )

                print("\033[0m\033[H\033[2J", end="")
                print_canvas(borde)

            elif user == "2":
                show = not show

                if show:
                    value = 1
                    print("VISIABLE!")

                else:
                    value = 0
                    print("HIDDEN!")
                borde = border(
                    maze,
                    path,
                    draw_wall,
                    "output_maze.txt",
                    color,
                    theme,
                    value
                )
                print("\033[0m\033[H\033[2J", end="")
                print_canvas(borde)

            elif user == "3":
                print("\nTHE AVAILABLE THEMES:")
                print("[1]. SEA-PEACHE")
                print("[2.  CHRISMAS")
                print("[3]. SUMMER")
                choice = input("\nCHOOSE ONE PLEASE: ")

                if choice == "1":
                    theme = 0
                elif choice == "2":
                    theme = 1
                elif choice == "3":
                    theme = 2
                else:
                    print("Wrong insertion.")
                    continue
                borde = border(
                    maze,
                    path,
                    draw_wall,
                    "output_maze.txt",
                    color,
                    theme,
                    value
                )

                print("\033[0m\033[H\033[2J", end="")
                print_canvas(borde)
            elif user == "4":
                print("you exit the program")
                sys.exit()

    except ValueError as e:
        print(e)

    except KeyboardInterrupt:
        print("you exit the program")
        sys.exit()


main_maze()
