from typing import Callable
from typing import Any


class Button:
    def __init__(self, function: callable, param: Any,
                 start_x: int, start_y: int,
                 width: int, height: int, color: int) -> None:
        self.function = function
        self.param = param
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.color = color

    def clic(self) -> None:
        self.function(self.param)