from typing import BinaryIO
from src.maze_generation.cell import Cell
from src.maze_generation.seed import (create_seed, next_randint)


class Maze():
    def __init__(self, widht: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool, seed: int) -> None:
        self.__matrix: list[list[Cell]] = []
        self.__widht: int = widht
        self.__height: int = height
        self.__entry: tuple[int, int] = entry
        self.__exit: tuple[int, int] = exit
        self.__seed: int = create_seed(seed)
        self.__perfect = perfect
        self.__after_exit = False

        for _ in range(height):
            row: list[int] = []
            for _ in range(widht):
                cell: Cell = Cell()
                cell.set_wall("SOUTH", True)
                cell.set_wall("NORTH", True)
                cell.set_wall("EST", True)
                cell.set_wall("WEST", True)
                row.append(cell)
            self.__matrix.append(row)

        exit_cell: Cell = self.get_cell(exit)
        exit_cell.set_exit()

    def get_matrix(self) -> list[list[Cell]]:
        return self.__matrix

    def get_cell(self, coords: tuple[int, int]) -> Cell:
        matrix = self.get_matrix()
        x, y = coords
        if x < 0 or y < 0 or x >= self.__widht or y >= self.__height:
            return None
        cell = matrix[y][x]
        return cell

    def is_perfect(self) -> bool:
        return self.__perfect

    def is_after_exit(self) -> bool:
        return self.__after_exit

    def invert_after_exit(self) -> None:
        self.__after_exit = True is not self.__after_exit

    def set_wall(self, coords: tuple[int, int], direction: str,
                 state: bool) -> None:
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
                if x + 1 < self.__widht:
                    next_coords = (x + 1, y)
                    next_dir = "WEST"

        if next_dir is not None:
            next_cell: Cell = self.get_cell(next_coords)
            next_cell.set_wall(next_dir, state)

    def output_in_file(self, file: BinaryIO) -> None:
        output: str = ""
        for y in range(self.__height):
            for x in range(self.__widht):
                cell: Cell = self.get_cell((x, y))
                value: str = cell.get_hex_value()
                output += value
            output += "\n"

        output += "\n"

        for x, y in [self.__entry, self.__exit]:
            output += f"{x},{y}\n"

        file.write(output)

    def get_seed(self) -> int:
        return self.__seed

    def get_entry(self) -> tuple[int, int]:
        return self.__entry

    def get_exit(self) -> tuple[int, int]:
        return self.__exit

    def create_path(self, coords: tuple[int, int],
                    last_coords: tuple[int, int] = None) -> tuple[int, int]:
        seed: int = self.get_seed()

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
            next_randint(seed, 0, n_valid_cells)]

        x, y = coords
        directions: dict[tuple[int, int], str] = {
            (x + 1, y): "EST",
            (x - 1, y): "WEST",
            (x, y + 1): "SOUTH",
            (x, y - 1): "NORTH",
        }

        self.set_wall((coords), directions[next_coords], False)
        return self.create_path(next_coords, coords)

    def find_next_cell(self, coords: tuple[int, int]) -> tuple[int, int]:
        cell: Cell = self.get_cell(coords)

        if cell.is_exit():
            self.invert_after_exit()

        x, y = coords
        directions: dict[str, tuple[int, int]] = {
            "EST": (x + 1, y),
            "WEST": (x - 1, y),
            "SOUTH": (x, y + 1),
            "NORTH": (x, y - 1),
        }

        open_walls = cell.get_state_walls(False)
        valid_cells: list[tuple[int, int]] = []
        visited_cells: list[tuple[int, int]] = []

        for direction in open_walls:
            check_coords: tuple[int, int] = directions[direction]
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
            seed = self.get_seed()
            next_cell: tuple[int, int] = visited_cells[
                next_randint(seed, 0, n_visited_cells)]
            return self.find_next_cell(next_cell)

        return coords

    def check_surroundings(self,
                           coords: tuple[int, int]) -> list[tuple[int, int]]:
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

        if x + 1 < self.__widht:
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

    def create_full_maze(self):
        entry_coords: tuple[int, int] = self.get_entry()
        next_coords: tuple[int, int] = self.create_path(entry_coords)
        next_coords = self.find_next_cell(next_coords)

        while next_coords is not None:
            next_coords = self.create_path(next_coords)
            next_coords = self.find_next_cell(next_coords)

        if not self.is_perfect():
            possible_breach: list[tuple[str, tuple[int, int]]] = []

            for y in range(self.__height):
                for x in range(self.__widht):
                    cell: Cell = self.get_cell((x, y))

                    if cell.is_exit():
                        continue

                    closed_walls = cell.get_state_walls(True)

                    next_cell: Cell = self.get_cell((x, y + 1))
                    if "SOUTH" in closed_walls and next_cell is not None:
                        if next_cell.is_exit():
                            continue
                        if next_cell.is_after_exit() != cell.is_after_exit():
                            possible_breach.append(tuple(("SOUTH", (x, y))))

                    next_cell: Cell = self.get_cell((x + 1, y))
                    if "EST" in closed_walls and next_cell is not None:
                        if next_cell.is_exit():
                            continue
                        if next_cell.is_after_exit() != cell.is_after_exit():
                            possible_breach.append(tuple(("EST", (x, y))))

            n_possible_breach: int = len(possible_breach)

            if n_possible_breach > 0:
                seed: int = self.get_seed()
                n_breach: int = next_randint(seed, 1, 3)
                for _ in range(n_breach):
                    direction, coords = possible_breach[
                        next_randint(seed, 0, n_possible_breach)]
                    self.set_wall(coords, direction, False)
