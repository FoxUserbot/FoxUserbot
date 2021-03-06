from pyrogram import Client, filters
from plugins.settings.main_settings import module_list, file_list
from time import perf_counter

from prefix import my_prefix
prefix = my_prefix()


@Client.on_message(filters.command('ping', prefixes=prefix) & filters.me)
async def ping(client, message):
    start = perf_counter()
    await message.edit("š| ā¾=== |š")
    await message.edit("š| =ā¾== |š")
    await message.edit("š| ==ā¾= |š")
    await message.edit("š| ===ā¾ |š")
    end = perf_counter()

    pinges = ((end - start) / 4)
    ping = pinges * 1000

    if 0 <= ping <= 199:
        connect = "š¢ Stable"
    if 199 <= ping <= 400:
        connect = "š  Good"
    if 400 <= ping <= 600:
        connect = "š“ Unstable"
    if 600 <= ping:
        connect = "ā  Check you network connection"
    await message.edit(f"<b>š Pong\nš¶</b> {round(ping)} ms\n{connect}")


module_list['Ping'] = f'{prefix}ping'
file_list['Ping'] = 'ping.py'
