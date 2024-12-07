import sys
import os

if len(sys.argv) < 3:
    print("Hasn't arguments")
else:
    api_id = sys.argv[1]
    api_hash = sys.argv[2]
    os.remove('configurator.py')
    with open('configurator.py', 'w+', encoding='utf-8') as file:
        file.write(f''' 
import os
import sys
import configparser
config_id = "{api_id}"
config_hash = "{api_hash}"
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
        print(f"Not found config.ini\\nGenerating new...")
    return api_id, api_hash, device_model
''')
