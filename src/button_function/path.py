from mazegen.display import Displayer


def change_path(displayer: Displayer) -> None:
    """Toggle the display of the shortest path.

    Toggles the path display state and refreshes the maze display
    to show or hide the shortest path visualization.

    Parameters
    ----------
    displayer : Displayer
        The Displayer instance to toggle the path on.

    Returns
    -------
    None
    """
    displayer.set_toggle_path(not displayer.toggle_path)
    displayer.display(False)
