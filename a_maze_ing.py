from src.config_parser import Config
from src.maze_generation.maze import Maze
from src.display.display import Displayer

config = Config()

config.add_parameter("WIDTH", [None, [int]])
config.add_parameter("HEIGHT", [None, [int]])
config.add_parameter("ENTRY", [None, [tuple, 2, [[int], [int]], ","]])
config.add_parameter("EXIT", [None, [tuple, 2, [[int], [int]], ","]])
config.add_parameter("OUTPUT_FILE", [None, [str]])
config.add_parameter("PERFECT", [None, [bool]])
config.add_parameter("SEED", [0, [int]])
config.add_parameter("ICON_FILE", [None, [str]])
config.add_parameter("MAZE_SIZE", [((0, 0), (0, 0)), [
    tuple, 2, [
        [tuple, 2, [[int], [int]], ","], [tuple, 2, [[int], [int]], ","]
        ], " "
    ]])

config_file = open("config.txt")

config.parse_file(config_file)

config_file.close()

width = config.get_value("WIDTH")
height = config.get_value("HEIGHT")
seed = config.get_value("SEED")

entry = config.get_value("ENTRY")
exit = config.get_value("EXIT")

perfect = config.get_value("PERFECT")

output_file = config.get_value("OUTPUT_FILE")
icon_file = config.get_value("ICON_FILE")

file = open(output_file, "w")

icon_file = open(icon_file, "r")

maze = Maze(width, height, entry, exit, perfect, seed, icon_file)
maze.create_full_maze()

maze.output_in_file(file)

screen_size, maze_size = config.get_value("MAZE_SIZE")

# probleme dans display quand screen size == 0

displayer = Displayer(screen_size, maze_size, maze, 5)

displayer.start_animated_display(60)
