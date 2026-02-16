from typing import Callable, Generator
from src.display import Displayer


def theme_purple(displayer: Displayer) -> None:
    displayer.set_color("background", (30, 0, 50))      # violet très sombre
    displayer.set_color("walls", (90, 0, 130))          # violet foncé
    displayer.set_color("entry", (180, 0, 255))         # violet vif
    displayer.set_color("exit", (230, 150, 255))        # violet clair
    displayer.set_color("path", (140, 70, 200))         # violet moyen
    displayer.set_color("icon", (255, 220, 255))        # presque blanc rosé


def theme_blue(displayer: Displayer) -> None:
    displayer.set_color("background", (5, 10, 40))      # bleu nuit
    displayer.set_color("walls", (0, 40, 120))          # bleu profond
    displayer.set_color("entry", (0, 120, 255))         # bleu vif
    displayer.set_color("exit", (120, 200, 255))        # bleu clair
    displayer.set_color("path", (0, 80, 180))           # bleu moyen
    displayer.set_color("icon", (200, 230, 255))        # bleu très clair


def theme_yellow(displayer: Displayer) -> None:
    displayer.set_color("background", (40, 30, 0))      # brun très sombre
    displayer.set_color("walls", (120, 90, 0))          # ocre
    displayer.set_color("entry", (255, 200, 0))         # jaune vif
    displayer.set_color("exit", (255, 240, 120))        # jaune pâle
    displayer.set_color("path", (200, 160, 0))          # jaune foncé
    displayer.set_color("icon", (255, 255, 200))        # crème clair


def theme_green(displayer: Displayer) -> None:
    displayer.set_color("background", (0, 30, 10))      # vert très sombre
    displayer.set_color("walls", (0, 80, 30))           # vert foncé
    displayer.set_color("entry", (0, 200, 80))          # vert vif
    displayer.set_color("exit", (120, 255, 180))        # vert clair
    displayer.set_color("path", (0, 140, 60))           # vert moyen
    displayer.set_color("icon", (200, 255, 220))        # vert très pâle


def theme_orange(displayer: Displayer) -> None:
    displayer.set_color("background", (50, 20, 0))      # brun sombre
    displayer.set_color("walls", (120, 50, 0))          # brun orangé
    displayer.set_color("entry", (255, 120, 0))         # orange vif
    displayer.set_color("exit", (255, 200, 120))        # orange clair
    displayer.set_color("path", (200, 90, 0))           # orange foncé
    displayer.set_color("icon", (255, 230, 200))        # pêche clair


def theme_red(displayer: Displayer) -> None:
    displayer.set_color("background", (40, 0, 0))       # rouge très sombre
    displayer.set_color("walls", (120, 0, 0))           # rouge foncé
    displayer.set_color("entry", (220, 0, 0))           # rouge vif
    displayer.set_color("exit", (255, 120, 120))        # rouge clair
    displayer.set_color("path", (180, 30, 30))          # rouge moyen
    displayer.set_color("icon", (255, 200, 200))        # rose très pâle


def theme_pink(displayer: Displayer) -> None:
    displayer.set_color("background", (40, 0, 30))      # prune sombre
    displayer.set_color("walls", (120, 20, 90))         # rose foncé
    displayer.set_color("entry", (255, 0, 150))         # rose vif
    displayer.set_color("exit", (255, 150, 220))        # rose clair
    displayer.set_color("path", (200, 60, 140))         # rose moyen
    displayer.set_color("icon", (255, 220, 240))        # rose très pâle


def theme_multicolor(displayer: Displayer) -> None:
    displayer.set_color("background", (20, 20, 20))     # gris sombre neutre
    displayer.set_color("walls", (0, 120, 255))         # bleu
    displayer.set_color("entry", (0, 200, 0))           # vert
    displayer.set_color("exit", (255, 0, 0))            # rouge
    displayer.set_color("path", (255, 200, 0))          # jaune
    displayer.set_color("icon", (200, 0, 255))          # violet


def change_theme(displayer: Displayer) -> Generator[None, None, None]:
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
