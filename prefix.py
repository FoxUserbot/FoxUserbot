import os
import sys
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def get_prefix():
    prefix = config.get("prefix", "prefix")
    return prefix


def my_prefix():
    try:
        prefix = get_prefix()
    except:
        config.add_section("prefix")
        config.set("prefix", "prefix", "!")
        with open("config.ini", "w") as config_file:
            config.write(config_file)
        prefix = "!"
    return prefix
