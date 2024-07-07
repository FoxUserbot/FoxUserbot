from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

import asyncio


@Client.on_message(filters.command("spamban", prefixes=my_prefix()) & filters.me)
async def spamban(client, message):
    await message.edit("Checking your account for Spamban...")
    await client.unblock_user("spambot")
    await client.send_message("spambot", "/start")
    async for iii in client.get_chat_history("spambot", limit=1):
        await message.edit(iii.text)


module_list['SpamBan'] = f'{my_prefix()}spamban'
file_list['SpamBan'] = 'spamban.py'
