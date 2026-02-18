from mazegen.display import Displayer


def print_seed(displayer: Displayer) -> None:
    """Print the seed of the current maze to standard output.

    Parameters
    ----------
    displayer : Displayer
        The Displayer instance containing the maze.

    Returns
    -------
    None
    """
    print(displayer.get_maze().get_seed())
