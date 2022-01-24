from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.settings.main_settings import module_list, file_list
from plugins.restarter import restart
import asyncio
import time

from prefix import my_prefix
prefix = my_prefix()

@Client.on_message(filters.command("online", prefix) & filters.me)
async def online_now(client: Client, message: Message):
    await message.edit("AutoOnline activated")
    while True:
        iii = await client.send_message("me", "bruh")
        await client.delete_messages("me", iii.message_id)
        await asyncio.sleep(45)

@Client.on_message(filters.command("offline", prefix) & filters.me)
async def offline_now(client: Client, message: Message):
    await message.edit("AutoOnline deactivated\nRestart...")
    await restart(message, restart_type="restart")

module_list['AutoOnline'] = f'{prefix}online | {prefix}offline'
file_list['AutoOnline'] = 'autoonline.py'