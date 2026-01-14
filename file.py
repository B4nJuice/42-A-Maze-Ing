from mlx import Mlx


def close(args):
    mlx, mlx_ptr, win_ptr = args
    mlx.mlx_destroy_window(mlx_ptr, win_ptr)
    mlx.mlx_loop_exit(mlx_ptr)


def put_pixel(data, x, y, color, bpp, size_line):
    offset = y * size_line + x * (bpp // 8)

mlx = Mlx()
mlx_ptr = mlx.mlx_init()
win_ptr = mlx.mlx_new_window(mlx_ptr, 1000, 1000, "Hello World")
mlx.mlx_hook(win_ptr, 33, 1 << 17, close, (mlx, mlx_ptr, win_ptr))
img = mlx.mlx_new_image(mlx_ptr, 920, 1000)
data, bpp, size_line, endian = mlx.mlx_get_data_addr(img)
mlx.put_pixel()
mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, img, 0, 0)
mlx.mlx_loop(mlx_ptr)
