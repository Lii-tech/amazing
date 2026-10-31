# this is only for testing
import sys
from typing import Any


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
        n = tuple(map(int, s))
    except ValueError:
        raise ValueError("Must contain only 2 integers!")

    for i in n:
        if i < 0:
            raise ValueError("Values must be non-negative!")
    # must parse the case when both are zeros and parse the seed!!!!!
    return n


def parsing(file_path: str) -> dict[str, Any]:
    """Reads, parses, and validates the maze configuration file."""
    config: dict[str, Any] = {}

    if len(sys.argv) != 2:
        raise ValueError("Expected exactly one config file!")

    req = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
           "OUTPUT_FILE", "PERFECT", "SEED"]
    sed = None
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

            if key not in req:
                raise ValueError(f"Unknown key: {key}")
            if sed == "SEED":
                if val.lower() in ("None", ""):
                    config[sed] = None
                else:
                    seed = int(val)
                    config[sed] = seed

                if seed < 0:
                    print(
                        "Warning! Negative and positive seed number "
                        "behavior is identical"
                    )

            config[key] = val

        # Check for missing keys
        for word in req:
            if word not in config:
                raise ValueError("Missing mandatory"
                                 f"configuration key: {word}")

        # Parse WIDTH and HEIGHT
        try:
            config["WIDTH"] = int(config["WIDTH"])
            config["HEIGHT"] = int(config["HEIGHT"])
        except ValueError:
            raise ValueError("WIDTH and HEIGHT must be integers!")

        if config["WIDTH"] <= 0 or config["HEIGHT"] <= 0:
            raise ValueError("WIDTH and HEIGHT must be positive!")

        width = config["WIDTH"]
        height = config["HEIGHT"]

        # Parse PERFECT
        config["PERFECT"] = perfect_parser(config["PERFECT"])

        # Check OUTPUT_FILE
        if not config["OUTPUT_FILE"]:
            raise ValueError("OUTPUT_FILE cannot be empty!")

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
