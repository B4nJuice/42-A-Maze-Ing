# !/usr/bin/env python3

from typing import BinaryIO
from typing import Any
from collections.abc import Generator


class ConfigError(Exception):
    def __init__(self, message="undefined"):
        super().__init__(f"Config error: {message}")


class Config():
    def __init__(self, file_name: str):
        self.__config = {
            "WIDTH": [None, int],
            "HEIGHT": [None, int],
            "ENTRY": [None, tuple, 2],
            "EXIT": [None, tuple, 2],
            "OUTPUT_FILE": [None, str],
            "PERFECT": [None, bool],
            "SEED": [None, int],
            "ICON_FILE": [None, str]
        }

        parse_file(file_name, self.__config)

    def get_config(self) -> dict[str, list[None, type, Any]]:
        return self.__config

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
    if parameter_list[0] is not None:
        raise ConfigError(f"Double declaration for \"{parameter}\"")

    if parameter_list[1] == tuple:
        parameter_list[0] = "Error"
        new_value = value.split(",")

        if len(new_value) != parameter_list[2]:
            raise (ConfigError(f"invalid argument\"{value}\" for {parameter}"))

        value = []

        for i in new_value:
            value.append(int(i))

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


def parse_file(file_name: str, config: list[None, type, Any]) -> None:
    try:
        file = open(file_name)

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

        file.close()
    except FileNotFoundError as e:
        print(f"Parsing error :{e}")
