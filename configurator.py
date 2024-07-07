import os
import sys
import configparser


config_id = "2860432"
config_hash = "2fde6ca0f8ae7bb58844457a239c7214"
config_model = "FoxUserbot"

config = configparser.ConfigParser()
config.read("config.ini")


def api():
    get_id = config.get("pyrogram", "api_id")
    get_hash = config.get("pyrogram", "api_hash")
    get_device_model = config.get("pyrogram", "device_model")
    return get_id, get_hash, get_device_model


def my_api():
    try:
        api_id, api_hash, device_model = api()
    except:
        config.add_section("pyrogram")
        config.set("pyrogram", "api_id", config_id)
        config.set("pyrogram", "api_hash", config_hash)
        config.set("pyrogram", "device_model", config_model)
        with open("config.ini", "w") as config_file:
            config.write(config_file)

        api_id = config_id
        api_hash = config_hash
        device_model = config_model
        print(f"Not found config.ini\nGenerating new...")
    return api_id, api_hash, device_model
