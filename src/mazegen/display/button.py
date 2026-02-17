from typing import Callable
from typing import Any


class ButtonError(Exception):
    def __init__(self, message: str = "undefined"):
        super().__init__(f"SpacingError: {message}")


class Button:
    def __init__(self, function: Callable, param: Any, size: tuple[int, int],
                 background_color: tuple = (255, 255, 255)) -> None:
        self.function = function
        self.param = param
        self.set_size(size)
        self.background_color: int = self.rgb_to_argb(background_color)
        self.start_x: int = 0
        self.start_y: int = 0

    def set_size(self, size: tuple[int, int]) -> None:
        width, height = size
        if width < 0 or height < 0:
            raise ButtonError("Button size must be greater than 0.")
        if not isinstance(width, int) or not isinstance(height, int):
            raise ButtonError("Button size must be int type.")
        self.height: int = height
        self.width: int = width

    @staticmethod
    def rgb_to_argb(rgb: tuple) -> int:
        red, green, blue = rgb

        red = abs(red) % 256
        green = abs(green) % 256
        blue = abs(blue) % 256

        color: int = (0xFF << 24) | (red << 16) | (green << 8) | blue
        return color


class ButtonText(Button):
    def __init__(self, function: Callable, param: Any, size: tuple[int, int],
                 background_color: tuple,
                 text: str = "No text") -> None:
        self.text_color = self.text_color_contrast(background_color)
        self.text = text
        super().__init__(function, param, size, background_color)

    @staticmethod
    def text_color_contrast(background_color: tuple[int, int, int]) -> int:
        r, g, b = background_color

        brightness = 0.299*r + 0.587*g + 0.114*b

        if brightness > 128:
            return (ButtonText.rgb_to_rgb24((0, 0, 0)))
        else:
            return (ButtonText.rgb_to_rgb24((255, 255, 255)))

    @staticmethod
    def rgb_to_rgb24(rgb: tuple) -> int:
        red, green, blue = rgb

        red = abs(red) % 256
        green = abs(green) % 256
        blue = abs(blue) % 256

        color: int = (blue << 16) | (green << 8) | red
        return color
