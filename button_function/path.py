from src.display import Displayer


def change_path(displayer: Displayer) -> None:
    displayer.set_toggle_path(not displayer.toggle_path)
    displayer.display(False)
