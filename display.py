from mlx import Mlx
from src.maze_generation.maze import Maze
from src.maze_generation.cell import Cell


def close(args):
    mlx, mlx_ptr, win_ptr = args
    mlx.mlx_destroy_window(mlx_ptr, win_ptr)
    mlx.mlx_loop_exit(mlx_ptr)
    return 0


def put_pixel(data, x, y, color, bpp, size_line):
    offset = y * size_line + x * (bpp // 8)
    data[offset:offset + 4] = color.to_bytes(4, 'little')


def get_size_square(width, height):
    if width >= height:
        size = image_size_x // width
    elif width < height:
        size = image_size_x // height
    return size


def print_west_east(pixel_x_start, pixel_y_start, size):
    for y in range(pixel_y_start, pixel_y_start + size):
        for x in range(pixel_x_start, pixel_x_start + size//4):
            put_pixel(data, x, y, 0xFFFF0000, bpp, size_line)


def print_north_south(pixel_x_start, pixel_y_start, size):
    for y in range(pixel_y_start, pixel_y_start + size//4):
        for x in range(pixel_x_start, pixel_x_start + size):
            put_pixel(data, x, y, 0xFFFF0000, bpp, size_line)


def print_cell(x, y, size, north, south, east, west):
    pixel_x_start = x * size
    pixel_y_start = y * size
    for y in range(pixel_y_start, pixel_y_start + size):
        for x in range(pixel_x_start, pixel_x_start + size):
            put_pixel(data, x, y, 0xFFFFFFFF, bpp, size_line)
    if west is not None:
        print_west_east(pixel_x_start, pixel_y_start, size)
    if east is not None:
        print_west_east(pixel_x_start + size * 3 // 4, pixel_y_start, size)
    if north is not None:
        print_north_south(pixel_x_start, pixel_y_start, size)
    if south is not None:
        print_north_south(pixel_x_start, pixel_y_start + size * 3 // 4, size)

def coordonates_cells(maze: Maze):
    matrix = maze.get_matrix()
    


image_size_x: int = 900
image_size_y: int = 900
width = 20
height = 25
x = 15
y = 10
size = get_size_square(width, height)
mlx = Mlx()
mlx_ptr = mlx.mlx_init()
win_ptr = mlx.mlx_new_window(mlx_ptr, 1000, 1000, "A-Maze-ing")
mlx.mlx_hook(win_ptr, 33, 1 << 17, close, (mlx, mlx_ptr, win_ptr))
new_img = mlx.mlx_new_image(mlx_ptr, 900, 900)
data, bpp, size_line, endian = mlx.mlx_get_data_addr(new_img)

print_cell(x, y, size, None, None, None, None)
mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, new_img, 0, 0)
mlx.mlx_loop(mlx_ptr)
