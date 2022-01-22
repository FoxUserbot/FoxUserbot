from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.settings.main_settings import module_list, file_list
import os
import sys
import wget
import zipfile

from prefix import my_prefix
prefix = my_prefix()


async def restart(message: Message, restart_type):
    if restart_type == "update":
        text = "1"
    else:
        text = "2"
    try:
        await os.execvp(
            "python3",
            [
                "python3",
                "./main.py",
                f"{message.chat.id}",
                f"{message.message_id}",
                f"{text}",
            ],
        )
    except:
        await os.execvp(
            "python",
            [
                "python",
                "./main.py",
                f"{message.chat.id}",
                f"{message.message_id}",
                f"{text}",
            ],
        )


# Обновы
@Client.on_message(filters.command("restart", prefix) & filters.me)
async def restart_get(client: Client, message: Message):
    try:
        await message.edit("Restart...")
        await restart(message, restart_type="restart")
    except:
        await message.edit("**An error occured...**")


@Client.on_message(filters.command('update', prefixes=prefix) & filters.me)
async def update(client: Client, message: Message):
    try:
        await message.edit('**Updating...**')
        link = "https://github.com/FoxUserbot/FoxUserbot/archive/refs/heads/main.zip"
        wget.download(link, 'temp/archive.zip')
        with zipfile.ZipFile("temp/archive.zip", "r") as zip_ref:
            zip_ref.extractall("./..")
        os.remove("temp/archive.zip")

        await message.edit('**Userbot succesfully updated\nRestarting...**')
        await restart(message, restart_type="update")
    except:
        await message.edit("**An error occured...**")


module_list['starter'] = f'{prefix}update | {prefix}restart'
file_list['starter'] = 'starter.py'