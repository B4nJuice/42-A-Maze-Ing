from typing import TextIO
from typing import Any
from typing import Iterator


class ConfigError(Exception):
    """Custom exception for configuration errors."""
    def __init__(self, message: str = "undefined") -> None:
        """Initialize the exception with a custom error message.

        Parameters
        ----------
        message : str, optional
            The error message describing the configuration issue.
            Defaults to "undefined".

        Returns
        -------
        None
        """
        super().__init__(f"Config error: {message}")


class Config():
    """Manage and parse a configuration file.

    This class provides utilities to register configuration parameters,
    parse them from a file, validate their types, and retrieve their values.

    Attributes
    ----------
    commentary_str : str
        The prefix string used to identify comment lines (default is "#").
    """
    def __init__(self) -> None:
        """Initialize an empty configuration registry.

        Creates the internal dictionary used to store configuration
        parameters and sets the default commentary prefix to "#".

        Returns
        -------
        None
        """
        self.__config: dict[str, Any] = {}
        self.__config = {}
        self.__commentary_str: str = "#"

    def set_commentary_str(self, commentary_str: str) -> None:
        """Set the prefix used to identify comment lines in the config file.

        Parameters
        ----------
        commentary_str : str
            The string that marks a line as a comment.

        Raises
        ------
        ConfigError
            If `commentary_str` is not a string.

        Returns
        -------
        None
        """
        if not isinstance(commentary_str, str):
            raise ConfigError(
                f"commentary_str: {commentary_str} is not a string"
                )
        self.__commentary_str = commentary_str

    def get_commentary_str(self) -> str:
        """Return the current comment prefix string.

        Returns
        -------
        str
            The string used to identify comment lines.
        """
        return self.__commentary_str

    def add_parameter(self, name: str, param: list[Any]) -> None:
        """Register a new configuration parameter and its type specification.

        This method adds a parameter to the internal configuration registry.
        The parameter definition includes its default value and a type
        specification describing how its value should be validated and
        converted when parsed.

        The ``param`` argument must follow the structure used by the
        configuration system:

        - index 0: default value (None to set the parameter as not facultative)
        - index 1: type specification

        The type specification format is:

        - [int], [str], [bool], etc. for simple types
        - [tuple, n, nested_types, separator] for structured tuples where:
            * n is the expected number of elements,
            * nested_types is a list of type specifications (one per element),
            * separator is the string used to split the input value

        This method automatically appends an internal boolean flag indicating
        whether the parameter has already been set.

        Parameters
        ----------
        name : str
            The name of the configuration parameter (e.g., "WIDTH",
            "BACKGROUND_COLOR").
        param : list
            A list containing the default value and its associated type
            specification.

        Returns
        -------
        None
            This method modifies the internal configuration dictionary in
            place.

        Examples
        --------
        >>> config.add_parameter("WIDTH", [20, [int]])
        >>> config.add_parameter("ENTRY",
        ...     [(0, 0), [tuple, 2, [[int], [int]], ","]])
        >>> config.add_parameter("BACKGROUND_COLOR",
        ...     [(255, 255, 255),
        ...      [tuple, 3, [[int], [int], [int]], ","]])
        """
        config = self.get_config()
        param.append(False)
        config.update({name: param})

    def get_config(self) -> dict[str, list[Any]]:
        """Return the internal configuration dictionary.

        Returns
        -------
        dict[str, list]
            The dictionary storing all registered configuration parameters.
        """
        return self.__config

    def parse_file(self, file: TextIO) -> None:
        """Parse a configuration file and update parameter values.

        Each non-empty and non-comment line must follow the format:
        `PARAMETER=VALUE`. The value is validated and converted
        according to its declared type specification.

        Parameters
        ----------
        file : TextIOWrapper
            The file object to read and parse.

        Raises
        ------
        ConfigError
            If an unknown parameter is encountered.
            If a value does not match its expected type.
            If required parameters are missing.

        Returns
        -------
        None
        """
        config = self.get_config()
        parameters = config.keys()
        for line in self.get_next_line(file):
            if line == "\n" or line.startswith(self.get_commentary_str()):
                continue
            parameter, value = self.get_unprocessed_value(line)
            if parameter in parameters:
                new_value = self.apply_types(parameter, config[parameter],
                                             value)
                config[parameter][0] = new_value
                config[parameter][2] = True
            else:
                raise ConfigError(f"Unknown parameter: {parameter}")

        self.check_config()

    def get_value(self, parameter: str) -> Any:
        """Return the value of a configuration parameter.

        Parameters
        ----------
        parameter : str
            The name of the parameter.

        Returns
        -------
        Any
            The value of the parameter if it exists, otherwise None.
        """
        config = self.get_config()
        parameters = config.keys()

        if parameter in parameters:
            return (config[parameter][0])
        return None

    def apply_types(self, parameter: str, parameter_list: list[Any],
                    value: Any) -> Any:
        """Convert a configuration parameter value to its declared type.

        This method validates and converts a string value according to the
        type specification stored in ``parameter_list``. Supported types are:

        - bool: accepts the strings "True" or "False" (not case-insensitive).
        - simple types: any callable type such as int, str or float.
        - tuple: a structured tuple with:
            * a fixed number of elements,
            * a list of nested type specifications,
            * a separator used to split the input string.

        Tuple types can be nested recursively (e.g., tuple of tuples).

        The method also ensures that a parameter is not declared more than
        once.

        Parameters
        ----------
        parameter : str
            The name of the parameter being processed. Used for error
            reporting.
        parameter_list : list[Any]
            A structure describing the parameter:
            - index 0: default value (unused here),
            - index 1: type specification,
            - index 2: boolean indicating whether the parameter was already
            set.
        value : str
            The raw string value to convert.

        Returns
        -------
        Any
            The converted value with the appropriate type applied.

        Raises
        ------
        ConfigError
            If the parameter is declared more than once.
            If the value does not match the expected type specification.
            If a tuple has an invalid number of elements.
            If a boolean value is not "True" or "False".
        """
        already_processed = parameter_list[2]
        separator: str = ""
        if already_processed is True:
            raise ConfigError(f"Double declaration for \"{parameter}\"")

        real_type = parameter_list[1]
        if real_type[0] == bool:
            if value.capitalize() == "True":
                value = True
            elif value.capitalize() == "False":
                value = False
            else:
                raise (ConfigError(
                    f"invalid argument \"{value}\" for {parameter}"))

        elif real_type[0] == tuple:
            separator = real_type[3]
            new_value = value.split(separator)

            n_types = real_type[1]
            if n_types != len(new_value):
                raise (ConfigError(
                    f"invalid argument \"{value}\" for {parameter}"
                    )
                )

            types = real_type[2]
            if n_types != len(types):
                raise (ConfigError(
                    f"invalid argument \"{value}\" for {parameter}"
                    )
                )

            value = []
            for i, nested_real_type in enumerate(types):
                type_list: list[Any] = []
                type_list.append(None)
                type_list.append(nested_real_type)
                type_list.append(False)
                value.append(self.apply_types(parameter,
                                              type_list, new_value[i]))
            value = tuple(value)

        elif real_type[0] == dict:
            separator = real_type[2]
            real_type.insert(1, len(value.split(separator)))
            real_type[0] = tuple
            tuple_value: tuple[Any] = self.apply_types(
                    parameter, parameter_list, value
                )
            list_value: list[tuple[Any]] = list(tuple_value)

            for element in list_value:
                if len(element) != 2:
                    raise ConfigError(
                            f"invalid argument \"{value}\" for {parameter}"
                        )

            result: dict[Any, Any] = {}
            for element in list_value:
                if not isinstance(element, (list, tuple)) or len(element) != 2:
                    raise ConfigError(
                        f"invalid argument \"{value}\" for {parameter}"
                    )
                k, v = element[0], element[1]
                result[k] = v
            value = result

        else:
            value = real_type[0](value)

        return value

    @staticmethod
    def get_next_line(file: TextIO) -> Iterator[str]:
        """Yield lines from a file one by one.

        Parameters
        ----------
        file : TextIOWrapper
            The file object to read.

        Yields
        ------
        str
            The next line in the file.
        """
        line: str = ""
        while True:
            line = file.readline()
            if not line:
                break
            yield line

    @staticmethod
    def get_unprocessed_value(line: str) -> tuple[str, str]:
        """Split a configuration line into parameter name and raw value.

        The line must contain exactly one "=" character.

        Parameters
        ----------
        line : str
            The line to process.

        Returns
        -------
        tuple[str, str]
            A tuple containing the parameter name and the stripped value.

        Raises
        ------
        ConfigError
            If the line format is invalid.
        """
        if line.count("=") != 1:
            raise ConfigError(f"undefined config line : {line}")
        parameter, value = line.split("=")
        parameter = parameter.strip()
        value = value.strip()
        return (parameter, value)

    def check_config(self) -> None:
        """Validate that all configuration parameters have assigned values.

        Raises
        ------
        ConfigError
            If one or more parameters have no value assigned.

        Returns
        -------
        None
        """
        config = self.get_config()
        values = config.values()
        for value in values:
            if value[0] is None:
                keys = [key for key, v in config.items() if v[0] is None]
                raise ConfigError(f"missing value(s): {keys}")
