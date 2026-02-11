class Cell():
    """
    Class representing a maze cell, with its walls and states (visited, dead, exit, etc).
    """
    def __init__(self) -> None:
        """
        Initialize an empty cell with all walls closed and all states set to False.
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
        """
        Indicates if the cell has been visited.
        :return: True if visited, False otherwise.
        """
        return self.__visited

    def set_visited(self) -> None:
        """
        Mark the cell as visited.
        """
        self.__visited = True

    def is_icon(self) -> bool:
        """
        Indicates if the cell is part of the central icon.
        :return: True if icon, False otherwise.
        """
        return self.__icon

    def set_icon(self) -> None:
        """
        Mark the cell as part of the icon and set it as dead.
        """
        self.set_dead()
        self.__icon = True

    def is_dead(self) -> bool:
        """
        Indicates if the cell is dead (no longer part of the path).
        :return: True if dead, False otherwise.
        """
        return self.__dead

    def set_dead(self) -> None:
        """
        Mark the cell as dead and visited.
        """
        self.set_visited()
        self.__dead = True

    def set_exit(self) -> None:
        """
        Mark the cell as the maze exit.
        """
        self.__exit = True

    def set_after_exit(self) -> None:
        """
        Mark the cell as after the exit (for maze generation).
        """
        self.__after_exit = True

    def is_after_exit(self) -> bool:
        """
        Indicates if the cell is after the exit.
        :return: True if after exit, False otherwise.
        """
        return self.__after_exit

    def is_exit(self) -> bool:
        """
        Indicates if the cell is the maze exit.
        :return: True if exit, False otherwise.
        """
        return self.__exit

    def get_wall(self, direction: str) -> bool:
        """
        Returns the state (open/closed) of the wall in a given direction.
        :param direction: Wall direction (NORTH, SOUTH, EST, WEST).
        :return: True if wall present, False otherwise.
        """
        return self.__walls[direction]

    def get_state_walls(self, state: bool) -> list[str]:
        """
        Returns the list of directions where the wall is in the given state.
        :param state: True for present walls, False for open.
        :return: List of corresponding directions.
        """
        dir_list: list[str] = []

        for direction in ["NORTH", "EST", "SOUTH", "WEST"]:
            if self.get_wall(direction) is state:
                dir_list.append(direction)
        return dir_list

    def set_wall(self, direction: str, state: bool) -> None:
        """
        Set the state (open/closed) of a wall in a given direction.
        :param direction: Wall direction (NORTH, SOUTH, EST, WEST).
        :param state: True for wall present, False for open.
        """
        self.__walls[direction] = state

    def get_hex_value(self) -> str:
        """
        Returns the hexadecimal value representing the state of the cell's walls.
        :return: Hexadecimal string.
        """
        hex: str = "0123456789ABCDEF"
        dec: int = 0
        i: int = 1
        for direction in ["NORTH", "EST", "SOUTH", "WEST"]:
            if self.get_wall(direction):
                dec += i
            i *= 2
        return hex[dec]
