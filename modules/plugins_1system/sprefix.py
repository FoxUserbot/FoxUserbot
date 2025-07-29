from pyrogram import Client, filters
from modules.plugins_1system.restarter import restart
from command import fox_command
import os
import configparser


PATH_FILE = "userdata/config.ini"

config = configparser.ConfigParser()
config.read(PATH_FILE)

@Client.on_message(fox_command(command1="sp", Module_Name="SetPrefix", names=os.path.basename(__file__), arg="[new prefix]") & filters.me)
async def sprefix(client, message):
    if len(message.command) > 1:
        prefixgett = message.command[1]
        config.set("prefix", "prefix", prefixgett)
        with open(PATH_FILE, "w") as config_file:
            config.write(config_file)
        await message.edit(
            f"<b>prefix [ <code>{prefixgett}</code> ] set!</b>\nRestarting userbot..."
        )
        await restart(message, restart_type="restart")
    else:
        await message.edit("<b>prefix don't be None</b>")

