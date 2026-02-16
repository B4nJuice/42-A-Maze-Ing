from src.display import Displayer
from src.maze_generation import Maze


def regenerate_maze(param: tuple[
            Displayer, bool, int, int, tuple,
            tuple, bool, str, str]) -> None:
    displayer, animated, w, h, ent, ex, perf, icon_name, output_name = param
    with open(output_name, "w") as output:
        with open(icon_name, "r") as icon:
            new_maze: Maze = Maze(w, h, ent, ex, perf, 0, icon)
            new_maze.create_full_maze()
            new_maze.output_in_file(output)

    displayer.set_maze(new_maze)
    if animated is True:
        displayer.start_animated_display(60)
    else:
        displayer.display(False)
