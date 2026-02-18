from typing import Callable
from typing import Any


class ButtonError(Exception):
    """Exception raised for button-related errors.

    Parameters
    ----------
    message : str, optional
        The error message (default is "undefined").
    """
    def __init__(self, message: str = "undefined"):
        super().__init__(f"SpacingError: {message}")


class Button:
    """A clickable button for the display window.

    Represents a button with a position, size, and background color that can
    trigger a function when clicked.

    Attributes
    ----------
    function : Callable
        The function to call when the button is clicked.
    param : Any
        Parameters to pass to the function.
    width : int
        Button width in pixels.
    height : int
        Button height in pixels.
    background_color : int
        Button background color as a 32-bit integer (0xAARRGGBB).
    start_x : int
        X position of the button in pixels.
    start_y : int
        Y position of the button in pixels.
    """
    def __init__(self, function: Callable[[Any], Any],
                 param: Any, size: tuple[int, int],
                 background_color: tuple[int, int, int] = (255, 255, 255)
                 ) -> None:
        """Initialize a Button.

        Parameters
        ----------
        function : Callable
            The function to call when the button is clicked.
        param : Any
            Parameters to pass to the function.
        size : tuple[int, int]
            Button size as (width, height) in pixels.
        background_color : tuple, optional
            RGB color tuple (0-255) for button background (default: white).

        Raises
        ------
        ButtonError
            If size values are negative or not integers.
        """
        self.function = function
        self.param = param
        self.set_size(size)
        self.background_color: int = self.rgb_to_argb(background_color)
        self.start_x: int = 0
        self.start_y: int = 0

    def set_size(self, size: tuple[int, int]) -> None:
        """Set the button size.

        Parameters
        ----------
        size : tuple[int, int]
            Button size as (width, height) in pixels.

        Raises
        ------
        ButtonError
            If width or height is negative or not an integer.

        Returns
        -------
        None
        """
        width, height = size
        if width < 0 or height < 0:
            raise ButtonError("Button size must be greater than 0.")
        if not isinstance(width, int) or not isinstance(height, int):
            raise ButtonError("Button size must be int type.")
        self.height: int = height
        self.width: int = width

    @staticmethod
    def rgb_to_argb(rgb: tuple[int, int, int]) -> int:
        """Convert RGB color tuple to ARGB 32-bit integer.

        Parameters
        ----------
        rgb : tuple
            RGB color tuple with values (0-255 each).

        Returns
        -------
        int
            Color as a 32-bit integer in ARGB format (0xAARRGGBB) with
            alpha channel set to full opacity (0xFF).
        """
        red, green, blue = rgb

        red = abs(red) % 256
        green = abs(green) % 256
        blue = abs(blue) % 256

        color: int = (0xFF << 24) | (red << 16) | (green << 8) | blue
        return color


class ButtonText(Button):
    """A button with a text label.

    Extends Button to display text on the button.
    The text color is automatically calculated to provide
    contrast with the background color.

    Attributes
    ----------
    text : str
        The text to display on the button.
    text_color : int
        Text color as a 24-bit integer (0xRRGGBB).
    """
    def __init__(self, function: Callable[[Any], Any],
                 param: Any, size: tuple[int, int],
                 background_color: tuple[int, int, int],
                 text: str = "No text") -> None:
        """Initialize a ButtonText.

        Parameters
        ----------
        function : Callable
            The function to call when the button is clicked.
        param : Any
            Parameters to pass to the function.
        size : tuple[int, int]
            Button size as (width, height) in pixels.
        background_color : tuple
            RGB color tuple (0-255 each) for button background.
        text : str, optional
            The text to display on the button (default is "No text").

        Raises
        ------
        ButtonError
            If size values are negative or not integers.
        """
        self.text_color = self.text_color_contrast(background_color)
        self.text = text
        super().__init__(function, param, size, background_color)

    @staticmethod
    def text_color_contrast(background_color: tuple[int, int, int]) -> int:
        """Calculate a contrasting text color for the given background color.

        Uses the relative luminance formula to determine if the background is
        light or dark, and returns black for light backgrounds or white for
        dark backgrounds to ensure readable text.

        Parameters
        ----------
        background_color : tuple[int, int, int]
            RGB color tuple (0-255 each) for the background.

        Returns
        -------
        int
            Text color as a 24-bit integer (0xRRGGBB) - either black (0x000000)
            or white (0xFFFFFF).
        """
        r, g, b = background_color

        brightness = 0.299*r + 0.587*g + 0.114*b

        if brightness > 128:
            return (ButtonText.rgb_to_rgb24((0, 0, 0)))
        else:
            return (ButtonText.rgb_to_rgb24((255, 255, 255)))

    @staticmethod
    def rgb_to_rgb24(rgb: tuple[int, int, int]) -> int:
        """Convert RGB color tuple to RGB 24-bit integer.

        Converts an RGB color tuple to a 24-bit integer representation in
        BGR format (as required by the MLX library).

        Parameters
        ----------
        rgb : tuple
            RGB color tuple with values (0-255 each).

        Returns
        -------
        int
            Color as a 24-bit integer in BGR format (0xBBGGRR).
        """
        red, green, blue = rgb

        red = abs(red) % 256
        green = abs(green) % 256
        blue = abs(blue) % 256

        color: int = (blue << 16) | (green << 8) | red
        return color
