from src.display import Displayer


def print_seed(displayer: Displayer) -> None:
    print(displayer.get_maze().get_seed())
