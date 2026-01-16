from mlx import Mlx
from typing import Any
from src.maze_generation.maze import Maze
from src.maze_generation.cell import Cell


class Displayer():
    def __init__(self, window_size: tuple[int, int], image_size: tuple[int, int], maze: Maze) -> None:
        self.__window_size = window_size
        self.__image_size = image_size
        self.__maze = maze

        mlx = Mlx()
        self.__mlx = mlx
        image_x, image_y = self.get_image_size()

        mlx_ptr = mlx.mlx_init()
        self.__mlx_ptr = mlx_ptr
        win_ptr = mlx.mlx_new_window(mlx_ptr, 1000, 1000, "A-Maze-ing")
        self.__win_ptr = win_ptr
        mlx.mlx_hook(win_ptr, 33, 1 << 17, self.close, None)
        new_img = mlx.mlx_new_image(mlx_ptr, image_x, image_y)
        self.__new_img = new_img
        height: int = maze.get_height()
        width: int = maze.get_width()

        if width >= height:
            size = image_x // width
        elif width < height:
            size = image_y // height
        self.__cell_size = size

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

    def display(self):
        maze = self.get_maze()
        height: int = maze.get_height()
        width: int = maze.get_width()
        size = self.get_cell_size()
        mlx = self.get_mlx()
        mlx_ptr = self.get_mlx_ptr()
        win_ptr = self.get_win_ptr()
        new_img = self.get_new_img()

        for x in range(width):
            for y in range(height):
                coords: tuple[int, int] = (x, y)
                cell: Cell = maze.get_cell(coords)
                walls = cell.get_state_walls(True)
                self.print_cell(coords, walls)
        mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, new_img, 0, 0)
        mlx.mlx_loop(mlx_ptr)

    @staticmethod
    def put_pixel(data, x, y, color, bpp, size_line):
        offset = y * size_line + x * (bpp // 8)
        data[offset:offset + 4] = color.to_bytes(4, 'little')

    def print_west_east(self, pixel_x_start, pixel_y_start):
        size = self.get_cell_size()
        new_img = self.get_new_img()
        mlx = self.get_mlx()
        data, bpb, size_line, endian = mlx.mlx_get_data_addr(new_img)
        for y in range(pixel_y_start, pixel_y_start + size):
            for x in range(pixel_x_start, pixel_x_start + size//4):
                Displayer.put_pixel(data, x, y, 0xFFFF0000, bpb, size_line)

    def print_north_south(self, pixel_x_start, pixel_y_start):
        size = self.get_cell_size()
        new_img = self.get_new_img()
        mlx = self.get_mlx()
        data, bpb, size_line, endian = mlx.mlx_get_data_addr(new_img)
        for y in range(pixel_y_start, pixel_y_start + size//4):
            for x in range(pixel_x_start, pixel_x_start + size):
                Displayer.put_pixel(data, x, y, 0xFFFF0000, bpb, size_line)

    def print_cell(self, coords: tuple[int, int], walls: list[str]):
        x, y = coords
        size = self.get_cell_size()
        pixel_x_start = x * size
        pixel_y_start = y * size
        mlx = self.get_mlx()
        new_img = self.get_new_img()
        data, bpb, size_line, endian = mlx.mlx_get_data_addr(new_img)
        for y in range(pixel_y_start, pixel_y_start + size):
            for x in range(pixel_x_start, pixel_x_start + size):
                Displayer.put_pixel(data, x, y, 0xFFFFFFFF, bpb, size_line)
        if "WEST" in walls:
            self.print_west_east(pixel_x_start, pixel_y_start)
        if "EST" in walls:
            self.print_west_east(pixel_x_start + size * 3 // 4, pixel_y_start)
        if "NORTH" in walls:
            self.print_north_south(pixel_x_start, pixel_y_start)
        if "SOUTH" in walls:
            self.print_north_south(pixel_x_start, pixel_y_start + size * 3//4)

    def close(self, _):
        mlx = self.get_mlx()
        mlx_ptr = self.get_mlx_ptr()
        win_ptr = self.get_win_ptr()
        mlx.mlx_destroy_window(mlx_ptr, win_ptr)
        mlx.mlx_loop_exit(mlx_ptr)
