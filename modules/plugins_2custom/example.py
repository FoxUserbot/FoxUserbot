from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list

from prefix import my_prefix



@Client.on_message(filters.command("example_edit", prefixes=my_prefix()) & filters.me)
async def example_edit(client, message):
    await message.edit("<code>This is an example module</code>")


module_list['Example'] = f'{my_prefix()}example_edit'
file_list['Example'] = 'example.py'
