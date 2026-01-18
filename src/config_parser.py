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
        param.append(False)
        self.__config.update({name: param})

    def get_config(self) -> dict[str, list[Any, type, Any]]:
        return self.__config

    def parse_file(self, file: BinaryIO) -> None:
        config = self.get_config()
        try:
            try:
                parameters = config.keys()
                for line in get_next_line(file):
                    parameter, value = get_value(line)
                    if parameter in parameters:
                        fill_param(config, parameter, value)
                    else:
                        raise ConfigError(f"unknown parameter: {parameter}")

                check_config(config)
            except Exception as e:
                config.clear()
                print(e)
        except FileNotFoundError as e:
            print(f"Parsing error :{e}")

    def get_value(self, parameter: str) -> Any:
        config = self.get_config()
        parameters = config.keys()

        if parameter in parameters:
            return (config[parameter][0])
        return None


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
        if None in value:
            keys = [key for key, v in config.items() if v[0] is None]
            raise ConfigError(f"missing value(s): {keys}")


def fill_param(config: dict[str, list[None, type, Any]],
               parameter: str, value: str):
    parameter_list = config[parameter]
    if parameter_list[-1] is True:
        raise ConfigError(f"Double declaration for \"{parameter}\"")
    else:
        parameter_list[-1] = True

    if parameter_list[1] == tuple:
        separator = parameter_list[4]
        parameter_list[0] = "Error"
        new_value = value.split(separator)

        if len(new_value) != parameter_list[2]:
            raise (ConfigError(f"invalid argument\"{value}\" for {parameter}"))

        types = parameter_list[3]

        if len(types) != parameter_list[2]:
            raise (ConfigError(f"invalid argument\"{value}\" for {parameter}"))

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
            raise (ConfigError(f"invalid argument\"{value}\" for {parameter}"))
    else:
        value = parameter_list[1](value)

    parameter_list[0] = value
