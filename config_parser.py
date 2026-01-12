# !/usr/bin/env python3

from typing import BinaryIO
from collections.abc import Generator


class ConfigError(Exception):
    def __init__(self, message="undefined"):
        super().__init__(f"Config error: {message}")


class Config():
    def __init__(self, file_name: str):
        self.config = {
            "WIDHT": None,
            "HEIGHT": None,
            "ENTRY": None,
            "EXIT": None,
            "OUTPUT_FILE": None,
            "PERFECT": None,
        }

        parse_file(file_name, self.config)


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
    return (parameter, value)


def check_config(config: dict[str, str]) -> None:
    values = config.values()
    if None in values:
        keys = [key for key, value in config.items() if value is None]
        raise ConfigError(f"missing value(s): {keys}")


def parse_file(file_name: str, config: dict[str, None]) -> None:
    try:
        file = open(file_name)

        try:
            parameters = config.keys()
            for line in get_next_line(file):
                parameter, value = get_value(line)
                if parameter in parameters:
                    config.update({parameter: value})
                else:
                    raise ConfigError(f"unknown parameter: {parameter}")

            check_config(config)
        except ConfigError as e:
            print(e)

        file.close()
    except FileNotFoundError as e:
        print(f"Parsing error :{e}")
