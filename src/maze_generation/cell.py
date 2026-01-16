class Cell():
    def __init__(self) -> None:
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
        return self.__visited

    def set_visited(self) -> None:
        self.__visited = True

    def is_icon(self) -> bool:
        return self.__icon

    def set_icon(self) -> None:
        self.set_dead()
        self.__icon = True

    def is_dead(self) -> bool:
        return self.__dead

    def set_dead(self) -> None:
        self.set_visited()
        self.__dead = True

    def set_exit(self) -> None:
        self.__exit = True

    def set_after_exit(self) -> None:
        self.__after_exit = True

    def is_after_exit(self) -> bool:
        return self.__after_exit

    def is_exit(self) -> bool:
        return self.__exit

    def get_wall(self, direction: str) -> bool:
        return self.__walls[direction]

    def get_state_walls(self, state: bool) -> list[str]:
        dir_list: list[str] = []

        for direction in ["NORTH", "EST", "SOUTH", "WEST"]:
            if self.get_wall(direction) is state:
                dir_list.append(direction)
        return dir_list

    def set_wall(self, direction: str, state: bool) -> None:
        self.__walls[direction] = state

    def get_hex_value(self) -> str:
        hex: str = "0123456789ABCDEF"
        dec: int = 0
        i: int = 1
        for direction in ["NORTH", "EST", "SOUTH", "WEST"]:
            if self.get_wall(direction):
                dec += i
            i *= 2
        return hex[dec]
