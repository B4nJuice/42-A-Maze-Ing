from typing import Callable
from typing import Any


class Button:
    def __init__(self, function: Callable, param: Any,
                 width: int, height: int) -> None:
        self.function = function
        self.param = param
        self.height = height
        self.width = width
        self.start_x: int = 0
        self.start_y: int = 0
