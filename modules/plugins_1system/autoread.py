from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix


the_regex = r"^r\/([^\s\/])+"
i = filters.chat([])


@Client.on_message(i)
async def auto_read(client, message):
    await client.read_history(message.chat.id)
    message.continue_propagation()


@Client.on_message(filters.command("autoread", prefixes=my_prefix()) & filters.me)
async def add_to_auto_read(client, message):
    if message.chat.id in i:
        i.remove(message.chat.id)
        await message.edit("Autoread deactivated")
    else:
        i.add(message.chat.id)
        await message.edit("Autoread activated")


module_list['AutoReadChat'] = f'{my_prefix()}autoread'
file_list['AutoReadChat'] = 'autoread.py'
