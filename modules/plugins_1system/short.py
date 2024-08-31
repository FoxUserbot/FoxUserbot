from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

import requests


@Client.on_message(filters.command("short", prefixes=my_prefix()) & filters.me)
async def shorten_link_command(client, message):
    try:
        await message.edit("Shorting...")
        if message.reply_to_message:
            link = message.reply_to_message.text
        else:
            link = message.command[1]

        full_url = link.replace("https://", "").replace("http://", "")
        response = requests.get('https://tinyurl.com/api-create.php?url=' + full_url)

        short_url = response.text
        
        await message.edit(f"Short URL: {short_url}")
    except Exception as error:
        await message.edit(f"Error: {error}")


module_list['ShortURL'] = f'{my_prefix()}short [Reply | link]'
file_list['ShortURL'] = 'short.py'
