*This project has been created as part of the 42 curriculum by lgirard, flauweri.*

# A-Maze-Ing

## Description
A-Maze-Ing is an interactive project for generating, displaying, and solving mazes. 
The goal is to allow users to visualize a randomly generated maze
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
- [MLX Docs](https://harm-smits.github.io/42docs/)



**How AI was used:**  
GitHub Copilot was used for:
- Docstring
- Suggesting interactive feature ideas
- Drafting and structuring this README.md

## Configuration
With the `Config` class (`src/config/config.py`) you register parameters (name, default and type-spec), optionally
override them from a file, and read typed values from your application. Below are the most-used helpers with a
prototype, a short description (based on the function docstrings), and concrete examples derived from
`a_maze_ing.py`.

### add_parameter

```python
def add_parameter(self, name: str, param: list[Any]) -> None
```

#### Brief
Register a configuration parameter in the internal registry. `param` is a list where:

#### Example (from `a_maze_ing.py`):

#### Typed parameter usage (detailed examples)

This project supports a compact type-spec syntax when registering parameters with `add_parameter`.
Below are concrete examples (taken from `a_maze_ing.py` and the `Config` docstrings) showing how to declare
and parse common types, nested tuples, and dict-like mappings.

- Simple integer / boolean / string

   Registration:

   ```py
   config.add_parameter("WIDTH", [20, [int]])
   config.add_parameter("PERFECT", [True, [bool]])
   config.add_parameter("OUTPUT_FILE", ["maze.txt", [str]])
   ```

   Result after parsing a config file (or using the defaults):
   - WIDTH -> int 20
   - PERFECT -> bool True
   - OUTPUT_FILE -> str "maze.txt"

- Fixed-size tuple (coordinates, colors)

   The tuple type spec has the form: `[tuple, n, [nested_types...], separator]`.

   Example: a 2-tuple of ints (coordinates):

   ```py
   config.add_parameter("ENTRY", [(0, 0), [tuple, 2, [[int], [int]], ","]])
   ```

   Example: an RGB color (3 ints):

   ```py
   config.add_parameter("PATH_COLOR", [(102,153,255), [tuple, 3, [[int],[int],[int]], ","]])
   ```

   When parsing `ENTRY=3,5` the parser returns the Python tuple `(3, 5)`.

- Nested tuples (example: `MAZE_SIZE`)

   You can nest tuples by using a tuple spec as a nested type. `a_maze_ing.py` registers `MAZE_SIZE` as a pair
   of 2-tuples (two coordinate pairs) separated by a space:

   ```py
   config.add_parameter("MAZE_SIZE", [((0,0),(0,0)), [
         tuple, 2, [
               [tuple, 2, [[int], [int]], ","],
               [tuple, 2, [[int], [int]], ","]
         ], " "
   ]])
   ```

   A config line like `MAZE_SIZE=1024,768 640,480` becomes
   `((1024, 768), (640, 480))`.

- Dict-like mappings (space-separated key:value entries)

   The parser models small mappings using a `dict` type built on top of tuple parsing. The typical pattern is:
   - top-level entries separated by a character (e.g. space),
   - each entry is a 2-tuple `key:value`, where `value` itself can be a tuple.

   Example used for `CUSTOM_PLAYER_COLORS` (from `a_maze_ing.py`):

   ```py
   # registration (default is a small example dict)
   config.add_parameter("CUSTOM_PLAYER_COLORS", [{"r": (255,0,0)}, [
         dict, [
               [tuple, 2, [[str], [tuple, 3, [[int],[int],[int]], ","]], ":"] ,
               [tuple, 2, [[str], [tuple, 3, [[int],[int],[int]], ","]], ":"] ,
               [tuple, 2, [[str], [tuple, 3, [[int],[int],[int]], ","]], ":"] ,
               [tuple, 2, [[str], [tuple, 3, [[int],[int],[int]], ","]], ":"] ,
         ], " "
   ]])
   ```

   Config line example:

   ```ini
   CUSTOM_PLAYER_COLORS=r:255,99,97 g:119,221,119 b:97,151,255 w:255,255,255
   ```

   Parsing result (approximate Python representation):

   ```py
   {
         'r': (255, 99, 97),
         'g': (119, 221, 119),
         'b': (97, 151, 255),
         'w': (255, 255, 255)
   }
   ```

   Notes: the `dict` spec is implemented by temporarily converting the requested type into a top-level
   `tuple` of N elements (where N is the number of top-level entries) and then converting the resulting
   iterable-of-pairs into a Python `dict`.


   ```python
   config.add_parameter("WIDTH", [20, [int]])
   config.add_parameter("ENTRY", [(0, 0), [tuple, 2, [[int], [int]], ","]])
   config.add_parameter("BACKGROUND_COLOR", [(255,255,255), [tuple, 3, [[int],[int],[int]], ","]])
  ```

#### Notes
You can also add all custom class/function callback that you want, the config will take it like a type and will do callback(parsed_value) and return the result. 

----
### set_commentary_str

```python
def set_commentary_str(self, commentary_str: str) -> None
```

#### Brief
Change the prefix used to recognize comment lines in config files. By default the parser treats lines starting
with `#` as comments; use this to change it (for example `"//"`).

#### Example
```python
config.set_commentary_str("#")   # default
config.set_commentary_str("//")   # if your config uses double slash for comments
```

----
### parse_file

```python
def parse_file(self, file: TextIO) -> None
```

#### Brief
Read and parse a configuration file (open file-like object). The parser expects lines of the form `KEY=VALUE`.
Known keys (registered via `add_parameter`) are validated and converted according to their type specification; unknown
keys raise `ConfigError`. After parsing the method also verifies that required parameters were provided.

#### Example (startup pattern in `a_maze_ing.py`):

```python
config = Config()
create_config(config)               # register all expected parameters and defaults
with open("src/default_config.config") as f:
    config.parse_file(f)            # override defaults from file
```

----
### get_value

```python
def get_value(self, parameter: str) -> Any
```

#### Brief
Return the current value for a registered parameter. If the parameter is not registered the function returns
`None`.

#### Example (usage in `a_maze_ing.py`):

```python
width = config.get_value("WIDTH")
height = config.get_value("HEIGHT")
entry = config.get_value("ENTRY")   # returns a tuple (x, y)
```

### Default config file format

```shell
# A-Maze-ing — Default configuration
# --------------------------------------------------
# Maze dimensions (in cells)
WIDTH=20
HEIGHT=20

# Entry and exit coordinates (format: x,y)
ENTRY=0,0
EXIT=19,19

# Output file for the generated maze
OUTPUT_FILE=maze.txt

# Generate a perfect maze
PERFECT=True

# Path to the icon file used in the display
ICON_FILE=src/default_icon.txt

# Random seed for reproducible generation (integer)
SEED=42

# Wall thickness expressed as a percentage
# Example: 5 means each wall occupy 5% of a cell
WALL_THICKNESS=5

# Screen / maze image size in pixels
# Format: width,height
MAZE_SIZE=900,900 0,900

# Toggle shortest path
TOGGLE_PATH=True

# --------------------------------------------------
# Color section (values in r,g,b format; 0..255)
# Set CUSTOM_COLORS to True to use the values below
CUSTOM_COLORS=True

# Color used to draw the shortest path
PATH_COLOR=200,200,200

# Color for the entry cell
ENTRY_COLOR=100,100,255

# Color for the exit cell
EXIT_COLOR=65,80,255

# --------------------------------------------------
# Animation parameters
ANIMATED=True
FPS=60

# Button parameter
SPACING=50

# --------------------------------------------------
# Custom player parameters
CUSTOM_PLAYER_FILE=src/default_player.txt
AUTO_ADJUST_PLAYER=True
CUSTOM_PLAYER_COLORS=r:255,0,0 g:0,255,0 b:0,0,255 w:255,255,255

```


## Maze Generation Algorithm
We chose the **Depth-First Search (DFS) with backtracking** algorithm to generate the maze.

### Why this algorithm ?
We chose DFS algorithm because it create more "natural" maze.

DFS:

![DFS](https://media.discordapp.net/attachments/1394986082721988680/1473608362133291028/image.png?ex=6996d43b&is=699582bb&hm=e6e8f68b6a0083616b3fd35c16f20c7813e12ba2c56388125f85ec2cfe68e233&=&format=webp&quality=lossless&width=641&height=641)

HPB:

![HPB](https://upload.wikimedia.org/wikipedia/commons/3/3f/Horizontally_Influenced_Depth-First_Search_Generated_Maze.png)

## Reusable Code
- The `maze_generation/maze.py` module is generic and can be reused for other maze projects.
- The `display/display.py` module can display any grid or maze compatible.
- The config parser (`config/config.py`) is adaptable for other projects needing simple config files.

## Team and project management

### Role of each member
#### flauweri
----
- Core Displayer
- Capability to move in maze
- Button creator
- Also participate in other shared tasks

#### lgirard
----
- Config parser
- Maze generation
- Maze animation
- Custom player
- Makefile
- Also participate in other shared tasks


### Planning
----
We started the project delayed, mid-January.

lgirard started with the config parser alone when flauweri were grinding python modules so he can be comfortable with python.

We did this project while doing python modules.

We finished the core part of A-Maze-Ing quickly, but we take our time to polish it and add various bonuses.

### What worked well and what could be improved ?

Teamwork went very well: our different skill levels were a real asset, and
everyone learned from each other. However, this same difference sometimes complicated the division of tasks—even though flauweri understood the principles of the maze generation algorithm,
it sometimes hindered the completion of certain parts related to the generation process.

### Tools used
- Git & GitHub for version control
- VS Code and GitHub Copilot for editing and AI assistance

## Bonuses
- Fully customizable config parser
- Maze animation
- Custom maze icon
- Capability to move in maze
- Custom player (which can adjust his size automatically)
- Button creator