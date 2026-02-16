import copy
from typing import TextIO
from src.maze_generation.cell import Cell
from src.maze_generation.seed import (create_seed, next_randint)


class MazeError(Exception):
    """
    Exception raised for general maze errors.

    Used as a base class for more specific maze-related exceptions.
    """
    def __init__(self, message: str = "undefined"):
        """
        Initialize the exception with a custom message.

        Parameters
        ----------
        message : str, optional
            Human-readable error message. Default is 'undefined'.
        """
        super().__init__(f"Maze error: {message}")


class IconError(MazeError):
    """
    Exception raised for errors related to the maze icon.
    """
    def __init__(self, message: str = "undefined"):
        """
        Initialize the exception with a custom message.

        Parameters
        ----------
        message : str, optional
            Human-readable error message. Default is 'undefined'.
        """
        super().__init__(f"Icon error: {message}")


class EntryExitError(MazeError):
    """
    Exception for invalid entry/exit positions or related errors.
    """
    def __init__(self, message: str = "undefined"):
        """
        Initialize the exception with a custom message.

        Parameters
        ----------
        message : str, optional
            Human-readable error message. Default is 'undefined'.
        """
        super().__init__(f"Entry Exit error: {message}")


class Maze():
    """
    Represent a maze grid and provide generation utilities.

    The Maze class stores Cell objects in a matrix and provides methods
    to generate, query and export the maze structure.
    """
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool, seed: int,
                 icon_file: TextIO) -> None:
        """
        Initialize a Maze instance.

        Parameters
        ----------
        width : int
            Maze width in cells.
        height : int
            Maze height in cells.
        entry : tuple[int, int]
            Entry coordinates as (x, y).
        exit : tuple[int, int]
            Exit coordinates as (x, y).
        perfect : bool
            If True, generate a perfect maze (single solution path).
        seed : int
            Seed value used by the RNG.
        icon_file : TextIO
            Text stream containing an ASCII icon to place at the maze center.

        Returns
        -------
        None
        """
        self.__matrix: list[list[Cell]] = []

        if (
            not isinstance(width, int) or not isinstance(height, int)
            or min(height, width) <= 0
                ):
            raise MazeError("width and height has to be positive integers.")

        self.__width: int = width
        self.__height: int = height
        self.__entry: tuple[int, int] = entry
        self.__exit: tuple[int, int] = exit
        self.__seed: int = create_seed(seed)
        self.__perfect: bool = perfect
        self.__after_exit = False
        self.__shortest_path = []
        self.__shortest_path_cells = []

        for coords in [entry, exit]:
            x, y = coords
            if x < 0 or y < 0 or x >= self.__width or y >= self.__height:
                raise EntryExitError("entry/exit cannot be outside the maze.")

        if entry == exit:
            raise EntryExitError("entry/exit cannot be the same cell.")

        for _ in range(height):
            row: list[int] = []
            for _ in range(width):
                cell: Cell = Cell()
                cell.set_wall("SOUTH", True)
                cell.set_wall("NORTH", True)
                cell.set_wall("EST", True)
                cell.set_wall("WEST", True)
                row.append(cell)
            self.__matrix.append(row)

        exit_cell: Cell = self.get_cell(exit)
        exit_cell.set_exit()

        icon_txt: str = icon_file.read(-1)
        icon_rows: list[str] = icon_txt.split("\n")

        for row in icon_rows:
            if row == "":
                icon_rows.remove(row)

        icon_height: int = len(icon_rows)
        icon_width: int = 0
        if icon_height > 0:
            icon_width = len(icon_rows[0])
            for row in icon_rows:
                if len(row) != icon_width:
                    icon_rows.clear()
                    raise IconError("icon line length has to stay the same.")

        if icon_height > height or icon_width > width:
            raise IconError("icon too big or maze too small.")

        start_x: int = round((width - icon_width) / 2)
        start_y: int = round((height - icon_height) / 2)

        icon_txt = icon_txt.replace("\n", "")

        for y in range(icon_height):
            for x in range(icon_width):
                if icon_txt[y * icon_width + x] not in ["0", " "]:
                    icon_cell_coords: tuple[int, int] = (x+start_x, y+start_y)
                    if entry == icon_cell_coords or exit == icon_cell_coords:
                        raise EntryExitError(
                            "entry/exit cannot be in the icon")
                    icon_cell: Cell = self.get_cell(icon_cell_coords)
                    icon_cell.set_icon()

    def get_matrix(self) -> list[list[Cell]]:
        """
        Return the internal matrix of Cells.

        Returns
        -------
        list[list[Cell]]
            2D list where each element is a :class:`Cell` instance.
        """
        return self.__matrix

    def get_cell(self, coords: tuple[int, int]) -> Cell:
        """
        Get the Cell at the specified coordinates.

        Parameters
        ----------
        coords : tuple[int, int]
            Coordinates as (x, y).

        Returns
        -------
        Cell | None
            The Cell instance at the coordinates, or None if out of bounds.
        """
        matrix = self.get_matrix()
        x, y = coords
        if x < 0 or y < 0 or x >= self.__width or y >= self.__height:
            raise ValueError
        cell = matrix[y][x]
        return cell

    def get_seed(self) -> int:
        """
        Return the RNG seed used for generation.

        Returns
        -------
        int
            Seed integer.
        """
        return self.__seed

    def get_entry(self) -> tuple[int, int]:
        """
        Return the entry coordinates.

        Returns
        -------
        tuple[int, int]
            Entry coordinates (x, y).
        """
        return self.__entry

    def get_exit(self) -> tuple[int, int]:
        """
        Return the exit coordinates.

        Returns
        -------
        tuple[int, int]
            Exit coordinates (x, y).
        """
        return self.__exit

    def get_width(self) -> int:
        """
        Return the maze width (number of columns).

        Returns
        -------
        int
            Maze width in cells.
        """
        return self.__width

    def get_height(self) -> int:
        """
        Return the maze height (number of rows).

        Returns
        -------
        int
            Maze height in cells.
        """
        return self.__height

    def get_shortest_path(self) -> list[str]:
        """
        Return the cached shortest path as a list of directions.

        Returns
        -------
        list[str]
            Sequence of directions (e.g. ["NORTH", "EST", ...]) from
            entry to exit.
        """
        return self.__shortest_path

    def is_perfect(self) -> bool:
        """
        Return True if the maze is perfect (contains a single path
        between any two cells).

        Returns
        -------
        bool
        """
        return self.__perfect

    def is_after_exit(self) -> bool:
        """
        Return whether generation has passed the exit cell.

        Returns
        -------
        bool
        """
        return self.__after_exit

    def invert_after_exit(self) -> None:
        """
        Toggle the 'after exit' generation flag.

        Returns
        -------
        None
        """
        self.__after_exit = True is not self.__after_exit

    def set_wall(self, coords: tuple[int, int], direction: str,
                 state: bool) -> None:
        """
        Place or remove a wall for the cell at ``coords`` and the
        neighboring cell in ``direction``.

        Parameters
        ----------
        coords : tuple[int, int]
            Coordinates of the cell to modify.
        direction : str
            One of "NORTH", "SOUTH", "EST", "WEST".
        state : bool
            True to close/place the wall, False to open/remove it.

        Returns
        -------
        None
        """
        cell: Cell = self.get_cell(coords)
        cell.set_wall(direction, state)

        x, y = coords
        next_dir: str = None
        next_coords: tuple[int, int] = None

        match direction:
            case "NORTH":
                if y - 1 >= 0:
                    next_coords = (x, y - 1)
                    next_dir = "SOUTH"
            case "WEST":
                if x - 1 >= 0:
                    next_coords = (x - 1, y)
                    next_dir = "EST"
            case "SOUTH":
                if y + 1 < self.__height:
                    next_coords = (x, y + 1)
                    next_dir = "NORTH"
            case "EST":
                if x + 1 < self.__width:
                    next_coords = (x + 1, y)
                    next_dir = "WEST"

        if next_dir is not None:
            next_cell: Cell = self.get_cell(next_coords)
            next_cell.set_wall(next_dir, state)

    def output_in_file(self, file: TextIO) -> None:
        """
        Write a textual representation of the maze to ``file``.

        The format is a grid of hexadecimal characters representing walls,
        followed by a blank line, then the entry and exit coordinates and
        the shortest path directions.

        Parameters
        ----------
        file : TextIO
            Open text file to write the maze representation to.

        Returns
        -------
        None
        """
        output: str = ""
        for y in range(self.__height):
            for x in range(self.__width):
                cell: Cell = self.get_cell((x, y))
                value: str = cell.get_hex_value()
                output += value
            output += "\n"

        output += "\n"

        for x, y in [self.get_entry(), self.get_exit()]:
            output += f"{x},{y}\n"

        for direction in self.get_shortest_path():
            output += direction[0]

        output += "\n"

        file.write(output)

    def create_path(self, coords: tuple[int, int],
                    last_coords: tuple[int, int] = None) -> tuple[int, int]:
        """
        Recursively carve a path from ``coords`` using randomized DFS.

        Parameters
        ----------
        coords : tuple[int, int]
            Starting coordinates for the path carving.
        last_coords : tuple[int, int], optional
            Coordinates of the previous cell used for backtracking.

        Returns
        -------
        tuple[int, int]
            Coordinates of the last cell reached by the recursion.
        """

        cell: Cell = self.get_cell(coords)
        cell.set_visited()

        if self.is_after_exit():
            cell.set_after_exit()

        valid_cells: list[tuple[int, int]] = self.check_surroundings(coords)
        n_valid_cells: int = len(valid_cells)

        if n_valid_cells == 0:
            return coords

        if cell.is_exit():
            self.invert_after_exit()
            if self.is_perfect():
                cell.set_dead()
                if last_coords is None:
                    return coords
                return last_coords

        next_coords: tuple[int, int] = valid_cells[
            next_randint(0, n_valid_cells)]

        next_direction = self.get_dir_by_coords(coords, next_coords)

        self.set_wall((coords), next_direction, False)
        return self.create_path(next_coords, coords)

    def find_next_cell(self, coords: tuple[int, int]) -> tuple[int, int]:
        """
        Determine the next cell to continue generation from.

        Parameters
        ----------
        coords : tuple[int, int]
            Current cell coordinates.

        Returns
        -------
        tuple[int, int] | None
            Next cell coordinates to process, or None if generation is
            complete from this branch.
        """
        cell: Cell = self.get_cell(coords)

        if cell.is_exit():
            self.invert_after_exit()

        open_walls = cell.get_state_walls(False)
        valid_cells: list[tuple[int, int]] = []
        visited_cells: list[tuple[int, int]] = []

        for direction in open_walls:
            check_coords: tuple[int, int] = self.get_coords_by_dir(coords,
                                                                   direction)
            check_cell: Cell = self.get_cell(check_coords)
            if check_cell is not None and not check_cell.is_dead():
                visited_cells.append(check_coords)

        valid_cells = self.check_surroundings(coords)
        n_valid_cells: int = len(valid_cells)

        if n_valid_cells == 0:
            cell.set_dead()
            n_visited_cells: int = len(visited_cells)
            if n_visited_cells == 0:
                return None
            next_cell: tuple[int, int] = visited_cells[
                next_randint(0, n_visited_cells)]
            return self.find_next_cell(next_cell)

        return coords

    def check_surroundings(self,
                           coords: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Return a list of unvisited neighboring cell coordinates.

        Parameters
        ----------
        coords : tuple[int, int]
            Coordinates of the reference cell.

        Returns
        -------
        list[tuple[int, int]]
            Valid neighboring coordinates that have not been visited.
        """
        x, y = coords
        valid_cells: list[str] = []

        cell: Cell = None
        cell_coords: tuple[int, int] = None

        if y + 1 < self.__height:
            cell_coords = (x, y + 1)
            cell = self.get_cell(cell_coords)
            if cell.is_visited() is False:
                valid_cells.append(cell_coords)
        if y - 1 >= 0:
            cell_coords = (x, y - 1)
            cell = self.get_cell(cell_coords)
            if cell.is_visited() is False:
                valid_cells.append(cell_coords)

        if x + 1 < self.__width:
            cell_coords = (x + 1, y)
            cell = self.get_cell(cell_coords)
            if cell.is_visited() is False:
                valid_cells.append(cell_coords)
        if x - 1 >= 0:
            cell_coords = (x - 1, y)
            cell = self.get_cell(cell_coords)
            if cell.is_visited() is False:
                valid_cells.append(cell_coords)
        return valid_cells

    def create_full_maze(self) -> None:
        """
        Generate the full maze starting from the entry cell.

        This builds a perfect maze first and optionally opens extra
        connections if the maze is not required to be perfect.

        Returns
        -------
        None
        """
        entry_coords: tuple[int, int] = self.get_entry()
        next_coords: tuple[int, int] = self.create_path(entry_coords)
        next_coords = self.find_next_cell(next_coords)

        while next_coords is not None:
            next_coords = self.create_path(next_coords)
            next_coords = self.find_next_cell(next_coords)

        if not self.is_perfect():
            possible_breach: list[tuple[str, tuple[int, int]]] = []

            for y in range(self.__height):
                for x in range(self.__width):
                    cell: Cell = self.get_cell((x, y))

                    if cell.is_exit():
                        continue

                    closed_walls = cell.get_state_walls(True)

                    next_cell: Cell = self.get_cell((x, y + 1))
                    if "SOUTH" in closed_walls and next_cell is not None:
                        if next_cell.is_exit():
                            continue
                        if next_cell.is_icon() or cell.is_icon():
                            continue
                        if next_cell.is_after_exit() != cell.is_after_exit():
                            possible_breach.append(tuple(("SOUTH", (x, y))))

                    next_cell: Cell = self.get_cell((x + 1, y))
                    if "EST" in closed_walls and next_cell is not None:
                        if next_cell.is_exit():
                            continue
                        if next_cell.is_icon() or cell.is_icon():
                            continue
                        if next_cell.is_after_exit() != cell.is_after_exit():
                            possible_breach.append(tuple(("EST", (x, y))))

            n_possible_breach: int = len(possible_breach)

            if n_possible_breach > 0:
                n_breach: int = next_randint(1, 3)
                for _ in range(n_breach):
                    direction, coords = possible_breach[
                        next_randint(0, n_possible_breach)]
                    self.set_wall(coords, direction, False)
        self.check_maze()
        self.__shortest_path = self.find_shortest_path()

        coords = self.get_entry()
        for char in self.get_shortest_path():
            coords = self.get_coords_by_dir(coords, char)
            self.__shortest_path_cells.append(self.get_cell(coords))

    @staticmethod
    def get_coords_by_dir(coords: tuple[int, int],
                          direction: str) -> tuple[int, int]:
        """
        Compute the coordinates of the neighbor in the given direction.

        Parameters
        ----------
        coords : tuple[int, int]
            Starting coordinates (x, y).
        direction : str
            Direction name: "NORTH", "SOUTH", "EST", or "WEST".

        Returns
        -------
        tuple[int, int]
            Neighboring coordinates (x, y).
        """
        x, y = coords
        directions: dict[str, tuple[int, int]] = {
            "EST": (x + 1, y),
            "WEST": (x - 1, y),
            "SOUTH": (x, y + 1),
            "NORTH": (x, y - 1),
        }
        direction = directions[direction]
        return direction

    @staticmethod
    def get_dir_by_coords(coords: tuple[int, int],
                          next_coords: tuple[int, int]) -> str:
        """
        Return the direction name to move from ``coords`` to
        ``next_coords``.

        Parameters
        ----------
        coords : tuple[int, int]
            Source coordinates.
        next_coords : tuple[int, int]
            Destination coordinates (must be adjacent).

        Returns
        -------
        str
            Direction string ("NORTH", "SOUTH", "EST", "WEST").
        """
        x, y = coords
        directions: dict[tuple[int, int], str] = {
            (x + 1, y): "EST",
            (x - 1, y): "WEST",
            (x, y + 1): "SOUTH",
            (x, y - 1): "NORTH",
        }
        direction = directions[next_coords]
        return direction

    @staticmethod
    def get_opposite_dir(direction: str) -> str | None:
        """
        Return the opposite direction for a cardinal direction.

        Parameters
        ----------
        direction : str
            One of "NORTH", "SOUTH", "EST", "WEST".

        Returns
        -------
        str | None
            Opposite direction string, or None if ``direction`` is None.
        """
        directions: dict[tuple[int, int], str] = {
            "WEST": "EST",
            "EST": "WEST",
            "NORTH": "SOUTH",
            "SOUTH": "NORTH",
        }

        if direction is None:
            return None

        return directions[direction]

    def is_isolate_cell(self, coords: tuple[int, int]) -> bool:
        """
        Determine whether the cell at ``coords`` is isolated (all walls
        closed).

        Parameters
        ----------
        coords : tuple[int, int]
            Cell coordinates.

        Returns
        -------
        bool
            True if the cell is isolated, False otherwise.
        """
        cell: Cell = self.get_cell(coords)
        if cell.is_dead():
            return False

        if len(cell.get_state_walls(True)) == 4:
            return True
        return False

    def is_in_shortest_path(self, cell: Cell) -> bool:
        return cell in self.__shortest_path_cells

    def check_maze(self) -> None:
        """
        Verify that the maze contains no isolated cells.

        Raises
        ------
        IconError
            If an isolated cell is detected.

        Returns
        -------
        None
        """
        for y in range(self.__height):
            for x in range(self.__width):
                coords: tuple[int, int] = (x, y)
                if self.is_isolate_cell(coords):
                    raise IconError(f"isolated cell : {coords}")

    def find_shortest_path(self) -> str:
        """
        Compute and return the shortest path from entry to exit.

        Returns
        -------
        list[str]
            Sequence of directions representing the shortest path.
        """
        entry_coords: tuple[int, int] = self.get_entry()
        entry_cell: Cell = self.get_cell(entry_coords)

        entry_path: list[list[str], Cell] = [[], entry_cell, entry_coords]

        paths = []
        paths.append(entry_path)

        while True:
            for path in paths:
                cell: Cell = path[1]
                if cell.is_exit():
                    return path[0]
                coords: tuple[int, int] = path[2]
                directions: list[str] | str = cell.get_state_walls(False)

                if len(directions) <= 2 and len(paths) >= 2:
                    last_dir: str | None = None
                    if len(path[0]) > 0:
                        last_dir = path[0][-1]
                    for direction in directions:
                        if len(path[0]) == 0 or direction !=\
                                self.get_opposite_dir(last_dir):
                            path[0].append(direction)
                            next_coords: tuple[int, int] =\
                                self.get_coords_by_dir(coords, direction)
                            next_cell: Cell = self.get_cell(next_coords)
                            path[2] = next_coords
                            path[1] = next_cell
                    if len(directions) == 1 and directions[0] ==\
                            self.get_opposite_dir(last_dir):
                        paths.remove(path)
                else:
                    last_dir: str | None = None
                    if len(path[0]) > 0:
                        last_dir = path[0][-1]
                    for direction in directions:
                        if direction != self.get_opposite_dir(last_dir):
                            new_path: list[list[str], Cell] =\
                                copy.deepcopy(path)
                            new_path[0].append(direction)
                            next_coords: tuple[int, int] =\
                                self.get_coords_by_dir(coords, direction)
                            next_cell: Cell = self.get_cell(next_coords)
                            new_path[2] = next_coords
                            new_path[1] = next_cell
                            paths.append(new_path)
                    paths.remove(path)
