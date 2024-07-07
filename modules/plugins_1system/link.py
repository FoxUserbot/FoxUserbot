from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list

from prefix import my_prefix



@Client.on_message(filters.command("link", prefixes=my_prefix()) & filters.me)
async def link(client, message):
    try:
        link = message.command[1]
        text = " ".join(message.command[2:])
        await message.delete()
        await client.send_message(message.chat.id, f'<a href="{link}">{text}</a>', disable_web_page_preview=True)
    except IndexError:
        message.edit('No text here!')

module_list['LinkInText'] = f'{my_prefix()}link [link] [text]'
file_list['LinkInText'] = 'link.py'
