from typing import Callable, Generator
from mazegen.display import Displayer


def theme_purple(displayer: Displayer) -> None:
    """Apply a purple color theme to the maze display.

    Parameters
    ----------
    displayer : Displayer
        The Displayer instance to apply the theme to.

    Returns
    -------
    None
    """
    displayer.set_color("background", (30, 0, 50))
    displayer.set_color("walls", (90, 0, 130))
    displayer.set_color("entry", (180, 0, 255))
    displayer.set_color("exit", (230, 150, 255))
    displayer.set_color("path", (140, 70, 200))
    displayer.set_color("icon", (255, 220, 255))


def theme_blue(displayer: Displayer) -> None:
    """Apply a blue color theme to the maze display.

    Parameters
    ----------
    displayer : Displayer
        The Displayer instance to apply the theme to.

    Returns
    -------
    None
    """
    displayer.set_color("background", (5, 10, 40))
    displayer.set_color("walls", (0, 40, 120))
    displayer.set_color("entry", (0, 120, 255))
    displayer.set_color("exit", (120, 200, 255))
    displayer.set_color("path", (0, 80, 180))
    displayer.set_color("icon", (200, 230, 255))


def theme_yellow(displayer: Displayer) -> None:
    """Apply a yellow color theme to the maze display.

    Parameters
    ----------
    displayer : Displayer
        The Displayer instance to apply the theme to.

    Returns
    -------
    None
    """
    displayer.set_color("background", (40, 30, 0))
    displayer.set_color("walls", (120, 90, 0))
    displayer.set_color("entry", (255, 200, 0))
    displayer.set_color("exit", (255, 240, 120))
    displayer.set_color("path", (200, 160, 0))
    displayer.set_color("icon", (255, 255, 200))


def theme_green(displayer: Displayer) -> None:
    """Apply a green color theme to the maze display.

    Parameters
    ----------
    displayer : Displayer
        The Displayer instance to apply the theme to.

    Returns
    -------
    None
    """
    displayer.set_color("background", (0, 30, 10))
    displayer.set_color("walls", (0, 80, 30))
    displayer.set_color("entry", (0, 200, 80))
    displayer.set_color("exit", (120, 255, 180))
    displayer.set_color("path", (0, 140, 60))
    displayer.set_color("icon", (200, 255, 220))


def theme_orange(displayer: Displayer) -> None:
    """Apply an orange color theme to the maze display.

    Parameters
    ----------
    displayer : Displayer
        The Displayer instance to apply the theme to.

    Returns
    -------
    None
    """
    displayer.set_color("background", (50, 20, 0))
    displayer.set_color("walls", (120, 50, 0))
    displayer.set_color("entry", (255, 120, 0))
    displayer.set_color("exit", (255, 200, 120))
    displayer.set_color("path", (200, 90, 0))
    displayer.set_color("icon", (255, 230, 200))


def theme_red(displayer: Displayer) -> None:
    """Apply a red color theme to the maze display.

    Parameters
    ----------
    displayer : Displayer
        The Displayer instance to apply the theme to.

    Returns
    -------
    None
    """
    displayer.set_color("background", (40, 0, 0))
    displayer.set_color("walls", (120, 0, 0))
    displayer.set_color("entry", (220, 0, 0))
    displayer.set_color("exit", (255, 120, 120))
    displayer.set_color("path", (180, 30, 30))
    displayer.set_color("icon", (255, 200, 200))


def theme_pink(displayer: Displayer) -> None:
    """Apply a pink color theme to the maze display.

    Parameters
    ----------
    displayer : Displayer
        The Displayer instance to apply the theme to.

    Returns
    -------
    None
    """
    displayer.set_color("background", (40, 0, 30))
    displayer.set_color("walls", (120, 20, 90))
    displayer.set_color("entry", (255, 0, 150))
    displayer.set_color("exit", (255, 150, 220))
    displayer.set_color("path", (200, 60, 140))
    displayer.set_color("icon", (255, 220, 240))


def theme_multicolor(displayer: Displayer) -> None:
    """Apply a multicolor theme to the maze display.

    Parameters
    ----------
    displayer : Displayer
        The Displayer instance to apply the theme to.

    Returns
    -------
    None
    """
    displayer.set_color("background", (20, 20, 20))
    displayer.set_color("walls", (0, 120, 255))
    displayer.set_color("entry", (0, 200, 0))
    displayer.set_color("exit", (255, 0, 0))
    displayer.set_color("path", (255, 200, 0))
    displayer.set_color("icon", (200, 0, 255))


def change_theme(displayer: Displayer) -> Generator[None, None, None]:
    """Cycle through color themes each time it is called.

    Creates a generator that cycles through all available color themes
    and applies them to the displayer when the generator is advanced.

    Parameters
    ----------
    displayer : Displayer
        The Displayer instance to apply themes to.

    Yields
    ------
    None
        On each iteration, applies the next theme and refreshes the display.
    """
    themes: list[Callable] = [theme_purple,
                              theme_blue,
                              theme_yellow,
                              theme_green,
                              theme_orange,
                              theme_red,
                              theme_pink,
                              theme_multicolor
                              ]
    i: int = 0
    len_themes: int = len(themes)

    while True:
        themes[i % len_themes](displayer)
        displayer.display(False)
        i += 1
        yield None
