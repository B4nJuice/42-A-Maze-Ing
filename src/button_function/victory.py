from mazegen.display import Displayer


class ImageError(Exception):
    """Exception raised when image loading fails."""
    pass


def close(param: tuple) -> None:
    """Close the MLX window.

    Parameters
    ----------
    param : tuple
        A tuple containing (mlx, mlx_ptr, win_ptr).

    Returns
    -------
    None
    """
    mlx, mlx_ptr, win_ptr = param
    mlx.mlx_destroy_window(mlx_ptr, win_ptr)


def key_press(keycode: int, param: tuple) -> None:
    """Handle key press events in the victory window.

    Closes the window when the ESC key is pressed.

    Parameters
    ----------
    keycode : int
        The key code of the pressed key.
    param : tuple
        A tuple containing (mlx, mlx_ptr, win_ptr).

    Returns
    -------
    None
    """
    mlx, mlx_ptr, win_ptr = param
    if keycode == 65307:
        mlx.mlx_destroy_window(mlx_ptr, win_ptr)


def victory_function(param: tuple[Displayer, tuple]) -> None:
    """Display a victory screen if the player reaches the exit.

    Creates and displays a victory image window when the player position
    equals the maze exit position.

    Parameters
    ----------
    param : tuple
        A tuple containing:
        - displayer : Displayer - The maze displayer instance.
        - exit : tuple - The exit coordinates (x, y).

    Raises
    ------
    ImageError
        If the victory image file cannot be loaded.

    Returns
    -------
    None
    """
    displayer, exit = param
    path = "src/assets/you_win.xpm"
    if displayer.player_pos == exit:
        mlx = displayer.get_mlx()
        mlx_ptr = displayer.get_mlx_ptr()

        img = mlx.mlx_xpm_file_to_image(mlx_ptr, path)
        img_ptr, x, y = img
        win_ptr = mlx.mlx_new_window(mlx_ptr, x, y, "Victory !")

        if img == (None, 0, 0):
            close((mlx, mlx_ptr, win_ptr))
            raise ImageError("loading image failed.")
        mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)
        mlx.mlx_hook(win_ptr, 33, 1 << 17, close, (mlx, mlx_ptr, win_ptr))
        mlx.mlx_hook(win_ptr, 2, 1 << 0, key_press, (mlx, mlx_ptr, win_ptr))
