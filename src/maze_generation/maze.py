from typing import BinaryIO
from src.maze_generation.cell import Cell
from src.maze_generation.seed import (create_seed, next_randint)


class Maze():
    def __init__(self, widht: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], seed: int) -> None:
        self.__matrix: list[list[Cell]] = []
        self.__widht: int = widht
        self.__height: int = height
        self.__entry: tuple[int, int] = entry
        self.__exit: tuple[int, int] = exit
        self.__seed: int = create_seed(seed)

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

        # for y in range(height):
        #     for x in range(widht):
        #         if y == height - 1:
        #             self.set_wall((x, y), "SOUTH", True)
        #         if y == 0:
        #             self.set_wall((x, y), "NORTH", True)

        #         if x == widht - 1:
        #             self.set_wall((x, y), "EST", True)
        #         if x == 0:
        #             self.set_wall((x, y), "WEST", True)

    def get_matrix(self) -> list[list[Cell]]:
        return self.__matrix

    def get_cell(self, coords: tuple[int, int]) -> Cell:
        matrix = self.get_matrix()
        x, y = coords
        cell = matrix[y][x]
        return cell

    def set_wall(self, coords: tuple[int, int], direction: str,
                 state: bool) -> None:
        cell: Cell = self.get_cell(coords)
        cell.set_wall(direction, state)

        x, y = coords
        next_dir: str = None

        match direction:
            case "NORTH":
                if y - 1 >= 0:
                    y -= 1
                    next_dir = "SOUTH"
            case "WEST":
                if x - 1 >= 0:
                    x -= 1
                    next_dir = "EST"
            case "SOUTH":
                if y + 1 < self.__height:
                    y += 1
                    next_dir = "NORTH"
            case "EAST":
                if x + 1 < self.__widht:
                    x += 1
                    next_dir = "WEST"

        if next_dir is not None:
            next_cell: Cell = self.get_cell((x, y))
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

    def create_path(self, coords: tuple[int, int]) -> None:
        seed: int = self.get_seed()

        cell: Cell = self.get_cell(coords)
        cell.set_visited()

        valid_cells: list[tuple[int, int]] = self.check_surroundings(coords)
        n_valid_cells: int = len(valid_cells)

        if n_valid_cells == 0:
            return None

        next_coords: tuple[int, int] = valid_cells[
            next_randint(seed, 0, n_valid_cells)]

        x, y = coords
        directions: dict[tuple[int, int], str] = {
            (x + 1, y): "EST",
            (x - 1, y): "WEST",
            (x, y + 1): "SOUTH",
            (x, y - 1): "NORTH",
        }

        self.set_wall(coords, directions[next_coords], False)
        self.create_path(next_coords)

    def check_surroundings(self,
                           coords: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = coords
        valid_cells: list[str] = []

        cell: Cell = None

        if y + 1 < self.__height:
            cell = self.get_cell((x, y + 1))
            if not cell.is_visited():
                valid_cells.append((x, y + 1))
        if y - 1 >= 0:
            cell = self.get_cell((x, y - 1))
            if not cell.is_visited():
                valid_cells.append((x, y - 1))

        if x + 1 < self.__widht:
            cell = self.get_cell((x + 1, y))
            if not cell.is_visited():
                valid_cells.append((x + 1, y))
        if x - 1 >= 0:
            cell = self.get_cell((x - 1, y))
            if not cell.is_visited():
                valid_cells.append((x - 1, y))
        return valid_cells
