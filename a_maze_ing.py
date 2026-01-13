# !/usr/bin/env python3

from src.config_parser import Config
from src.maze_generation.maze import Maze

config = Config("config.txt")

widht = config.get_value("WIDHT")
height = config.get_value("HEIGHT")
seed = config.get_value("SEED")

entry = config.get_value("ENTRY")
exit = config.get_value("EXIT")

maze = Maze(widht, height, entry, exit, seed)

output_file = config.get_value("OUTPUT_FILE")

file = open(output_file, "w")

maze.create_path(entry)

maze.output_in_file(file)
