# !/usr/bin/env python3

from typing import BinaryIO
from typing import Any
from collections.abc import Generator


class ConfigError(Exception):
    def __init__(self, message="undefined"):
        super().__init__(f"Config error: {message}")


class Config():
    def __init__(self):
        self.__config = {}

    def add_parameter(self, name: str, param: list[
            Any, type, int, list[type], str]) -> None:
        config = self.get_config()
        param.append(False)
        config.update({name: param})

    def get_config(self) -> dict[str, list[Any, type, Any]]:
        return self.__config

    def parse_file(self, file: BinaryIO) -> None:
        config = self.get_config()
        parameters = config.keys()
        for line in get_next_line(file):
            parameter, value = get_value(line)
            if parameter in parameters:
                new_value = self.apply_types(parameter, config[parameter],
                                             value)
                config[parameter][0] = new_value
                config[parameter][2] = True
                # self.fill_param(config, parameter, value)
            else:
                raise ConfigError(f"unknown parameter: {parameter}")

        check_config(config)

    def get_value(self, parameter: str) -> Any:
        config = self.get_config()
        parameters = config.keys()

        if parameter in parameters:
            return (config[parameter][0])
        return None

    def apply_types(self, parameter: str, parameter_list: list[Any],
                    value: str) -> list[Any]:

        already_processed = parameter_list[2]
        if already_processed is True:
            raise ConfigError(f"Double declaration for \"{parameter}\"")

        real_type = parameter_list[1]
        if real_type[0] == bool:
            if value.capitalize() == "True":
                value = True
            elif value.capitalize() == "False":
                value = False
            else:
                raise (ConfigError(f"invalid argument\"{value}\"\
 for {parameter}"))
        elif real_type[0] == tuple:
            separator = real_type[3]
            n_types = real_type[1]
            new_value = value.split(separator)

            if n_types != len(new_value):
                raise (ConfigError(f"invalid argument\"{value}\"\
 for {parameter}"))

            types = real_type[2]

            if n_types != len(types):
                raise (ConfigError(f"invalid argument\"{value}\"\
 for {parameter}"))

            value = []
            for i, nested_real_type in enumerate(types):
                type_list = []
                type_list.append(None)
                type_list.append(nested_real_type)
                type_list.append(False)
                value.append(self.apply_types(parameter,
                                              type_list, new_value[i]))
            value = tuple(value)

        else:
            value = real_type[0](value)

        return value

    def fill_param(self, parameter: str, value: str) -> None:
        config = self.get_config()
        parameter_list = config[parameter]

        if parameter_list[-1] is True:
            raise ConfigError(f"Double declaration for \"{parameter}\"")
            parameter_list[-1] = True

        if parameter_list[1] == tuple:
            separator = parameter_list[4]
            parameter_list[0] = "Error"
            new_value = value.split(separator)

            if len(new_value) != parameter_list[2]:
                raise (ConfigError(f"invalid argument\"{value}\"\
 for {parameter}"))

            types = parameter_list[3]

            if len(types) != parameter_list[2]:
                raise (ConfigError(f"invalid argument\"{value}\"\
 for {parameter}"))

            value = []

            for i, v in enumerate(new_value):
                try:
                    value.append(types[i](v))
                except Exception as e:
                    raise ConfigError(e)

            value = tuple(value)
        elif parameter_list[1] == bool:
            if value.capitalize() == "True":
                value = True
            elif value.capitalize() == "False":
                value = False
            else:
                raise (ConfigError(f"invalid argument\"{value}\"\
 for {parameter}"))
        else:
            value = parameter_list[1](value)

        parameter_list[0] = value


def get_next_line(file: BinaryIO) -> Generator[int, str, None]:
    line = 1
    while line:
        line = file.readline()
        if line == "" or line is None:
            return None
        yield line


def get_value(line: str) -> tuple[str, str]:
    if line.count("=") != 1:
        raise ConfigError(f"undefined config line : {line}")
    parameter, value = line.split("=")
    value = value.replace('\n', '')
    value = value.strip()
    return (parameter, value)


def check_config(config: dict[str, list[None, type, Any]]) -> None:
    values = config.values()
    for value in values:
        if value[0] is None:
            keys = [key for key, v in config.items() if v[0] is None]
            raise ConfigError(f"missing value(s): {keys}")
