from src.config_parser import Config
from src.maze_generation.maze import Maze
from src.display.display import Displayer

config = Config("config.txt")

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

displayer = Displayer((3000, 2000), (2000, 2000), maze, 2.5)

displayer.start_animated_display(60)
