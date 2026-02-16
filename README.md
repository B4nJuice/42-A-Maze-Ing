https://harm-smits.github.io/42docs/


# TODO
- [x] Thickness = 50 000 => division by 0
- [x] Negative numbers in WIDTH and HEIGHT
- [x] Problem if exit next to entry
- [x] Strip keys and values in the config parsing
- [ ] Change theme when animated (stash frame anc display until this frame)
- [ ] Fix README.md
- [ ] Fix get_cell -> None | Cell
- [ ] self.custom_player()

*This project has been created as part of the 42 curriculum by lgirard, flauweri.*

# A-Maze-Ing

## Description
A-Maze-Ing is an interactive project for generating, displaying, and solving mazes. 
The goal is to allow users to visualize a randomly generated maze, move a player inside it, 
display the shortest path, and experiment with various display and interaction options.

## Instructions

### Installation
1. Clone the repository:
   ```sh
   git clone <repo_url>
   cd 42-A-Maze-Ing
   ```
2. Install dependencies and create the virtual environment:
   ```sh
   make install
   ```

### Execution
To run the main program:
```sh
make run
```
To launch the debugger:
```sh
make debug
```
To check code quality:
```sh
make lint
```

## Resources
- [Python Documentation](https://docs.python.org/3/)
- [MiniLibX Python (mlx)](https://github.com/42Paris/minilibx-linux)
- [Maze generation algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [pdb module tutorial](https://docs.python.org/3/library/pdb.html)
- [GeeksforGeeks](https://www.geeksforgeeks.org/)
- [W3Schools](https://www.w3schools.com/)
- [Stack Overflow](https://stackoverflow.com/)


**How AI was used:**  
GitHub Copilot was used for:
- Docstring
- Suggesting interactive feature ideas
- Drafting and structuring this README.md

## Config File Structure

The configuration file (`default_config.config`) uses a key-value format, with comments starting with `#`. Here are the main sections and options:

### Maze Parameters
- `WIDTH` and `HEIGHT`: Maze dimensions in cells (e.g., `WIDTH=20`)
- `ENTRY` and `EXIT`: Entry and exit coordinates (e.g., `ENTRY=0,0`)
- `OUTPUT_FILE`: Output file for the generated maze
- `PERFECT`: Whether to generate a perfect maze (no loops)
- `SEED`: Random seed for reproducible generation
- `WALL_THICKNESS`: Wall thickness as a percentage of a cell (e.g., `25`)
- `MAZE_SIZE`: Screen/maze image size in pixels (e.g., `MAZE_SIZE=900,900`)

### Display & Path
- `ICON_FILE`: Path to the icon file for display
- `TOGGLE_PATH`: Show/hide the shortest path (`True` or `False`)

### Colors
- `CUSTOM_COLORS`: Enable custom colors (`True` or `False`)
- `PATH_COLOR`: Color for the shortest path (e.g., `200,200,200`)
- `ENTRY_COLOR`: Color for the entry cell
- `EXIT_COLOR`: Color for the exit cell
- (All colors are in `r,g,b` format, 0..255)

### Animation
- `ANIMATED`: Enable animation (`True` or `False`)
- `FPS`: Frames per second for animation

### Buttons & Player
- `SPACING`: Button spacing in pixels
- `CUSTOM_PLAYER_FILE`: Path to custom player icon
- `AUTO_ADJUST_PLAYER`: Auto-adjust player size (`True` or `False`)
- `CUSTOM_PLAYER_COLORS`: Custom player colors (e.g., `r:255,0,0 g:0,255,0 b:0,0,255 w:255,255,255`)

**Example :**
```
WIDTH=20
HEIGHT=20
ENTRY=0,0
EXIT=19,19
PERFECT=True
SEED=42
WALL_THICKNESS=25
MAZE_SIZE=900,900
TOGGLE_PATH=True
CUSTOM_COLORS=True
PATH_COLOR=200,200,200
ENTRY_COLOR=100,100,255
EXIT_COLOR=65,80,255
ANIMATED=True
FPS=60
```

## Maze Generation Algorithm
We chose the **Depth-First Search (DFS) with backtracking** algorithm to generate the maze.  
This algorithm is simple to implement, guarantees a unique path between any two cells, and is easy to animate.

**Why this algorithm?**
- Easy to animate and understand
- Generates perfect mazes (no loops)
- Easily extendable for other algorithms (bonus)

## Reusable Code
- The `maze_generation/maze.py` module is generic and can be reused for other maze projects.
- The `display/display.py` module can display any grid or maze compatible with its API.
- The config parser (`config_parser.py`) is adaptable for other projects needing simple config files.

## Team & Project Management

### Roles
- <login1>: Maze generation, solving logic, config parser
- <login2>: Graphical display, event handling, MiniLibX integration
- <login3>: Documentation, Makefile management, testing & QA

### Planning
- Week 1: Research, algorithm selection, project structure
- Week 2: Implementation of generation and display
- Week 3: Adding interactive features, testing, documentation

**Evolution:**  
The schedule was adjusted to add more display and customization options based on user feedback.

### What worked well & improvements
- **Strengths:** Good task distribution, modular code, clear user interface
- **To improve:** More automated tests, better exception handling, more advanced GUI

### Tools used
- Git & GitHub for version control
- VS Code and GitHub Copilot for editing and AI assistance
- MiniLibX Python for graphics
- Flake8 and mypy for code quality

## Advanced Features
- Buttons to change maze color and toggle shortest path display
- move_mode and capability to move in maze
- Possibility to add other generation algorithms
- Dynamic display options (size, colors, etc.)

---
