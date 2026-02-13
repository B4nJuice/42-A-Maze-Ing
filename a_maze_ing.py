#! .venv/bin/python3

from src.config import Config
from src.maze_generation import Maze
from src.display import Displayer
from src.display import Button
from src.display.button import ButtonText
from src.theme import change_theme
import sys


def create_config(config: Config) -> None:
    config.add_parameter("WIDTH", [20, [int]])
    config.add_parameter("HEIGHT", [15, [int]])
    config.add_parameter("ENTRY", [(0, 0), [tuple, 2, [[int], [int]], ","]])
    config.add_parameter("EXIT", [(19, 14), [tuple, 2, [[int], [int]], ","]])
    config.add_parameter("OUTPUT_FILE", ["maze.txt", [str]])
    config.add_parameter("PERFECT", [True, [bool]])
    config.add_parameter("SEED", [42, [int]])
    config.add_parameter("ICON_FILE", ["src/default_icon.txt", [str]])
    config.add_parameter("TOGGLE_PATH", [False, [bool]])
    config.add_parameter("MAZE_SIZE", [((0, 0), (0, 0)), [
        tuple, 2, [
            [tuple, 2, [[int], [int]], ","], [tuple, 2, [[int], [int]], ","]
            ], " "
        ]])
    config.add_parameter("WALL_THICKNESS", [5, [int]])

    config.add_parameter("CUSTOM_COLORS", [False, [bool]])
    config.add_parameter("BACKGROUND_COLOR", [
            (255, 255, 255), [tuple, 3, [[int], [int], [int]], ","]
        ])
    config.add_parameter("WALLS_COLOR", [
            (0, 0, 0), [tuple, 3, [[int], [int], [int]], ","]
        ])
    config.add_parameter("ICON_COLOR", [
            (0, 0, 0), [tuple, 3, [[int], [int], [int]], ","]
        ])
    config.add_parameter("ENTRY_COLOR", [
            (0, 255, 0), [tuple, 3, [[int], [int], [int]], ","]
        ])
    config.add_parameter("EXIT_COLOR", [
            (255, 0, 0), [tuple, 3, [[int], [int], [int]], ","]
        ])
    config.add_parameter("PATH_COLOR", [
            (0, 0, 255), [tuple, 3, [[int], [int], [int]], ","]
        ])

    config.add_parameter("ANIMATED", [False, [bool]])
    config.add_parameter("FPS", [60, [int]])
    config.add_parameter("SPACING", [42, [int]])

    config.add_parameter("CUSTOM_PLAYER_FILE", ["", [str]])
    config.add_parameter("AUTO_ADJUST_PLAYER", [True, [bool]])
    config.add_parameter("CUSTOM_PLAYER_COLORS", [{"r": (255, 0, 0)}, [
        dict, [
            [tuple, 2, [[str], [tuple, 3, [[int], [int], [int]], ","]], ":"],
            [tuple, 2, [[str], [tuple, 3, [[int], [int], [int]], ","]], ":"],
            [tuple, 2, [[str], [tuple, 3, [[int], [int], [int]], ","]], ":"],
            [tuple, 2, [[str], [tuple, 3, [[int], [int], [int]], ","]], ":"],
            ], " "
        ]])


if __name__ == "__main__":
    argv: list[str] = sys.argv
    argc: int = len(argv)

    config_file_name: str = ""

    if argc >= 2:
        config_file_name = argv[1]

    config: Config = Config()

    try:
      create_config(config)

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

      if config.get_value("CUSTOM_COLORS"):
          displayer.set_color("background", config.get_value(
              "BACKGROUND_COLOR"))
          displayer.set_color("walls", config.get_value("WALLS_COLOR"))
          displayer.set_color("icon", config.get_value("ICON_COLOR"))
          displayer.set_color("entry", config.get_value("ENTRY_COLOR"))
          displayer.set_color("exit", config.get_value("EXIT_COLOR"))
          displayer.set_color("path", config.get_value("PATH_COLOR"))

      x, _ = displayer.win_buttons_size
      y = displayer.get_cell_size()
      # button1 = Button(test, None, (x, y))
      button2 = ButtonText(next, change_theme(displayer), (x, y), (255, 255, 255), "THEME")
      # displayer.add_button(button1)
      displayer.add_button(button2)
      displayer.set_spacing(config.get_value("SPACING"))
      displayer.print_buttons()

      player_file: str = config.get_value("CUSTOM_PLAYER_FILE")

      if player_file != "":
          with open(player_file, "r") as textio_player_file:
              displayer.set_auto_adjust_player(
                      config.get_value("AUTO_ADJUST_PLAYER")
                  )
              displayer.set_custom_player_colors(
                  config.get_value("CUSTOM_PLAYER_COLORS")
              )
              displayer.set_custom_player(textio_player_file)

      if config.get_value("TOGGLE_PATH"):
          displayer.set_toggle_path(True)

      if config.get_value("ANIMATED"):
          displayer.start_animated_display(config.get_value("FPS"))
      else:
          displayer.display()
    except Exception as e:
        print(e)