from typing import BinaryIO
from src.maze_generation.cell import Cell


class Maze():
    def __init__(self, widht: int, height: int) -> None:
        self.__matrix: list[list[Cell]] = []
        self.__widht: int = widht
        self.__height: int = height

        for _ in range(height):
            row: list[int] = []
            for _ in range(widht):
                row.append(Cell())
            self.__matrix.append(row)

        for x in range(height):
            for y in range(widht):
                if x == height - 1:
                    self.set_wall((x, y), "SOUTH", True)
                if x == 0:
                    self.set_wall((x, y), "NORTH", True)

                if y == widht - 1:
                    self.set_wall((x, y), "EST", True)
                if y == 0:
                    self.set_wall((x, y), "WEST", True)

    def get_matrix(self) -> list[list[Cell]]:
        return self.__matrix

    def get_cell(self, coords: tuple[int, int]) -> Cell:
        matrix = self.get_matrix()
        x, y = coords
        cell = matrix[x][y]
        return cell

    def set_wall(self, coords: tuple[int, int], direction: str,
                 state: bool) -> None:
        cell: Cell = self.get_cell(coords)
        cell.set_wall(direction, state)

        x, y = coords
        next_dir: str = None

        match direction:
            case "NORTH":
                if x - 1 >= 0:
                    x -= 1
                    next_dir = "SOUTH"
            case "WEST":
                if y - 1 >= 0:
                    y -= 1
                    next_dir = "EST"
            case "SOUTH":
                if x + 1 < self.__height:
                    x += 1
                    next_dir = "NORTH"
            case "EAST":
                if y + 1 < self.__widht:
                    y += 1
                    next_dir = "WEST"

        if next_dir is not None:
            next_cell: Cell = self.get_cell((x, y))
            next_cell.set_wall(next_dir, state)

    def output_in_file(self, file: BinaryIO) -> None:
        output: str = ""
        for x in range(self.__height):
            for y in range(self.__widht):
                cell: Cell = self.get_cell((x, y))
                value: str = cell.get_hex_value()
                output += value
            output += "\n"
        file.write(output)
