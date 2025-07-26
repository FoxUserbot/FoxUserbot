import os
import sys
import configparser

PATH_FILE = "userdata/config.ini"

config = configparser.ConfigParser()
config.read(PATH_FILE)

def get_prefix():
    prefix = config.get("prefix", "prefix")
    return prefix


def my_prefix():
    try:
        prefix = get_prefix()
    except:
        config.add_section("prefix")
        config.set("prefix", "prefix", "!")
        with open(PATH_FILE, "w") as config_file:
            config.write(config_file)
        prefix = "!"
    return prefix
