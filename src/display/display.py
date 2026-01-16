from mlx import Mlx
from typing import Any
import math
from src.maze_generation.maze import Maze
from src.maze_generation.cell import Cell


class Displayer():
    def __init__(self, window_size: tuple[int, int], image_size: tuple[int, int], maze: Maze) -> None:
        self.__window_size = window_size
        self.__image_size = image_size
        self.__maze = maze

        mlx = Mlx()
        window_x, window_y = self.get_window_size()
        image_x, image_y = self.get_image_size()
        mlx_ptr = mlx.mlx_init()
        win_ptr = mlx.mlx_new_window(mlx_ptr, window_x, window_y, "A-Maze-ing")
        mlx.mlx_hook(win_ptr, 33, 1 << 17, self.close, None)
        new_img = mlx.mlx_new_image(mlx_ptr, image_x, image_y)

        self.__mlx = mlx
        self.__mlx_ptr = mlx_ptr
        self.__win_ptr = win_ptr
        self.__new_img = new_img

        height: int = maze.get_height()
        width: int = maze.get_width()

        if width >= height:
            size = image_x // width
        elif width < height:
            size = image_y // height
        self.__cell_size = size

        background_color = 0xFFB8B8FF
        walls_color = 0xFF9381FF
        entry_color = 0xFFF8F7FF
        exit_color = 0xFFFFD8BE
        path_color = 0xFFFFEEDD
        icon_color = 0xFFFF92C2
        self.__background_color = background_color
        self.__walls_color = walls_color
        self.__entry_color = entry_color
        self.__exit_color = exit_color
        self.__path_color = path_color
        self.__icon_color = icon_color

    def get_window_size(self) -> Any:
        return self.__window_size

    def get_mlx(self) -> Mlx:
        return self.__mlx

    def get_new_img(self) -> Any:
        return self.__new_img

    def get_maze(self) -> Maze:
        return self.__maze

    def get_image_size(self) -> tuple[int, int]:
        return self.__image_size

    def get_cell_size(self) -> int:
        return self.__cell_size

    def get_mlx_ptr(self) -> Any:
        return self.__mlx_ptr

    def get_win_ptr(self) -> Any:
        return self.__win_ptr

    def get_background_color(self) -> int:
        return self.__background_color

    def get_walls_color(self) -> int:
        return self.__walls_color

    def get_entry_color(self) -> int:
        return self.__entry_color

    def get_exit_color(self) -> int:
        return self.__exit_color

    def get_icon_color(self) -> int:
        return self.__icon_color
    
    def get_path_color(self) -> int:
        return self.__path_color

    def display(self):
        maze = self.get_maze()
        height: int = maze.get_height()
        width: int = maze.get_width()
        mlx = self.get_mlx()
        mlx_ptr = self.get_mlx_ptr()
        win_ptr = self.get_win_ptr()
        new_img = self.get_new_img()
        background_color = self.get_background_color()
        icon_color = self.get_icon_color()
        walls_color = self. get_walls_color()

        for x in range(width):
            for y in range(height):
                coords: tuple[int, int] = (x, y)
                cell: Cell = maze.get_cell(coords)
                walls = cell.get_state_walls(True)
                if (cell.is_icon()):
                    self.print_cell(coords, icon_color)
                else:
                    self.print_cell(coords, background_color)
                self.print_walls(coords, walls, walls_color)

        self.print_entry()
        self.print_exit()
        mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, new_img, 0, 0)
        mlx.mlx_loop(mlx_ptr)

    @staticmethod
    def put_pixel(data, x, y, color, bpp, size_line):
        offset = y * size_line + x * (bpp // 8)
        data[offset:offset + 4] = color.to_bytes(4, 'little')

    def print_entry(self) -> None:
        maze = self.get_maze()
        entry = maze.get_entry()
        entry_color = self.get_entry_color()
        walls_color = self.get_walls_color()
        background_color = self.get_background_color()

        self.print_cell(entry, entry_color)

        cell: Cell = maze.get_cell(entry)

        walls = cell.get_state_walls(False)
        self.print_walls(entry, walls, background_color)
        walls = cell.get_state_walls(True)
        self.print_walls(entry, walls, walls_color)

    def print_exit(self) -> None:
        maze = self.get_maze()
        exit = maze.get_exit()
        exit_color = self.get_exit_color()
        walls_color = self.get_walls_color()
        background_color = self.get_background_color()

        self.print_cell(exit, exit_color)

        cell: Cell = maze.get_cell(exit)

        walls = cell.get_state_walls(False)
        self.print_walls(exit, walls, background_color)
        walls = cell.get_state_walls(True)
        self.print_walls(exit, walls, walls_color)

    def print_cell(self, coords: tuple[int, int], color: int):
        x, y = coords
        size = self.get_cell_size()
        pixel_x = x * size
        pixel_y = y * size
        mlx = self.get_mlx()
        new_img = self.get_new_img()
        data, bpb, size_line, endian = mlx.mlx_get_data_addr(new_img)
        for y in range(pixel_y, pixel_y + size):
            for x in range(pixel_x, pixel_x + size):
                Displayer.put_pixel(data, x, y, color, bpb, size_line)

    def print_west_east(self, pixel_x_start, pixel_y_start, walls_color):
        size = self.get_cell_size()
        new_img = self.get_new_img()
        mlx = self.get_mlx()
        data, bpb, size_line, endian = mlx.mlx_get_data_addr(new_img)
        for y in range(pixel_y_start, pixel_y_start + size):
            for x in range(pixel_x_start, pixel_x_start + size // 4):
                Displayer.put_pixel(data, x, y, walls_color, bpb, size_line)

    def print_north_south(self, pixel_x_start, pixel_y_start, walls_color):
        size = self.get_cell_size()
        new_img = self.get_new_img()
        mlx = self.get_mlx()
        data, bpb, size_line, endian = mlx.mlx_get_data_addr(new_img)
        for y in range(pixel_y_start, pixel_y_start + size // 4):
            for x in range(pixel_x_start, pixel_x_start + size):
                Displayer.put_pixel(data, x, y, walls_color, bpb, size_line)

    def print_walls(self, coords: tuple[int, int], walls: list[str], color: int):
        x, y = coords
        size = self.get_cell_size()
        pixel_x = x * size
        pixel_y = y * size

        if "WEST" in walls:
            self.print_west_east(pixel_x, pixel_y, color)
        if "EST" in walls:
            self.print_west_east(pixel_x + math.ceil(size * 3/4), pixel_y, color)
        if "NORTH" in walls:
            self.print_north_south(pixel_x, pixel_y, color)
        if "SOUTH" in walls:
            self.print_north_south(pixel_x, pixel_y + math.ceil(size * 3/4), color)

    def close(self, _):
        mlx = self.get_mlx()
        mlx_ptr = self.get_mlx_ptr()
        win_ptr = self.get_win_ptr()
        mlx.mlx_destroy_window(mlx_ptr, win_ptr)
        mlx.mlx_loop_exit(mlx_ptr)
