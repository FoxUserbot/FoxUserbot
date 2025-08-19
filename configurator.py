import os
import sys
import configparser

# default values (TDesktop)
config_id = "2040"
config_hash = "b18441a1ff607e10a989891a5462e627"
config_model = "FoxUserbot"

PATH_FILE = "userdata/config.ini"

config = configparser.ConfigParser()
config.read(PATH_FILE)

def api():
    get_id = config.get("pyrogram", "api_id")
    get_hash = config.get("pyrogram", "api_hash")
    get_device_model = config.get("pyrogram", "device_model")
    return get_id, get_hash, get_device_model


def update_api(api_id, api_hash):
    # old variable (not work)
    old_config_id = ["2860432", "29679445"]
    old_config_hash = ["2fde6ca0f8ae7bb58844457a239c7214", "e656a7489649d542ceb3c326f54345ba"]
    
    config_changed = False
    
    if str(api_id) in old_config_id:
        api_id_temp = api_id
        api_id = config_id
        config.set("pyrogram", "api_id", config_id)
        config_changed = True
        print(f"Updated API ID from {api_id_temp} to {config_id}")
        
    if api_hash in old_config_hash:
        api_hash_temp = api_hash
        api_hash = config_hash
        config.set("pyrogram", "api_hash", config_hash)
        config_changed = True
        print(f"Updated API Hash from {api_hash_temp} to {config_hash}")

    if config_changed:
        with open(PATH_FILE, "w") as config_file:
            config.write(config_file)
        print("Config file updated successfully!")

    return api_id, api_hash


def my_api():
    try:
        api_id, api_hash, device_model = api()
        api_id, api_hash = update_api(api_id, api_hash)
    except (configparser.NoSectionError, configparser.NoOptionError):
        if not config.has_section("pyrogram"):
            config.add_section("pyrogram")
        
        config.set("pyrogram", "api_id", config_id)
        config.set("pyrogram", "api_hash", config_hash)
        config.set("pyrogram", "device_model", config_model)
        
        with open(PATH_FILE, "w") as config_file:
            config.write(config_file)
            
        api_id = config_id
        api_hash = config_hash
        device_model = config_model
        print(f"Not found config.ini\nGenerating new...")
    
    return api_id, api_hash, device_model