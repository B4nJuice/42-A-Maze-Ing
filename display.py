from mlx import Mlx


def close(args):
    mlx, mlx_ptr, win_ptr = args
    mlx.mlx_destroy_window(mlx_ptr, win_ptr)
    mlx.mlx_loop_exit(mlx_ptr)
    return 0


def put_pixel(data, x, y, color, bpp, size_line):
    offset = y * size_line + x * (bpp // 8)
    data[offset:offset + 4] = color.to_bytes(4, 'little')


def get_size_square(width, height) -> int:
    size = 1000 / window_size_x


window_size_x = 1000
window_size_y = 1000
mlx = Mlx()
mlx_ptr = mlx.mlx_init()
win_ptr = mlx.mlx_new_window(mlx_ptr, window_size_x, window_size_y, "A-Maze-ing")
mlx.mlx_hook(win_ptr, 33, 1 << 17, close, (mlx, mlx_ptr, win_ptr))
new_img = mlx.mlx_new_image(mlx_ptr, 900, 1000)
data, bpp, size_line, endian = mlx.mlx_get_data_addr(new_img)

for x in range(window_size_x):
    for y in range(window_size_y):
        put_pixel(data, window_size_x, window_size_y, 0xFFFFFFFF, bpp, size_line)

mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, new_img, 0, 0)
mlx.mlx_loop(mlx_ptr)
