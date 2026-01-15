from mlx import Mlx


def close(args):
    mlx, mlx_ptr, win_ptr = args
    mlx.mlx_destroy_window(mlx_ptr, win_ptr)
    mlx.mlx_loop_exit(mlx_ptr)
    return 0


def put_pixel(data, x, y, color, bpp, size_line):
    offset = y * size_line + x * (bpp // 8)
    data[offset:offset + 4] = color.to_bytes(4, 'little')


def put_cell(x, y, X, Y, wall):


mlx = Mlx()
mlx_ptr = mlx.mlx_init()
win_ptr = mlx.mlx_new_window(mlx_ptr, 1500, 1000, "A-Maze-ing")
mlx.mlx_hook(win_ptr, 33, 1 << 17, close, (mlx, mlx_ptr, win_ptr))
new_img = mlx.mlx_new_image(mlx_ptr, 900, 1000)
data, bpp, size_line, endian = mlx.mlx_get_data_addr(new_img)

put_pixel(data, 500, 500, 0xFFFFFFFF, bpp, size_line)

mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, new_img, 0, 0)
mlx.mlx_loop(mlx_ptr)
