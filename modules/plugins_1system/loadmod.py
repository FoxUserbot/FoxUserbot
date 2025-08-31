from pyrogram import Client
from modules.plugins_1system.restarter import restart
from command import fox_command, fox_sudo, who_message
import os
import wget


@Client.on_message(fox_command("loadmod", "Loadmod", os.path.basename(__file__), "[link to the module/reply]") & fox_sudo())
async def loadmod(client, message):
    message = await who_message(client, message, message.reply_to_message)
    await message.edit(f"<emoji id='5190903199137013741'>🔍</emoji> **Checking and load module**")
    try:
        link = message.text.split()[1]
        wget.download(link, 'modules/plugins_2custom/')
        await message.edit(
            f"<emoji id='5237699328843200968'>✅</emoji> **The module has been loaded successfully** \nRestart..."
        )
        await restart(message, restart_type="restart")
    except:
        await client.download_media(message.reply_to_message.document, file_name='modules/plugins_2custom/')
        await message.edit(
            f"<emoji id='5237699328843200968'>✅</emoji> **The module has been loaded successfully** \nRestart..."
        )
        await restart(message, restart_type="restart")
