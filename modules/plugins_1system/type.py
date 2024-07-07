from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

import asyncio


@Client.on_message(filters.command("type", prefixes=my_prefix()) & filters.me)
async def types(client, message):
    try:
        orig_text = ' '.join(message.text.split()[1:])
        text = orig_text
        tbp = ""
        typing_symbol = "▒"
        while tbp != orig_text:
            await message.edit(str(tbp + typing_symbol))
            await asyncio.sleep(0.10)
            tbp = tbp + text[0]
            text = text[1:]
            await message.edit(str(tbp))
            await asyncio.sleep(0.10)
    except IndexError:
        message.edit('No text here!')


module_list['Type'] = f'{my_prefix()}type [text]'
file_list['Type'] = 'type.py'
