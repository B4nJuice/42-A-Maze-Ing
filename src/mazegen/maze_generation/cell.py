class Cell():
    """Represent a single maze cell.

    Stores the state of the four walls and boolean flags used during
    maze generation and pathfinding (visited, dead, exit, after-exit,
    icon).

    Attributes
    ----------
    visited : bool
        Whether the cell has been visited during maze generation.
    dead : bool
        Whether the cell is dead (excluded from the main path).
    exit : bool
        Whether this cell is the maze exit.
    after_exit : bool
        Whether the cell is located after the exit.
    icon : bool
        Whether the cell is part of the central icon.
    walls : dict[str, bool]
        Dictionary storing wall states for each direction.
    """
    def __init__(self) -> None:
        """Initialize a cell with default states.

        All walls are initialized as closed and all state flags are set to
        False.

        Returns
        -------
        None
        """
        self.__visited: bool = False
        self.__dead: bool = False
        self.__exit: bool = False
        self.__after_exit: bool = False
        self.__icon: bool = False
        self.__walls: dict[str, bool] = {
            "NORTH": False,
            "WEST": False,
            "SOUTH": False,
            "EST": False,
        }

    def is_visited(self) -> bool:
        """Check whether the cell has been visited.

        Returns
        -------
        bool
            True if the cell was visited, False otherwise.
        """
        return self.__visited

    def set_visited(self) -> None:
        """Mark the cell as visited.

        Returns
        -------
        None
        """
        self.__visited = True

    def is_icon(self) -> bool:
        """Check whether the cell is part of the central icon.

        Returns
        -------
        bool
            True if the cell is an icon cell, False otherwise.
        """
        return self.__icon

    def set_icon(self) -> None:
        """Mark the cell as part of the icon.

        This also marks the cell as dead (not part of the main path).

        Returns
        -------
        None
        """
        self.set_dead()
        self.__icon = True

    def is_dead(self) -> bool:
        """Check whether the cell is dead (excluded from the path).

        Returns
        -------
        bool
            True if dead, False otherwise.
        """
        return self.__dead

    def set_dead(self) -> None:
        """Mark the cell as dead and visited.

        Returns
        -------
        None
        """
        self.set_visited()
        self.__dead = True

    def set_exit(self) -> None:
        """Mark this cell as the maze exit.

        Returns
        -------
        None
        """
        self.__exit = True

    def set_after_exit(self) -> None:
        """Mark the cell as being located after the exit.

        Returns
        -------
        None
        """
        self.__after_exit = True

    def is_after_exit(self) -> bool:
        """Check whether the cell is after the exit.

        Returns
        -------
        bool
            True if after-exit, False otherwise.
        """
        return self.__after_exit

    def is_exit(self) -> bool:
        """Check whether the cell is the maze exit.

        Returns
        -------
        bool
            True if this cell is the exit, False otherwise.
        """
        return self.__exit

    def get_wall(self, direction: str) -> bool:
        """Get the state of a wall in the specified direction.

        Parameters
        ----------
        direction : str
            One of "NORTH", "SOUTH", "EST", "WEST".

        Returns
        -------
        bool
            True if the wall is present (closed), False if open.
        """
        return self.__walls[direction]

    def get_state_walls(self, state: bool) -> list[str]:
        """Return a list of wall directions that match the given state.

        Parameters
        ----------
        state : bool
            True to list present (closed) walls, False to list open walls.

        Returns
        -------
        list[str]
            Directions in the order ["NORTH", "EST", "SOUTH", "WEST"].
        """
        dir_list: list[str] = []

        for direction in ["NORTH", "EST", "SOUTH", "WEST"]:
            if self.get_wall(direction) is state:
                dir_list.append(direction)
        return dir_list

    def set_wall(self, direction: str, state: bool) -> None:
        """Set the state of a wall.

        Parameters
        ----------
        direction : str
            One of "NORTH", "SOUTH", "EST", "WEST".
        state : bool
            True to close/present the wall, False to open it.

        Returns
        -------
        None
        """
        self.__walls[direction] = state

    def get_hex_value(self) -> str:
        """Return a single hexadecimal character representing the walls.

        The four walls are treated as bits in the order
        ["NORTH", "EST", "SOUTH", "WEST"], least-significant first.
        The resulting value is mapped to a hexadecimal character (0..F).

        Returns
        -------
        str
            A single hex character representing the wall bitmask.
        """
        hex: str = "0123456789ABCDEF"
        dec: int = 0
        i: int = 1
        for direction in ["NORTH", "EST", "SOUTH", "WEST"]:
            if self.get_wall(direction):
                dec += i
            i *= 2
        return hex[dec]
