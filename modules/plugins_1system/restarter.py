from pyrogram import Client, filters
from pyrogram.types import Message
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

import os
import zipfile
import wget
import shutil


async def restart(message: Message, restart_type):
    if restart_type == "update":
        text = "1"
    else:
        text = "2"

    if os.name == "nt":
        await os.execvp(
            "python",
            [
                "python",
                "main.py",
                f"{message.chat.id}",
                f"{message.id}",
                f"{text}",
            ],
        )
    else:
        await os.execvp(
            "python3",
            [
                "python3",
                "main.py",
                f"{message.chat.id}",
                f"{message.id}",
                f"{text}",
            ],
        )


# Restart
@Client.on_message(filters.command("restart", prefixes=my_prefix()) & filters.me)
async def restart_get(client, message):
    try:
        await message.edit("**Restarting userbot...**")
        await restart(message, restart_type="restart")
    except:
        await message.edit("**An error occured...**")


# Update
@Client.on_message(filters.command('update', prefixes=my_prefix()) & filters.me)
async def update(client, message):
    try:
        await message.edit('**Updating...**')
        link = "https://github.com/FoxUserbot/FoxUserbot/archive/refs/heads/main.zip"
        wget.download(link, 'temp/archive.zip')

        with zipfile.ZipFile("temp/archive.zip", "r") as zip_ref:
            zip_ref.extractall("temp/")
        os.remove("temp/archive.zip")

        shutil.make_archive("temp/archive", "zip", "temp/FoxUserbot-main/")

        with zipfile.ZipFile("temp/archive.zip", "r") as zip_ref:
            zip_ref.extractall(".")
        os.remove("temp/archive.zip")
        shutil.rmtree("temp/FoxUserbot-main")

        await message.edit('**Userbot succesfully updated\nRestarting...**')
        await restart(message, restart_type="update")
    except:
        await message.edit(f"**An error occured...**")



module_list['Restarter'] = f'{my_prefix()}update | {my_prefix()}restart'
file_list['Restarter'] = 'restarter.py'
