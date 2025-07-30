from pyrogram import Client, filters
from modules.plugins_1system.restarter import restart
from command import fox_command
import os
import wget


@Client.on_message(fox_command("loadmod", "Loadmod", os.path.basename(__file__), "[link to the module/reply]") & filters.me)
async def loadmod(client, message):
    if not message.reply_to_message:
        await message.edit("<b>Load module...</b>")
        link = message.command[1]
        wget.download(link, 'modules/plugins_2custom/')
        await message.edit(
            f"<b>**The module has been loaded successfully.**\nRestart..."
        )
        await restart(message, restart_type="restart")
    else:
        await client.download_media(message.reply_to_message.document, file_name='modules/plugins_2custom/')
        await message.edit(
            f"<b>**The module has been loaded successfully.**\nRestart..."
        )
        await restart(message, restart_type="restart")

