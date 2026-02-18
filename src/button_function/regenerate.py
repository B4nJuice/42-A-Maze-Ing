from mazegen.display import Displayer
from mazegen.maze_generation import Maze


def regenerate_maze(param: tuple[
            Displayer, bool, int, int, tuple,
            tuple, bool, str, str]) -> None:
    """Generate a new maze and display it.

    Creates a completely new maze with the given parameters, saves it to
    a file, updates the displayer, and displays it either with animation
    or static rendering.

    Parameters
    ----------
    param : tuple
        A tuple containing:
        - displayer : Displayer - The display instance to update.
        - animated : bool - Whether to animate maze generation.
        - w : int - Maze width in cells.
        - h : int - Maze height in cells.
        - ent : tuple - Entry coordinates as (x, y).
        - ex : tuple - Exit coordinates as (x, y).
        - perf : bool - Whether the maze should be perfect.
        - icon_name : str - Path to the icon file.
        - output_name : str - Path where the maze should be saved.

    Returns
    -------
    None
    """
    displayer, animated, w, h, ent, ex, perf, icon_name, output_name = param
    with open(output_name, "w") as output:
        with open(icon_name, "r") as icon:
            new_maze: Maze = Maze(w, h, ent, ex, perf, 0, icon)
            new_maze.create_full_maze()
            new_maze.output_in_file(output)

    displayer.set_maze(new_maze)
    if animated is True:
        displayer.clear(0xFF000000)
        displayer.start_animated_display(60)
    else:
        displayer.display(False)
