# !/usr/bin/env python3

from config_parser import Config


config = Config("config.txt")
parsed = config.get_config()

print(parsed)

keys = parsed.keys()
values = parsed.values()
