from pyrogram import Client
from pyrogram.types import Message
from command import fox_command, fox_sudo, who_message
import os
import zipfile
import wget
import shutil
import traceback

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


async def update_repository(client, message, repo_url, repo_type):
    try:
        try:
            os.remove("temp/archive.zip")
        except:
            pass
        await message.edit(f'<emoji id="5264727218734524899">🔄</emoji> **Updating {repo_type}...**')

        wget.download(repo_url, 'temp/archive.zip')

        with zipfile.ZipFile("temp/archive.zip", "r") as zip_ref:
            file_list = zip_ref.namelist()
            root_folder = None
            for file in file_list:
                if file.endswith('/') and file.count('/') == 1:
                    root_folder = file.strip('/')
                    break
            
            if not root_folder:
                raise Exception("Not found root dir")

            zip_ref.extractall("temp/")

        os.remove("temp/archive.zip")
        shutil.make_archive("temp/archive", "zip", f"temp/{root_folder}/")
        with zipfile.ZipFile("temp/archive.zip", "r") as zip_ref:
            zip_ref.extractall(".")

        os.remove("temp/archive.zip")
        shutil.rmtree(f"temp/{root_folder}")
        
        await message.edit("<emoji id='5237699328843200968'>✅</emoji> **Userbot successfully updated\n<emoji id='5264727218734524899'>🔄</emoji> Restarting...**")
        await restart(message, restart_type="update")
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        error_message = f"<emoji id='5210952531676504517'>❌</emoji> **An error occurred:**\n\n`{str(e)}`\n\n**Traceback:**\n`{error_traceback[-1000:]}`"  # Ограничиваем длину traceback

        if len(error_message) > 4000:
            error_message = error_message[:4000] + "..."
        
        await message.edit(error_message)


# Restart
@Client.on_message(fox_command("restart", "Restarter", os.path.basename(__file__)) & fox_sudo())
async def restart_get(client, message):
    message = await who_message(client, message, message.reply_to_message)
    try:
        await message.edit("<emoji id='5264727218734524899'>🔄</emoji> **Restarting userbot...**")
        await restart(message, restart_type="restart")
    except:
        await message.edit("<emoji id='5210952531676504517'>❌</emoji> **An error occured...**")


# Update main
@Client.on_message(fox_command("update", "Restarter", os.path.basename(__file__)) & fox_sudo())
async def update(client, message):
    message = await who_message(client, message, message.reply_to_message)
    await update_repository(client, message, "https://github.com/FoxUserbot/FoxUserbot/archive/refs/heads/main.zip", "main")


# Update beta
@Client.on_message(fox_command("beta", "Restarter", os.path.basename(__file__)) & fox_sudo())
async def update_beta(client, message):
    message = await who_message(client, message, message.reply_to_message)
    await update_repository(client, message, "https://github.com/FoxUserbot/FoxUserbot-dev/archive/refs/heads/main.zip", "beta")
