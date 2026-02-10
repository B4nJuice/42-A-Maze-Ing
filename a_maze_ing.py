from src.config_parser import Config
from src.maze_generation.maze import Maze
from src.display.display import Displayer
import sys

if __name__ == "__main__":
    argv: list[str] = sys.argv
    argc: int = len(argv)

    config_file_name: str = ""

    if argc >= 2:
        config_file_name = argv[1]

    config: Config = Config()

    config.add_parameter("WIDTH", [20, [int]])
    config.add_parameter("HEIGHT", [15, [int]])
    config.add_parameter("ENTRY", [(0, 0), [tuple, 2, [[int], [int]], ","]])
    config.add_parameter("EXIT", [(19, 14), [tuple, 2, [[int], [int]], ","]])
    config.add_parameter("OUTPUT_FILE", ["maze.txt", [str]])
    config.add_parameter("PERFECT", [True, [bool]])
    config.add_parameter("SEED", [42, [int]])
    config.add_parameter("ICON_FILE", ["src/default_icon.txt", [str]])
    config.add_parameter("MAZE_SIZE", [((0, 0), (0, 0)), [
        tuple, 2, [
            [tuple, 2, [[int], [int]], ","], [tuple, 2, [[int], [int]], ","]
            ], " "
        ]])
    config.add_parameter("WALL_THICKNESS", [10, [int]])

    if config_file_name != "":
        with open(config_file_name) as config_file:
            config.parse_file(config_file)

    width: int = config.get_value("WIDTH")
    height: int = config.get_value("HEIGHT")
    seed: int = config.get_value("SEED")

    entry: tuple[int, int] = config.get_value("ENTRY")
    _exit: tuple[int, int] = config.get_value("EXIT")

    perfect: bool = config.get_value("PERFECT")

    output_file_name: str = config.get_value("OUTPUT_FILE")
    icon_file_name: str = config.get_value("ICON_FILE")

    with open(output_file_name, "w") as output_file:
        with open(icon_file_name, "r") as icon_file:
            maze: Maze = Maze(
                            width,
                            height,
                            entry,
                            _exit,
                            perfect,
                            seed,
                            icon_file
                        )

            maze.create_full_maze()
        maze.output_in_file(output_file)

    screen_size, maze_size = config.get_value("MAZE_SIZE")
    wall_thickness: int = config.get_value("WALL_THICKNESS")

    displayer: Displayer = Displayer(
                                screen_size,
                                maze_size,
                                maze,
                                wall_thickness
                            )

    displayer.set_color("background", 255, 255, 255)
    displayer.set_color("walls", 0, 0, 0)
    displayer.set_color("icon", 0, 0, 0)

    displayer.start_animated_display(60)
