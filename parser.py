import shutil
import sys
from typing import Any
from pathlib import Path

def perfect_parser(char: str) -> bool:
    """Converts a string into a boolean value."""
    char = char.strip().lower()

    if char in ["true", "1"]:
        return True
    elif char in ["false", "0"]:
        return False
    else:
        raise ValueError("Only '[true/false]' values are allowed!")


def entry_exit(c: str) -> tuple[int, int]:
    """Parses and validates entry or exit coordinates."""

    s = c.split(",")

    if len(s) != 2:
        raise ValueError("Must contain only 2 integers!")

    try:
        x, y = tuple(map(int, s))
    except ValueError:
        raise ValueError("Must contain only 2 integers!")

    if x < 0 or y < 0:
        raise ValueError("Values must be non-negative!")
    # must parse the case when both are zeros and parse the seed!!!!!
    return x, y

def parsing(file_path: str) -> dict[str, Any]:
    """Reads, parses, and validates the maze configuration file."""
    config: dict[str, Any] = {}

    if len(sys.argv) != 2:
        raise ValueError("Expected exactly one config file!")

    req = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
           "OUTPUT_FILE", "PERFECT"]
    optional = ["SEED"]
    allowed = req + optional
    try:
        with open(file_path, "r") as file:
            lines = file.read().splitlines()

        # Read the configuration
        for line in lines:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError("Invalid config line!")

            key, val = line.split("=", 1)

            key = key.strip().upper()
            val = val.strip()

            if key not in allowed:
                raise ValueError(f"Unknown key: {key}")
            if key in req:
                if val.lower() in ("none", ""):
                    raise ValueError(f"KEY {key} IS NEEDED!")

            if key == "SEED":
                if val.lower() == "none":
                    config[key] = None
                else:
                    try:
                        seed = int(val)
                    except ValueError:
                        raise ValueError("SEED must be Valued!")
                    if seed < 0:
                        print(
                            "Warning! Negative and positive seed number "
                            "behavior is identical"
                        )

                    config[key] = seed
                continue
            config[key] = val

        # Check for missing keys
        for word in req:
            if word not in config:
                raise ValueError("Missing mandatory"
                                 f"configuration key: {word}")

        # SEED not provided -> no fixed seed
        config.setdefault("SEED", None)
        # Parse WIDTH and HEIGHT
        
        try:
            config["WIDTH"] = int(config["WIDTH"])
            config["HEIGHT"] = int(config["HEIGHT"])
        except ValueError:
            raise ValueError("WIDTH and HEIGHT must be integers!")
        if config["WIDTH"] <= 0 or config["HEIGHT"] <= 0:
            raise ValueError("WIDTH and HEIGHT must be positive!")
        if config["WIDTH"] < 3 or config["HEIGHT"] < 3:
            raise ValueError("MAZE cannot be smaller than 4*4 cells")
        
        required_width = config["WIDTH"] * 4 + 2
        required_height = config["HEIGHT"] * 2 + 1
        width = required_width
        height = required_height

        # Parse PERFECT
        config["PERFECT"] = perfect_parser(config["PERFECT"])

        # Check OUTPUT_FILE
        if not config["OUTPUT_FILE"]:
            raise ValueError("OUTPUT_FILE cannot be empty!")
        p = Path(config["OUTPUT_FILE"])
        if p.suffix.lower() != ".txt":
            raise ValueError(f"'{config["OUTPUT_FILE"]}' must have a .txt extension")

        # Parse ENTRY and EXIT
        config["ENTRY"] = entry_exit(config["ENTRY"])
        config["EXIT"] = entry_exit(config["EXIT"])

        entr = config["ENTRY"]
        ext = config["EXIT"]

        # checking the ENTRY and EXIT difference
        if ext == entr:
            raise ValueError("ENTRY and EXIT should never be the same!")

        # ENTRY must be inside the maze
        if not (0 <= entr[0] < width and 0 <= entr[1] < height):
            raise ValueError("ENTRY is outside the maze!")

        #  checkin the the border of the exit inside the maze
        if not (0 <= ext[0] < width and 0 <= ext[1] < height):
            raise ValueError("EXIT is outside the maze!")
        
        # to prevent the user from zooming in or out so much that
        # the terminal becomes unsuitable for displaying the maze.

        terminal_width, terminal_height = shutil.get_terminal_size()
        if (required_width > terminal_width 
                or required_height > terminal_height):
            raise RuntimeError("Terminal is too small to display the maze!")

    # checkin any error could occuar during the compilation
    except FileNotFoundError:
        print(f"Error: The configuration file '{file_path}' was not found!")
        sys.exit(1)

    except PermissionError:
        print(f"Error: Permission denied to read '{file_path}'!")
        sys.exit(1)

    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    return config
