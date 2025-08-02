from pyrogram import Client, filters
from pyrogram.types import Message
from command import fox_command
import os
import zipfile
import wget
import shutil

def restart_executor(chat_id=None, message_id=None, text=None, thread=None):
    if os.name == "nt":
        os.execvp(
            "python",
            [
                "python",
                "main.py",
                f"{chat_id}",
                f"{message_id}",
                f"{text}",
                f"{thread}" if thread else "None",
            ],
        )
    else:
        os.execvp(
            "python3",
            [
                "python3",
                "main.py",
                f"{chat_id}",
                f"{message_id}",
                f"{text}",
                f"{thread}" if thread else "None",
            ],
        )


async def restart(message: Message, restart_type):
    if restart_type == "update":
        text = "1"
    else:
        text = "2"
    thread_id = message.message_thread_id if message.message_thread_id else None
    restart_executor(message.chat.id, message.id, text, thread_id)


# Restart
@Client.on_message(fox_command("restart", "Restarter", os.path.basename(__file__)) & filters.me)
async def restart_get(client, message):
    try:
        await message.edit("<emoji id='5264727218734524899'>🔄</emoji> **Restarting userbot...**")
        await restart(message, restart_type="restart")
    except:
        await message.edit("<emoji id='5210952531676504517'>❌</emoji> **An error occured...**")


# Update
@Client.on_message(fox_command("update", "Restarter", os.path.basename(__file__)) & filters.me)
async def update(client, message):
    try:
        await message.edit('<emoji id="5264727218734524899">🔄</emoji> **Updating...**')
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

        await message.edit('<emoji id="5237699328843200968">✅</emoji> **Userbot succesfully updated\nRestarting...**')
        await restart(message, restart_type="update")
    except:
        await message.edit(f"<emoji id='5210952531676504517'>❌</emoji> **An error occured...**")