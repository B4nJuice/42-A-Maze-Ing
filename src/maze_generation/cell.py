class Cell():
    def __init__(self) -> None:
        self.__visited: bool = False
        self.__dead: bool = False
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

    def is_dead(self) -> bool:
        return self.__dead

    def set_dead(self) -> None:
        self.set_visited()
        self.__dead = True

    def get_wall(self, direction: str) -> bool:
        return self.__walls[direction]

    def set_wall(self, direction: str, state: bool) -> None:
        self.__walls[direction] = state

    def get_hex_value(self) -> str:
        hex: str = "0123456789ABCDEF"
        dec: int = 0
        i: int = 1
        for direction in ["NORTH", "WEST", "SOUTH", "EST"]:
            if self.get_wall(direction):
                dec += i
            i *= 2
        return hex[dec]
