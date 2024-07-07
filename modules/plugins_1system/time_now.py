from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

import datetime


@Client.on_message(filters.command("time", prefixes=my_prefix()) & filters.me)
async def time(client, message):
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d - %H:%M:%S")
    now = datetime.datetime.now().strftime("Date: %d/%m/%Y\nTime: %H:%M:%S")
    await message.edit(now)


module_list['TimeNow'] = f'{my_prefix()}time'
file_list['TimeNow'] = 'time_now.py'
