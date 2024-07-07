from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
import random


from prefix import my_prefix


@Client.on_message(filters.command("chance", prefixes=my_prefix()) & filters.me)
async def chance(client, message):
    text = ' '.join(message.text.split()[1:])
    await message.edit(f"{text}\nChance: {random.randint(1, 100)}%")


module_list['Chance'] = f'{my_prefix()}chance [Text]'
file_list['Chance'] = 'chance.py'
