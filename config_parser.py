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
            "WIDHT": [None, int],
            "HEIGHT": [None, int],
            "ENTRY": [None, tuple, 2],
            "EXIT": [None, tuple, 2],
            "OUTPUT_FILE": [None, str],
            "PERFECT": [None, bool],
        }

        parse_file(file_name, self.__config)

    def get_config(self):
        return self.__config


def get_next_line(file: BinaryIO) -> Generator[int, str, None]:
    line = 1
    while line:
        line = file.readline()
        if line == "" or line is None:
            return None
        yield line


def get_value(line: str) -> tuple:
    if line.count("=") != 1:
        raise ConfigError(f"undefined config line : {line}")
    parameter, value = line.split("=")
    value = value.replace('\n', '')
    value = value.strip()
    return (parameter, value)


def check_config(config: dict[str, list[None, type, Any]]) -> None:
    values = config.values()
    if None in values:
        keys = [key for key, value in config.items() if value[0] is None]
        raise ConfigError(f"missing value(s): {keys}")


def parse_file(file_name: str, config: list[None, type, Any]) -> None:
    try:
        file = open(file_name)

        try:
            parameters = config.keys()
            for line in get_next_line(file):
                parameter, value = get_value(line)
                if parameter in parameters:
                    parameter_list = config[parameter]
                    try:
                        if parameter_list[1] == tuple:
                            try:
                                new_value = value.split(",")
                                if len(new_value) != parameter_list[2]:
                                    raise (ConfigError(f"invalid argument\
\"{value}\" for {parameter}"))
                                for num in new_value:
                                    num = int(num)
                                value = new_value
                            except Exception as e:
                                raise ConfigError(e)
                        else:
                            value = parameter_list[1](value)
                        parameter_list[0] = value
                    except Exception as e:
                        print(e)
                else:
                    raise ConfigError(f"unknown parameter: {parameter}")

            check_config(config)
        except ConfigError as e:
            print(e)

        file.close()
    except FileNotFoundError as e:
        print(f"Parsing error :{e}")
