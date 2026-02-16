from mlx import Mlx
from typing import Any
import math
import time
from typing import TextIO
from src.maze_generation.maze import Maze
from src.maze_generation.cell import Cell
from src.display.button import Button
from src.display.button import ButtonText


class PlayerError(Exception):
    def __init__(self, message: str = "undefined"):
        super().__init__(f"PlayerError: {message}")


class SpacingError(Exception):
    def __init__(self, message: str = "undefined"):
        super().__init__(f"SpacingError: {message}")


class Displayer():
    """
    Display a maze using the MLX library.

    Manages the window, image, colors and rendering of cells, walls,
    path, entry and exit.
    """
    def __init__(self,
                 window_size: tuple[int, int],
                 image_size: tuple[int, int],
                 maze: Maze,
                 wall_thickness: int) -> None:
        """
        Initialize a Displayer.

        Parameters
        ----------
        window_size : tuple[int, int]
            Window size (x, y).
        image_size : tuple[int, int]
            Image size (x, y).
        maze : Maze
            Maze object to display.
        wall_thickness : int
            Wall size percentage.

        Returns
        -------
        None
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

        self.animation_finished: bool = True

        window_x, window_y = self.get_window_size()
        image_x, image_y = self.get_image_size()

        height: int = maze.get_height()
        width: int = maze.get_width()

        if width >= height:
            size = image_x // width
        elif width < height:
            size = image_y // height
        self.__cell_size = size

        self.x_offset = (image_x - size * width) // 2
        self.y_offset = (image_y - size * height) // 2

        win_ptr = mlx.mlx_new_window(mlx_ptr, window_x, window_y, "A-Maze-ing")
        mlx.mlx_hook(win_ptr, 33, 1 << 17, self.close, None)
        mlx.mlx_hook(win_ptr, 2, 1 << 0, self.key_press, None)
        mlx.mlx_hook(win_ptr, 4, 1 << 2, self.mouse_event, None)
        new_img = mlx.mlx_new_image(mlx_ptr, image_x, image_y)

        self.__mlx = mlx
        self.__mlx_ptr = mlx_ptr
        self.__win_ptr = win_ptr
        self.__new_img = new_img

        if wall_thickness <= 0:
            wall_thickness = 1
        div = round(1 / wall_thickness * 100)
        self.__div = div

        self.set_color("walls", (0, 0, 0))
        self.set_color("background", (239, 233, 244))
        self.set_color("icon",  (0, 0, 0))
        self.set_color("entry", (88, 99, 248))
        self.set_color("exit", (88, 99, 248))
        self.set_color("path", (95, 191, 249))

        self.set_toggle_path(False)

        self.move_mode: bool = False
        self.player_pos: tuple[int, int] = (0, 0)

        self.buttons: list[Button] = []
        self.win_buttons_ptr: Any
        self.win_buttons_size: tuple[int, int] = (window_x // 2, window_y)
        self.buttons_img: Any
        self.spacing: int = 50
        self.button_printer_x: int = self.spacing
        self.button_printer_y: int = self.spacing
        self.win_buttons()

        self.custom_player: None = None
        self.auto_adjust_player: bool = True
        self.custom_player_colors: dict = {}

    def set_maze(self, new: Maze) -> None:
        self.__maze = new

    def set_spacing(self, spacing: int) -> None:
        if spacing <= 0:
            raise SpacingError("Spacing must be greater than 0.")

        x, y = self.win_buttons_size
        if spacing > x // 2 or spacing > y // 2:
            raise SpacingError("Spacing is too large for the window button.")

        self.spacing = spacing
        self.button_printer_x = spacing
        self.button_printer_y = spacing

    def set_custom_player_colors(self, colors: dict[str, tuple]) -> None:
        self.custom_player_colors = colors

    def set_auto_adjust_player(self, auto_adjust_player: bool) -> None:
        if not isinstance(auto_adjust_player, bool):
            raise ValueError("auto_adjust_player has to be a bool.")
        self.auto_adjust_player = auto_adjust_player

    def set_toggle_path(self, toggle: bool) -> None:
        if not isinstance(toggle, bool):
            raise ValueError("toggle has to be a bool.")
        self.toggle_path = toggle

    def set_color(self, location: str,
                  rgb: tuple[int, int, int]) -> bool:
        """
        Set a color for a specific UI location.

        Parameters
        ----------
        location : str
            One of "background", "walls", "entry", "exit", "path", or "icon".
        rgb : tuple[int, int, int]
            RGB values (0-255) for the color.

        Returns
        -------
        bool
            True if the color was applied, False if the location is unknown.
        """

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
        Return the window size.

        Returns
        -------
        tuple[int, int]
            Window size as (x, y).
        """
        return self.__window_size

    def get_mlx(self) -> Mlx:
        """
        Return the MLX instance.

        Returns
        -------
        Mlx
            The MLX instance used for window and image operations.
        """
        return self.__mlx

    def get_new_img(self) -> Any:
        """
        Return the MLX image used for rendering.

        Returns
        -------
        Any
            The MLX image object (implementation-specific).
        """
        return self.__new_img

    def get_maze(self) -> Maze:
        """
        Return the maze to display.

        Returns
        -------
        Maze
            The Maze instance being displayed.
        """
        return self.__maze

    def get_image_size(self) -> tuple[int, int]:
        """
        Return the image size.

        Returns
        -------
        tuple[int, int]
            Image size as (x, y).
        """
        return self.__image_size

    def get_cell_size(self) -> int:
        """
        Return the size (in pixels) of a single maze cell.

        Returns
        -------
        int
            Cell size in pixels.
        """
        return self.__cell_size

    def get_mlx_ptr(self) -> Any:
        """
        Return the raw MLX context pointer.

        Returns
        -------
        Any
            Low-level MLX context pointer required by the wrapper.
        """
        return self.__mlx_ptr

    def get_win_ptr(self) -> Any:
        """
        Return the MLX window pointer.

        Returns
        -------
        Any
            Low-level MLX window pointer.
        """
        return self.__win_ptr

    def get_div(self) -> int:
        """
        Return the divider used to compute wall thickness.

        Returns
        -------
        int
            Divider value used when drawing walls.
        """
        return self.__div

    def get_background_color(self) -> int:
        """
        Return the background color.

        Returns
        -------
        int
            Color as a 32-bit integer (0xAARRGGBB).
        """
        return self.__background_color

    def get_walls_color(self) -> int:
        """
        Return the wall color.

        Returns
        -------
        int
            Color as a 32-bit integer (0xAARRGGBB).
        """
        return self.__walls_color

    def get_entry_color(self) -> int:
        """
        Return the entry cell color.

        Returns
        -------
        int
            Color as a 32-bit integer (0xAARRGGBB).
        """
        return self.__entry_color

    def get_exit_color(self) -> int:
        """
        Return the exit cell color.

        Returns
        -------
        int
            Color as a 32-bit integer (0xAARRGGBB).
        """
        return self.__exit_color

    def get_icon_color(self) -> int:
        """
        Return the central icon color.

        Returns
        -------
        int
            Color as a 32-bit integer (0xAARRGGBB).
        """
        return self.__icon_color

    def get_path_color(self) -> int:
        """
        Return the path color.

        Returns
        -------
        int
            Color as a 32-bit integer (0xAARRGGBB).
        """
        return self.__path_color

    def display(self, loop: bool = True) -> None:
        """
        Display the complete maze in the MLX window.

        Renders all cells, walls, path, entry and exit, then puts the image
        to the window and starts the MLX event loop.

        Returns
        -------
        None
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

        buf, bpp, size_line, endian = mlx.mlx_get_data_addr(new_img)

        addr: memoryview[int] = buf.cast('B')

        image_width, image_height = self.get_image_size()

        addr[:] = \
            background_color.to_bytes(bpp // 8, 'little') \
            * (image_width * image_height)

        for x in range(width):
            for y in range(height):
                coords: tuple[int, int] = (x, y)
                cell: Cell = maze.get_cell(coords)
                walls = cell.get_state_walls(True)
                if (cell.is_icon()):
                    self.print_cell(coords, icon_color)
                self.print_walls(coords, walls, walls_color)

        self.print_path()
        self.print_entry()
        self.print_exit()
        if self.move_mode:
            self.print_player(self.get_walls_color())
        mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, new_img, 0, 0)
        if loop:
            mlx.mlx_loop(mlx_ptr)

    def __static_display(self, _: None = None) -> None:
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
        if self.move_mode is True:
            self.print_player(self.get_walls_color())
        mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, new_img, 0, 0)

    def key_press(self, keycode: int, _: None) -> None:
        esc = 65307
        move_mode = 109
        left = 65361
        up = 65362
        right = 65363
        down = 65364

        if keycode == esc:
            self.close(None)

        maze = self.get_maze()

        mlx = self.get_mlx()
        mlx_ptr = self.get_mlx_ptr()
        win_ptr = self.get_win_ptr()
        new_img = self.get_new_img()
        if keycode == move_mode:
            self.move_mode = not self.move_mode
            if self.move_mode:
                self.player_pos = maze.get_entry()
                self.print_player(self.get_walls_color())
            else:
                self.display(False)

        if self.move_mode is True and keycode in range(65361, 65365):
            x, y = self.player_pos
            cell = maze.get_cell(self.player_pos)

            if keycode == left and not cell.get_wall("WEST"):
                self.player_pos = x - 1, y
            elif keycode == up and not cell.get_wall("NORTH"):
                self.player_pos = x, y - 1
            elif keycode == right and not cell.get_wall("EST"):
                self.player_pos = x + 1, y
            elif keycode == down and not cell.get_wall("SOUTH"):
                self.player_pos = x, y + 1
            if (x, y) != self.player_pos:
                cell_dict: dict[tuple, int] = {
                    maze.get_exit(): self.get_exit_color(),
                    maze.get_entry(): self.get_entry_color(),
                }

                cell_color = self.get_background_color()
                if (maze.is_in_shortest_path(cell)
                        and self.toggle_path and self.animation_finished):
                    cell_color = self.get_path_color()

                if cell_dict.get((x, y)) and self.animation_finished:
                    cell_color = cell_dict[(x, y)]
                self.print_cell((x, y), cell_color)
                self.print_walls(
                    (x, y), cell.get_state_walls(True),
                    self.get_walls_color())
                self.print_player(self.get_walls_color())

        mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, new_img, 0, 0)

    def start_static_display(self) -> None:
        mlx = self.get_mlx()
        mlx_ptr = self.get_mlx_ptr()
        win_ptr = self.get_win_ptr()

        mlx.mlx_hook(win_ptr, 2, 1 << 0, self.key_press, None)
        mlx.mlx_hook(win_ptr, 4, 1 << 2, self.mouse_event, None)
        mlx.mlx_loop_hook(mlx_ptr, self.__static_display, None)
        mlx.mlx_loop(mlx_ptr)

    def start_animated_display(self, fps: int) -> None:
        """
        Start an animated display of the maze.

        Parameters
        ----------
        fps : int
            Target frames per second for the animation.

        Returns
        -------
        None
        """
        mlx = self.get_mlx()
        mlx_ptr = self.get_mlx_ptr()

        self.fps = fps
        self.timestamp = time.time()
        self.first = True
        self.animation_finished = False

        mlx.mlx_loop_hook(mlx_ptr, self.__animate_display, None)
        mlx.mlx_loop(mlx_ptr)

    def __animate_display(self, _: None = None) -> None:
        """
        Internal callback used by MLX to update the animated display.

        Parameters
        ----------
        _ : Any
            Unused callback argument provided by the MLX loop.

        Returns
        -------
        None
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

                cell = maze.get_cell(coords)

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
            if self.animation_finished:
                return
            self.animation_finished = True
            self.print_path()
            self.print_entry()
            self.print_exit()
            mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, new_img, 0, 0)

    @staticmethod
    def put_pixel(data: bytearray, x: int, y: int, color: int,
                  bpp: int, size_line: int) -> None:
        """
        Put a colored pixel into the image data buffer.

        Parameters
        ----------
        data : bytearray or memoryview
            Writable image data buffer returned by the MLX library.
        x : int
            X coordinate in pixels.
        y : int
            Y coordinate in pixels.
        color : int
            Color encoded as a 32-bit integer (0xAARRGGBB).
        bpp : int
            Bits per pixel for the image.
        size_line : int
            Number of bytes per image line (stride).

        Notes
        -----
        This writes four bytes (little-endian) starting at the computed
        offset. The function assumes the buffer is large enough for the
        write; an IndexError may be raised if coordinates are out of range.
        """
        offset = y * size_line + x * (bpp // 8)
        data[offset:offset + 4] = color.to_bytes(4, 'little')

    def print_entry(self) -> None:
        """
        Display the maze entry cell.

        Draws the entry cell and its walls using configured colors.

        Returns
        -------
        None
        """
        maze = self.get_maze()
        entry = maze.get_entry()
        entry_color = self.get_entry_color()
        walls_color = self.get_walls_color()

        self.print_cell(entry, entry_color)

        cell: Cell = maze.get_cell(entry)
        walls = cell.get_state_walls(False)
        self.print_walls(entry, walls, entry_color)
        walls = cell.get_state_walls(True)
        self.print_walls(entry, walls, walls_color)
        if self.move_mode:
            self.print_player(self.get_background_color())

    def print_exit(self) -> None:
        """
        Display the maze exit cell.

        Draws the exit cell and its walls using configured colors.

        Returns
        -------
        None
        """
        maze = self.get_maze()
        exit = maze.get_exit()
        exit_color = self.get_exit_color()
        walls_color = self.get_walls_color()

        self.print_cell(exit, exit_color)

        cell: Cell = maze.get_cell(exit)
        walls = cell.get_state_walls(False)
        self.print_walls(exit, walls, exit_color)
        walls = cell.get_state_walls(True)
        self.print_walls(exit, walls, walls_color)
        if self.move_mode:
            self.print_player(self.get_background_color())

    def set_custom_player(self, player_file: TextIO) -> None:
        player_txt: str = player_file.read(-1)
        player_rows: list[str] = player_txt.split("\n")

        for row in player_rows:
            if row == "":
                player_rows.remove(row)

        player_height: int = len(player_rows)
        player_width: int = 0
        if player_height > 0:
            player_width = len(player_rows[0])
            for row in player_rows:
                if len(row) != player_width:
                    player_rows.clear()
                    raise PlayerError(
                        "player line length has to stay the same."
                    )

        if (max(player_height, player_width) > self.get_cell_size()
                and not self.auto_adjust_player):
            raise PlayerError("player too big.")

        player_txt = player_txt.replace("\n", "")

        self.custom_player: list = []

        for y in range(player_height):
            custom_player_row: list = []
            for x in range(player_width):
                char: str = player_txt[y * player_width + x]
                if char not in ["0", " "]:
                    rgb: tuple = self.custom_player_colors.get(char)
                    if rgb is not None:
                        red, green, blue = rgb

                        red = abs(red) % 256
                        green = abs(green) % 256
                        blue = abs(blue) % 256

                        custom_color: int = (
                            (0xFF << 24) | (red << 16) | (green << 8) | blue
                        )
                        custom_player_row.append(custom_color)
                    else:
                        custom_player_row.append(self.get_walls_color())
                else:
                    custom_player_row.append(None)
            self.custom_player.append(custom_player_row)

        if not self.auto_adjust_player:
            return

        cell_size: int = self.get_cell_size()
        expected_x_size: int = math.ceil(cell_size * 0.75)
        expected_y_size: int = math.ceil(cell_size * 0.75)

        src_h = player_height
        src_w = player_width
        tgt_h = expected_y_size
        tgt_w = expected_x_size

        if src_h == 0 or src_w == 0:
            self.custom_player = None
        else:
            resized: list[list] = []
            for ty in range(tgt_h):
                src_y = min(src_h - 1, int(ty * src_h / tgt_h))
                row_list: list = []
                for tx in range(tgt_w):
                    src_x = min(src_w - 1, int(tx * src_w / tgt_w))
                    try:
                        val = self.custom_player[src_y][src_x]
                    except Exception:
                        val = None
                    row_list.append(val)
                resized.append(row_list)

            self.custom_player = resized

    def print_player(self, color: int) -> None:
        x, y = self.player_pos
        size = self.get_cell_size()

        mlx = self.get_mlx()
        new_img = self.get_new_img()
        data, bpb, size_line, endian = mlx.mlx_get_data_addr(new_img)

        if self.custom_player is not None:
            player_offset_x: int = (size - len(self.custom_player)) // 2
            player_offset_y: int = (size - len(self.custom_player[0])) // 2
            for pixel_y, row in enumerate(self.custom_player):
                for pixel_x, custom_color in enumerate(row):
                    if custom_color is not None:
                        Displayer.put_pixel(
                            data,
                            (pixel_x + x * size + self.x_offset
                                + player_offset_x),
                            (pixel_y + y * size + self.y_offset
                                + player_offset_y),
                            custom_color, bpb, size_line
                            )
        else:
            pixel_x = x * size + size // 3
            pixel_y = y * size + size // 3

            for y in range(pixel_y, pixel_y + size // 3):
                for x in range(pixel_x, pixel_x + size // 3):
                    Displayer.put_pixel(
                        data,
                        x + self.x_offset,
                        y + self.y_offset,
                        color, bpb, size_line
                    )

    def print_cell(self, coords: tuple[int, int], color: int) -> None:
        """
        Draw a filled cell at the given coordinates.

        Parameters
        ----------
        coords : tuple[int, int]
            Cell coordinates as (x, y).
        color : int
            Fill color as a 32-bit integer (0xAARRGGBB).

        Returns
        -------
        None
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

    def print_west_east(self, pixel_x_start: int,
                        pixel_y_start: int, walls_color: int) -> None:
        """
        Draw a vertical wall (west or east) for a cell.

        Parameters
        ----------
        pixel_x_start : int
            Starting X position in pixels.
        pixel_y_start : int
            Starting Y position in pixels.
        walls_color : int
            Wall color as a 32-bit integer.

        Returns
        -------
        None
        """
        size = self.get_cell_size()
        new_img = self.get_new_img()
        div = self.get_div()
        mlx = self.get_mlx()
        data, bpb, size_line, endian = mlx.mlx_get_data_addr(new_img)
        for y in range(pixel_y_start, pixel_y_start + size):
            for x in range(pixel_x_start, pixel_x_start + size // div):
                Displayer.put_pixel(data, x, y, walls_color, bpb, size_line)

    def print_north_south(self, pixel_x_start: int,
                          pixel_y_start: int, walls_color: int) -> None:
        """
        Draw a horizontal wall (north or south) for a cell.

        Parameters
        ----------
        pixel_x_start : int
            Starting X position in pixels.
        pixel_y_start : int
            Starting Y position in pixels.
        walls_color : int
            Wall color as a 32-bit integer.

        Returns
        -------
        None
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
                    color: int) -> None:
        """
        Draw all walls for a cell according to the provided directions.

        Parameters
        ----------
        coords : tuple[int, int]
            Cell coordinates as (x, y).
        walls : list[str]
            List of wall directions (e.g. "NORTH", "SOUTH", "WEST", "EST").
        color : int
            Wall color as a 32-bit integer.

        Returns
        -------
        None
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

    def print_path(self) -> None:
        """
        Draw the shortest path in the maze.

        Iterates the stored shortest path and renders each step and its
        adjacent walls.

        Returns
        -------
        None
        """
        if self.toggle_path:
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
            if self.move_mode:
                self.print_player(self.get_background_color())

    def close(self, _: None) -> None:
        """
        Close the MLX window and exit the event loop.

        Parameters
        ----------
        _ : Any
            Unused callback argument from MLX.

        Returns
        -------
        None
        """
        mlx = self.get_mlx()
        mlx_ptr = self.get_mlx_ptr()
        win_ptr = self.get_win_ptr()
        mlx.mlx_destroy_window(mlx_ptr, win_ptr)
        mlx.mlx_loop_exit(mlx_ptr)

    def mouse_event(self, mousecode: int, x: int, y: int, _: None) -> None:
        for button in self.buttons:
            width, height = button.width, button.height
            start_x: int = button.start_x
            start_y: int = button.start_y
            if (start_x <= x and x <= start_x + width):
                if (start_y <= y and y <= start_y + height):
                    button.function(button.param)

    def win_buttons(self) -> None:
        mlx = self.get_mlx()
        mlx_ptr = self.get_mlx_ptr()

        x, y = self.win_buttons_size

        self.win_button_ptr = mlx.mlx_new_window(mlx_ptr, x, y, "Buttons")

        win_ptr = self.win_button_ptr
        mlx.mlx_hook(win_ptr, 33, 1 << 17, self.close, None)
        mlx.mlx_hook(win_ptr, 4, 1 << 2, self.mouse_event, None)
        mlx.mlx_hook(win_ptr, 2, 1 << 0, self.key_press, None)

        self.buttons_img = mlx.mlx_new_image(mlx_ptr, x, y)

    def print_background_button(self, button: Button, data: bytearray,
                                bpb: int, size_line: int) -> None:
        spacing = self.spacing

        pixel_x = self.button_printer_x
        pixel_y = self.button_printer_y

        button.width -= 2 * spacing
        width = button.width
        height = button.height

        button.start_x = pixel_x
        button.start_y = pixel_y

        for x in range(pixel_x, pixel_x + width):
            for y in range(pixel_y, pixel_y + height):
                Displayer.put_pixel(data, x, y,
                                    button.background_color, bpb, size_line)

        self.button_printer_y += height
        self.button_printer_y += spacing

    def print_text_button(self, button: ButtonText) -> None:
        mlx = self.get_mlx()
        mlx_ptr = self.get_mlx_ptr()
        win_ptr = self.win_button_ptr

        width = button.width
        height = button.height
        pixel_x = button.start_x
        pixel_y = button.start_y

        mlx.mlx_string_put(mlx_ptr, win_ptr,
                           pixel_x + (width-len(button.text)*8)//2,
                           pixel_y + (height - 16) // 2,
                           button.text_color, button.text)

    def print_buttons(self) -> None:
        mlx = self.get_mlx()
        img = self.buttons_img
        data, bpb, size_line, _ = mlx.mlx_get_data_addr(img)
        mlx_ptr = self.get_mlx_ptr()

        for button in self.buttons:
            self.print_background_button(button, data, bpb, size_line)

        mlx.mlx_put_image_to_window(mlx_ptr, self.win_button_ptr, img, 0, 0)

        for button in self.buttons:
            if isinstance(button, ButtonText):
                self.print_text_button(button)

    def add_button(self, button: Button) -> None:
        self.buttons.append(button)
