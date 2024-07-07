from pyrogram import Client, filters
from modules.plugins_1system.restarter import restart
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix


import asyncio


@Client.on_message(filters.command("online", prefixes=my_prefix()) & filters.me)
async def online_now(client, message):
    await message.edit("AutoOnline activated")
    while True:
        iii = await client.send_message("me", "bruh")
        await client.delete_messages("me", iii.id)
        await asyncio.sleep(45)


@Client.on_message(filters.command("offline", prefixes=my_prefix()) & filters.me)
async def offline_now(client, message):
    await message.edit("AutoOnline deactivated\nRestart...")
    await restart(message, restart_type="restart")


module_list['AutoOnline'] = f'{my_prefix()}online | {my_prefix()}offline'
file_list['AutoOnline'] = 'autoonline.py'
