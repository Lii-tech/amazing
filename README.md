*This activity has been created as part of the 42 curriculum by <leobeida>, <aalorsan>.*

<div align="center">

# A-Maze-ing

### A Configurable Maze Generator in Python

A maze-generation project developed as part of the 42 curriculum.

Generate mazes, explore their paths, visualize their structure, and customize their appearance directly in the terminal.

<br>

[Description](#description) · [Instructions](#instructions) · [Configuration](#configuration) · [Algorithm](#maze-generation-algorithm) · [Project Management](#team-and-project-management)

</div>

---

## Table of Contents

* [Description](#description)
* [Features](#features)
* [Instructions](#instructions)
* [Configuration](#configuration)
* [Maze Generation Algorithm](#maze-generation-algorithm)
* [Shortest-Path Calculation](#shortest-path-calculation)
* [Project Structure](#project-structure)
* [Reusable Code](#reusable-code)
* [Advanced Features](#advanced-features)
* [Team and Project Management](#team-and-project-management)
* [Resources](#resources)
* [License](#license)

---

## Description

**A-Maze-ing** is a Python application that generates mazes according to user-defined configuration parameters. It creates a grid, generates passages between cells, calculates a path between the entry and exit, and exports the resulting maze to a text file.

The application also provides a terminal-based visualization with customizable color themes and interactive options.

The project combines graph traversal, grid-based data structures, configuration parsing, file handling, and terminal rendering in a modular implementation.

### Objectives

The main objectives are to:

* Generate mazes using a graph-traversal algorithm.
* Represent maze cells and their walls using a grid-based data structure.
* Allow users to configure the dimensions, entry, exit, and generation settings.
* Support perfect and imperfect maze generation.
* Calculate the shortest path between the entry and exit.
* Export the maze representation to a file.
* Display the maze in the terminal using colors.
* Provide interactive options for changing the visualization.
* Organize the implementation into reusable modules.

### How It Works

The application follows these stages:

1. Read and validate the configuration file.
2. Initialize the maze grid.
3. Generate passages between cells.
4. Calculate the shortest path between the entry and exit.
5. Export the maze representation.
6. Convert the maze data into a terminal visualization.
7. Allow the user to interact with the displayed maze.

---

## Features

| Feature                   | Description                                                                              |
| ------------------------- | ---------------------------------------------------------------------------------------- |
| Configurable dimensions   | Set the maze width and height.                                                           |
| Custom entry and exit     | Define the starting and ending coordinates.                                              |
| Perfect mazes             | Generate mazes without loops when the generation algorithm and configuration support it. |
| Imperfect mazes           | Introduce additional passages to create loops.                                           |
| Random seed               | Configure the seed used for reproducible maze generation.                                |
| Shortest-path calculation | Calculate a route from the entry to the exit.                                            |
| File export               | Save the generated maze in a textual representation.                                     |
| Terminal rendering        | Display the maze using terminal characters and ANSI colors.                              |
| Color themes              | Choose between available visual themes.                                                  |
| Interactive menu          | Regenerate the maze, toggle the shortest-path display, change the theme, or exit.        |
| 42 pattern                | Incorporate the required 42 pattern into the maze representation.                        |

---

## Instructions

### Requirements

* Python 3.12 or a compatible Python version.
* A Linux environment or WSL terminal is recommended.
* A terminal that supports ANSI color escape sequences.
* `make`, if you want to use the provided Makefile.

The application primarily uses Python's standard library.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

Replace the placeholders with your actual repository URL and directory name.

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Configure the Application

Create or edit `config.txt` in the project root. Follow the format described in the [Configuration](#configuration) section.

### 4. Run the Application

Execute the program with the configuration-file path as its argument:

```bash
python3 a_maze_ing.py config.txt
```

### 5. Interact with the Maze

Once the maze is displayed, use the interactive menu to access the available options:

* Regenerate the maze.
* Show or hide the shortest path.
* Change the color theme.
* Exit the application.

The available options depend on the implementation in the current version.

### 6. Output

The application generates a textual maze representation and displays a visual version in the terminal.

The current main program writes to `output_maze.txt`. If the `OUTPUT_FILE` configuration parameter is intended to control the destination, ensure the main program passes its configured value to the output function.

---

## Configuration

The application uses a configuration file to determine how the maze is generated.

Each parameter follows this format:

```text
KEY=VALUE
```

### Complete Configuration Example

```text
WIDTH=15
HEIGHT=10
ENTRY=0,0
EXIT=14,9
OUTPUT_FILE=output_maze.txt
PERFECT=True
SEED=42
```

### Configuration Parameters

| Parameter     | Type              | Description                                                   | Example           |
| ------------- | ----------------- | ------------------------------------------------------------- | ----------------- |
| `WIDTH`       | Positive integer  | Number of columns in the maze.                                | `15`              |
| `HEIGHT`      | Positive integer  | Number of rows in the maze.                                   | `10`              |
| `ENTRY`       | Two integers      | Coordinates of the entry, written as `x,y`.                   | `0,0`             |
| `EXIT`        | Two integers      | Coordinates of the exit, written as `x,y`.                    | `14,9`            |
| `OUTPUT_FILE` | File path         | Intended destination for the generated maze.                  | `output_maze.txt` |
| `PERFECT`     | Boolean           | Determines whether the maze should be perfect or allow loops. | `True`            |
| `SEED`        | Integer or `None` | Random seed used for maze generation.                         | `42`              |

### Parameter Details

**`WIDTH` and `HEIGHT`**

These parameters determine the dimensions of the maze. Both must be positive integers.

**`ENTRY` and `EXIT`**

These parameters specify the maze's entry and exit positions.

Coordinates are written as `x,y`. Because grid implementations often use `(row, column)` indexing, the coordinates must be converted consistently when initializing the maze.

Both positions must be within the maze boundaries and must be different.

**`OUTPUT_FILE`**

This parameter specifies the intended name or path of the output file. The main program should use the configured value when calling the output function.

**`PERFECT`**

This parameter determines whether the generated maze should be perfect or permit additional loops.

Accepted values depend on the parser; the current Boolean parser supports `true` and `false`, as well as `1` and `0`, without case sensitivity.

**`SEED`**

A numerical seed allows pseudorandom generation to be reproduced when the algorithm uses the same random-number generator and the same generation procedure.

The value `None` allows generation without a fixed seed.

### Validation

The configuration parser is responsible for checking the supplied values before the maze is generated.

Validation should ensure that:

* All required parameters are present.
* The dimensions are positive integers.
* The entry and exit contain valid coordinate pairs.
* The entry and exit are within the maze boundaries.
* The entry and exit are different.
* The Boolean parameter contains an accepted value.
* The seed is either a valid integer or `None`.

Invalid configuration values should produce a clear error instead of allowing the application to fail later during generation.

---

## Maze Generation Algorithm

### Depth-First Search

The maze generator uses **Depth-First Search (DFS)** to explore the grid and create passages between cells.

DFS is a graph-traversal algorithm that explores one branch as far as possible before backtracking to explore another branch.

For maze generation, cells are treated as vertices in a graph, and possible movements between adjacent cells are treated as edges.

### How It Works

The generation process follows these steps:

1. Select a starting cell.
2. Mark the current cell as visited.
3. Identify eligible neighboring cells that have not yet been visited.
4. Select an eligible neighbor.
5. Remove the wall separating the current cell from the selected neighbor.
6. Continue the search from the selected neighbor.
7. If no unvisited eligible neighbors remain, backtrack to an earlier cell.
8. Repeat until all eligible cells have been processed.

A stack or recursion can be used to implement the backtracking process.

### Why DFS?

DFS was chosen because it is well suited to grid-based maze generation and provides a straightforward way to construct passages while tracking visited cells.

Its main advantages are:

* **Simplicity:** The algorithm is relatively easy to implement and understand.
* **Efficiency:** A standard implementation can visit every cell in linear time relative to the number of cells and grid connections.
* **Backtracking:** The algorithm naturally explores different branches until no eligible neighbors remain.
* **Perfect-maze generation:** When every cell is visited and exactly one connection is added for each newly visited cell, the resulting connected maze is a spanning tree. This produces a perfect maze with a unique path between any two cells.
* **Extensibility:** Additional passages can be introduced after generation to create an imperfect maze with loops.

DFS also integrates naturally with the project's grid and cell data structures.

### Perfect and Imperfect Mazes

A perfect maze has no loops and exactly one possible path between any two reachable cells.

An imperfect maze contains additional passages that create cycles, allowing multiple possible routes between some cells.

The project separates loop-related functionality into its own module, allowing maze generation and the introduction of additional passages to be handled as distinct responsibilities.

---

## Shortest-Path Calculation

After the maze is generated, the application calculates a path between the entry and exit.

The maze can be represented as a graph:

* Each traversable cell represents a vertex.
* Each open passage between neighboring cells represents an edge.
* Walls prevent movement between cells.

The shortest-path module determines a route through the available passages.

For an unweighted maze, **Breadth-First Search (BFS)** is a suitable approach because it explores vertices in increasing order of distance from the starting vertex. The first time it reaches the destination, the resulting route is a shortest path.

The exact algorithm used should match the implementation in `shortest_path.py`.

The calculated path can also be displayed in the terminal, allowing the user to visualize a route through the generated maze.

---

## Project Structure

The project separates configuration parsing, grid management, maze generation, pathfinding, file output, and rendering into individual modules.

```text
A-Maze-ing/
│
├── a_maze_ing.py
├── config.txt
├── parser.py
├── renderer.py
├── Makefile
│
└── mazegen/
    ├── __init__.py
    ├── cell.py
    ├── dfs.py
    ├── grid.py
    ├── imperfect.py
    ├── maze_generator.py
    ├── output_file.py
    ├── pattern.py
    └── shortest_path.py
```

### Module Responsibilities

| Module            | Responsibility                                                                                     |
| ----------------- |----------------------------------------------------------------------------------------------------|
| `a_maze_ing.py`     | Main entry point that coordinates configuration, generation, pathfinding, output, and interaction. |
| `parser.py`         | Reads and validates configuration parameters.                                                      |
| `renderer.py`       | Provides terminal-rendering operations and prepares the maze representation for display.           |
| `cell.py`           | Represents an individual cell and its walls.                                                       |
| `grid.py`           | Creates the grid and manages neighboring cells and boundaries.                                     |
| `dfs.py`            | Implements depth-first search for maze generation.                                                 |
| `imperfect.py`      | Handles functionality associated with imperfect mazes and loops.                                   |
| `maze_generator.py` | Coordinates maze initialization and generation.                                                    |
| `shortest_path.py`  | Calculates a path between the entry and exit.                                                      |
| `output_file.py`    | Exports the maze and associated information to a text file.                                        |
| `pattern.py`        | Contains functionality related to the 42 pattern.                                                  |
| `config.txt`        | Stores the maze configuration.                                                                     |
| `output_maze.txt`   | Stores the generated maze representation.                                                          |
| `Makefile`          | Defines available build or execution commands.                                                     |
---

## Reusable Code

One of the project's main design principles is separating functionality into modules so that individual components can be reused without rewriting the entire application.

### 1. Grid and Cell Modules

The grid and cell modules define the maze's underlying representation.

The cell module stores wall information, while the grid module manages cell positions, boundaries, and neighboring cells.

These modules can be reused by other grid-based applications, including different maze-generation algorithms or pathfinding implementations.

### 2. Maze Generator

The maze generator coordinates the generation process using the grid representation.

It can be extended to support additional algorithms while keeping the cell and grid structures unchanged, provided the new algorithms use compatible interfaces.

### 3. Configuration Parser

The parser separates configuration handling from maze generation.

This makes it possible to reuse the parsing and validation logic in other command-line applications that accept structured configuration files.

### 4. Shortest-Path Module

Keeping pathfinding separate from maze generation allows the pathfinding logic to operate on different maze instances.

It can also be adapted for other graph-based applications, provided their graph representation is compatible.

### 5. Output Module

The output module separates maze serialization from the main application.

It can be reused to export maze data without requiring the terminal renderer to run.

### 6. Rendering Components

Separating rendering from generation allows the same maze data to be displayed using different terminal themes or alternative visualization methods.

A new rendering style can be implemented without changing the core generation algorithm, provided the renderer receives the required maze representation.

---

## Advanced Features

The project includes additional functionality beyond basic maze generation.

### Imperfect Maze Generation

The project supports imperfect mazes by introducing additional passages. These passages create loops and provide alternative routes through the maze.

### Multiple Color Themes

The renderer provides several color themes:

* **Sea-peache**
* **Christmas**
* **Summer**

The interactive menu allows the user to switch between the available themes.

### Shortest-Path Display

The application can show or hide the calculated shortest path without requiring the maze-generation algorithm to be rewritten.

### Interactive Regeneration

The user can regenerate the maze through the menu instead of restarting the application manually.

### 42 Pattern

The project includes functionality associated with the required 42 pattern.

The precise effect of the pattern on traversability and maze generation depends on how `pattern.py` and the generator integrate it.

---

## Team and Project Management

### Team Roles

Replace the placeholders below with the actual team members and their responsibilities.

| Team Member | Responsibilities                                                                     |
| ----------- | ------------------------------------------------------------------------------------ |
| `<login1>`  | `<Describe the modules implemented, tests performed, and responsibilities handled.>` |
| `<login2>`  | `<Describe the modules implemented, tests performed, and responsibilities handled.>` |
| `<login3>`  | `<Describe the modules implemented, tests performed, and responsibilities handled.>` |

If there are fewer or more team members, adjust the table accordingly.

### Anticipated Planning

The initial plan was organized around the main development stages.

| Stage             | Planned Activities                                                                           |
| ----------------- | -------------------------------------------------------------------------------------------- |
| 1. Analysis       | Understand the requirements and identify the configuration parameters and expected output.   |
| 2. Design         | Define the cell and grid representations and establish module interfaces.                    |
| 3. Implementation | Develop the maze-generation algorithm, configuration parser, and pathfinding logic.          |
| 4. Integration    | Connect the modules and implement output generation and terminal rendering.                  |
| 5. Testing        | Verify configuration validation, maze connectivity, pathfinding, and output correctness.     |
| 6. Finalization   | Review the implementation, improve documentation, and prepare the repository for submission. |

### How the Plan Evolved

Describe how the actual development process differed from the original plan.

For example, document whether integration took longer than expected, whether rendering required additional work, or whether the team changed its approach after testing.

This section should reflect the team's actual experience rather than presenting the anticipated schedule as a completed historical record.

### What Worked Well

Potential strengths to discuss, if they reflect your experience, include:

* Dividing the application into independent modules.
* Sharing a common grid and cell representation between components.
* Separating generation, pathfinding, output, and rendering.
* Using configuration files to test different maze dimensions and settings.
* Using version control to track changes and collaborate.

### What Could Be Improved

Potential improvements include:

* Agreeing on module interfaces before implementation begins.
* Integrating components earlier to identify incompatibilities.
* Adding automated tests for configuration errors and maze boundaries.
* Testing perfect and imperfect mazes systematically.
* Verifying that the shortest path is valid and minimal.
* Keeping documentation synchronized with implementation changes.
* Improving error messages and handling invalid input consistently.

Replace or adapt these points to reflect what your team actually experienced.

### Tools Used

Document the tools that were genuinely used during development.

| Tool               | Purpose                                                       |
| ------------------ | ------------------------------------------------------------- |
| Python             | Implementing the maze generator and its supporting modules.   |
| Git                | Tracking changes and managing versions of the code.           |
| GitHub             | Hosting the repository and supporting collaboration, if used. |
| Linux / WSL        | Providing the development and execution environment, if used. |
| Make               | Running project commands defined in the Makefile, if used.    |
| Text editor or IDE | Writing, reviewing, and debugging the implementation.         |

---

## Resources

### Technical Documentation

The following references provide background on the concepts and tools used in the project.

1. **Python Documentation**
   https://docs.python.org/3/
   Reference for Python syntax, built-in data structures, file handling, exceptions, and standard-library modules.

2. **Python `random` Module**
   https://docs.python.org/3/library/random.html
   Documentation for pseudorandom number generation and seeded random sequences.

3. **Depth-First Search**
   https://en.wikipedia.org/wiki/Depth-first_search
   Overview of depth-first traversal and its use in graph exploration.

4. **Breadth-First Search**
   https://en.wikipedia.org/wiki/Breadth-first_search
   Explanation of breadth-first traversal and shortest-path calculations in unweighted graphs.

5. **Graph Theory**
   https://en.wikipedia.org/wiki/Graph_theory
   Background on vertices, edges, connected graphs, cycles, and spanning trees.

6. **Git Documentation**
   https://git-scm.com/doc
   Reference for version control, commits, branches, and collaboration.

### AI Usage

AI tools were used as development assistance where applicable.

The README should accurately describe the actual use of AI in this project. Relevant categories to document include:

* **Algorithm understanding:** Explaining DFS, graph traversal, maze connectivity, and shortest-path concepts.
* **Debugging:** Investigating error messages and identifying possible causes of implementation problems.
* **Code review:** Examining module responsibilities and suggesting improvements to code structure.
* **Documentation:** Organizing the README and explaining configuration parameters and module responsibilities.
* **Testing support:** Suggesting test cases for invalid configurations, maze boundaries, and pathfinding.

For transparency, specify which AI tools were used, the tasks for which they were used, and which parts of the project were affected. Distinguish between suggestions that were incorporated and those that were not.

AI-generated code or explanations should be reviewed and tested by the team. Each member should understand the functionality they submit.

---

## License

This project is part of the 42 curriculum.

If the repository includes a `LICENSE` file, consult that file for the applicable licensing terms.

