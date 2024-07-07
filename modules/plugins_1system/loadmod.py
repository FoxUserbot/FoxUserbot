from pyrogram import Client, filters
from modules.plugins_1system.restarter import restart
from modules.plugins_1system.settings.main_settings import module_list
from prefix import my_prefix

import wget


@Client.on_message(filters.command('loadmod', prefixes=my_prefix()) & filters.me)
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


module_list['Loadmod'] = f'{my_prefix()}loadmod [link to the module]'
