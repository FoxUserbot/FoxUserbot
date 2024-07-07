from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

import time


@Client.on_message(filters.command("progressbar", prefixes=my_prefix()) & filters.me)
async def progressbar(client, message):
    try:
        text = ' '.join(message.text.split()[1:])

        total = 100
        bar_length = 10
        for i in range(total + 1):
            percent = 100.0 * i / total
            time.sleep(0.1)
            await message.edit(
                text + "\n[{:{}}] {:>3}%".format("█" * int(percent / (100.0 / bar_length)), bar_length, int(percent)))
    except IndexError:
        message.edit('No text here!')
module_list['Progressbar'] = f'{my_prefix()}progressbar [Text]'
file_list['Progressbar'] = 'progressbar.py'
