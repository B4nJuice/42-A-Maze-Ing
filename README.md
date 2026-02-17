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

----
#### Config Types


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
- The config parser (`config/config.py`) is adaptable for other projects needing simple config files.

### Tools used
- Git & GitHub for version control
- VS Code and GitHub Copilot for editing and AI assistance
- MiniLibX Python for graphics
- Flake8 and mypy for code quality

## Advanced Features
- Buttons to change maze color and toggle shortest path display
- move_mode and capability to move in maze
- Dynamic display options (size, colors, etc.)

---
