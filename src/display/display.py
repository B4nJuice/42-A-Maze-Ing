from mlx import Mlx
from typing import Any
import math
import time
from src.maze_generation.maze import Maze
from src.maze_generation.cell import Cell


class Displayer():
    """
    Class for displaying a maze using the MLX library.
    Manages the window, image, colors, and rendering of cells, walls, path, entry, and exit.
    """
    def __init__(self,
                 window_size: tuple[int, int],
                 image_size: tuple[int, int],
                 maze: Maze,
                 wall_percent: int) -> None:
        """
        Initialize the Displayer with sizes, maze, and colors.
        :param window_size: Window size (x, y).
        :param image_size: Image size (x, y).
        :param maze: Maze object to display.
        :param wall_percent: Wall size percentage.
        """

        mlx = Mlx()
        mlx_ptr = mlx.mlx_init()

        _, screen_size_x, screen_size_y = mlx.mlx_get_screen_size(mlx_ptr)

        for x, y in (window_size, image_size):
            if x <= 0 or y <= 0:
                size: int = round(min(screen_size_x, screen_size_y)*0.75)
                window_size = (size, size)
                image_size = (size, size)
                break

        self.__window_size = window_size
        self.__image_size = image_size
        self.__maze = maze

        window_x, window_y = self.get_window_size()
        image_x, image_y = self.get_image_size()

        height: int = maze.get_height()
        width: int = maze.get_width()

        if width >= height:
            size = image_x // width
        elif width < height:
            size = image_y // height
        self.__cell_size = size

        self.x_offset = (image_x - size*width) // 2
        self.y_offset = (image_y - size*height) // 2

        win_ptr = mlx.mlx_new_window(mlx_ptr, window_x, window_y, "A-Maze-ing")
        mlx.mlx_hook(win_ptr, 33, 1 << 17, self.close, None)
        new_img = mlx.mlx_new_image(mlx_ptr, image_x, image_y)

        self.__mlx = mlx
        self.__mlx_ptr = mlx_ptr
        self.__win_ptr = win_ptr
        self.__new_img = new_img

        if wall_percent <= 0:
            wall_percent = 1
        div = round(1 / wall_percent * 100)
        self.__div = div

        self.set_color("walls", (0, 0, 0))
        self.set_color("background", (239, 233, 244))
        self.set_color("icon",  (0, 0, 0))
        self.set_color("entry", (88, 99, 248))
        self.set_color("exit", (88, 99, 248))
        self.set_color("path", (95, 191, 249))

    def set_color(
                self,
                location: str,
                rgb: tuple[int, int, int]
            ) -> bool:

        red, green, blue = rgb

        red = abs(red) % 256
        green = abs(green) % 256
        blue = abs(blue) % 256

        color: int = (0xFF << 24) | (red << 16) | (green << 8) | blue

        match location:
            case "background":
                self.__background_color = color
                return True
            case "walls":
                self.__walls_color = color
                return True
            case "entry":
                self.__entry_color = color
                return True
            case "exit":
                self.__exit_color = color
                return True
            case "path":
                self.__path_color = color
                return True
            case "icon":
                self.__icon_color = color
                return True
            case _:
                return False

    def get_window_size(self) -> tuple[int, int]:
        """
        Returns the window size.
        :return: Tuple (x, y).
        """
        return self.__window_size

    def get_mlx(self) -> Mlx:
        """
        Returns the Mlx object used.
        :return: Mlx object.
        """
        return self.__mlx

    def get_new_img(self) -> Any:
        """
        Returns the Mlx image used for rendering.
        :return: Mlx image.
        """
        return self.__new_img

    def get_maze(self) -> Maze:
        """
        Returns the maze to display.
        :return: Maze object.
        """
        return self.__maze

    def get_image_size(self) -> tuple[int, int]:
        """
        Returns the image size.
        :return: Tuple (x, y).
        """
        return self.__image_size

    def get_cell_size(self) -> int:
        """
        Returns the size of a cell.
        :return: Integer.
        """
        return self.__cell_size

    def get_mlx_ptr(self) -> Any:
        """
        Returns the MLX pointer.
        :return: MLX pointer.
        """
        return self.__mlx_ptr

    def get_win_ptr(self) -> Any:
        """
        Returns the MLX window pointer.
        :return: Window pointer.
        """
        return self.__win_ptr

    def get_div(self) -> int:
        """
        Returns the divider used for wall size.
        :return: Integer.
        """
        return self.__div

    def get_background_color(self) -> int:
        """
        Returns the background color.
        :return: Color (int).
        """
        return self.__background_color

    def get_walls_color(self) -> int:
        """
        Returns the wall color.
        :return: Color (int).
        """
        return self.__walls_color

    def get_entry_color(self) -> int:
        """
        Returns the entry color.
        :return: Color (int).
        """
        return self.__entry_color

    def get_exit_color(self) -> int:
        """
        Returns the exit color.
        :return: Color (int).
        """
        return self.__exit_color

    def get_icon_color(self) -> int:
        """
        Returns the central icon color.
        :return: Color (int).
        """
        return self.__icon_color

    def get_path_color(self) -> int:
        """
        Returns the path color.
        :return: Color (int).
        """
        return self.__path_color

    def display(self):
        """
        Displays the complete maze in the MLX window.
        """
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

        self.print_path()
        self.print_entry()
        self.print_exit()
        mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, new_img, 0, 0)
        mlx.mlx_loop(mlx_ptr)

    def start_animated_display(self, fps: int):
        """
        Starts the animated display of the maze with a given number of frames per second.
        :param fps: Frames per second.
        """
        mlx = self.get_mlx()
        mlx_ptr = self.get_mlx_ptr()

        self.fps = fps
        self.timestamp = time.time()
        self.first = True

        mlx.mlx_loop_hook(mlx_ptr, self.__animate_display, None)
        mlx.mlx_loop(mlx_ptr)

    def __animate_display(self, _):
        """
        Internal function to handle display animation.
        """
        maze = self.get_maze()
        height: int = maze.get_height()
        width: int = maze.get_width()
        mlx = self.get_mlx()
        mlx_ptr = self.get_mlx_ptr()
        win_ptr = self.get_win_ptr()
        new_img = self.get_new_img()
        background_color = self.get_background_color()
        icon_color = self.get_icon_color()
        walls_color = self.get_walls_color()

        if self.first:
            for x in range(width):
                for y in range(height):
                    coords: tuple[int, int] = (x, y)
                    cell: Cell = maze.get_cell(coords)
                    if cell.is_icon():
                        self.print_cell(coords, icon_color)
                        walls = cell.get_state_walls(True)
                        self.print_walls(coords, walls, walls_color)
                    else:
                        self.print_cell(coords, walls_color)
            mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, new_img, 0, 0)

            entry_coords: tuple[int, int] = maze.get_entry()

            self.visited: set[tuple[int, int]] = set()
            self.stack: list[tuple[int, int]] = [entry_coords]

        if self.fps <= 0:
            self.fps = 1
        frame_delay = 1 / self.fps

        if time.time() - self.timestamp >= frame_delay or self.first:
            self.timestamp = time.time()
        else:
            return

        if len(self.stack) or self.first:
            actual_len: int = len(self.visited)
            while len(self.visited) == actual_len:
                coords = self.stack.pop()
                if coords in self.visited:
                    continue
                self.visited.add(coords)

                cell: Cell = maze.get_cell(coords)

                self.print_cell(coords, background_color)
                walls = cell.get_state_walls(True)
                self.print_walls(coords, walls, walls_color)

                mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, new_img, 0,
                                            0)

                directions = cell.get_state_walls(False)
                if isinstance(directions, str):
                    directions = [directions]

                for direction in directions:
                    next_coords: tuple[int, int] = (
                        maze.get_coords_by_dir(coords, direction)
                    )
                    if next_coords not in self.visited:
                        self.stack.append(next_coords)
                self.first = False
        else:
            self.print_path()
            self.print_entry()
            self.print_exit()
            mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, new_img, 0, 0)

    @staticmethod
    def put_pixel(data, x, y, color, bpp, size_line):
        """
        Puts a colored pixel at a given position in the MLX image.
        :param data: Image data.
        :param x: X position.
        :param y: Y position.
        :param color: Pixel color.
        :param bpp: Bits per pixel.
        :param size_line: Line size.
        """
        offset = y * size_line + x * (bpp // 8)
        data[offset:offset + 4] = color.to_bytes(4, 'little')

    def print_entry(self) -> None:
        """
        Displays the maze entry cell.
        """
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
        """
        Displays the maze exit cell.
        """
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
        """
        Displays a cell at given coordinates with a given color.
        :param coords: Cell coordinates.
        :param color: Color to use.
        """
        x, y = coords
        size = self.get_cell_size()
        pixel_x = x * size
        pixel_y = y * size
        mlx = self.get_mlx()
        new_img = self.get_new_img()
        data, bpb, size_line, endian = mlx.mlx_get_data_addr(new_img)
        for y in range(pixel_y, pixel_y + size):
            for x in range(pixel_x, pixel_x + size):
                Displayer.put_pixel(
                    data,
                    x + self.x_offset,
                    y + self.y_offset,
                    color,
                    bpb,
                    size_line
                )

    def print_west_east(self, pixel_x_start, pixel_y_start, walls_color):
        """
        Displays a West or East wall for a cell.
        :param pixel_x_start: Starting x position.
        :param pixel_y_start: Starting y position.
        :param walls_color: Wall color.
        """
        size = self.get_cell_size()
        new_img = self.get_new_img()
        div = self.get_div()
        mlx = self.get_mlx()
        data, bpb, size_line, endian = mlx.mlx_get_data_addr(new_img)
        for y in range(pixel_y_start, pixel_y_start + size):
            for x in range(pixel_x_start, pixel_x_start + size // div):
                Displayer.put_pixel(data, x, y, walls_color, bpb, size_line)

    def print_north_south(self, pixel_x_start, pixel_y_start, walls_color):
        """
        Displays a North or South wall for a cell.
        :param pixel_x_start: Starting x position.
        :param pixel_y_start: Starting y position.
        :param walls_color: Wall color.
        """
        size = self.get_cell_size()
        new_img = self.get_new_img()
        div = self.get_div()
        mlx = self.get_mlx()
        data, bpb, size_line, endian = mlx.mlx_get_data_addr(new_img)
        for y in range(pixel_y_start, pixel_y_start + size // div):
            for x in range(pixel_x_start, pixel_x_start + size):
                Displayer.put_pixel(data, x, y, walls_color, bpb, size_line)

    def print_walls(self, coords: tuple[int, int], walls: list[str],
                    color: int):
        """
        Displays all the walls of a cell according to the directions.
        :param coords: Cell coordinates.
        :param walls: List of wall directions.
        :param color: Wall color.
        """
        x, y = coords
        size = self.get_cell_size()
        div = self.get_div()
        add_to_coord = math.ceil(size * (div-1)/div)
        pixel_x = x * size + self.x_offset
        pixel_y = y * size + self.y_offset

        if "WEST" in walls:
            self.print_west_east(pixel_x, pixel_y, color)
        if "EST" in walls:
            self.print_west_east(pixel_x + add_to_coord, pixel_y, color)
        if "NORTH" in walls:
            self.print_north_south(pixel_x, pixel_y, color)
        if "SOUTH" in walls:
            self.print_north_south(pixel_x, pixel_y + add_to_coord, color)

    def print_path(self):
        """
        Displays the shortest path in the maze.
        """
        maze = self.get_maze()
        coords = maze.get_entry()
        path_color = self.get_path_color()
        walls_color = self.get_walls_color()
        for char in maze.get_shortest_path():
            coords = maze.get_coords_by_dir(coords, char)
            self.print_cell(coords, path_color)
            cell = maze.get_cell(coords)
            walls = cell.get_state_walls(True)
            self.print_walls(coords, walls, walls_color)

    def close(self, _):
        """
        Closes the MLX window and exits the loop.
        """
        mlx = self.get_mlx()
        mlx_ptr = self.get_mlx_ptr()
        win_ptr = self.get_win_ptr()
        mlx.mlx_destroy_window(mlx_ptr, win_ptr)
        mlx.mlx_loop_exit(mlx_ptr)
