from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

import asyncio


@Client.on_message(filters.command("q", prefixes=my_prefix()) & filters.me)
async def quotly(client, message):
    if not message.reply_to_message:
        await message.edit("Reply to message")
        return

    await client.unblock_user("QuotLyBot")
    await message.edit("Create quotes... wait...")
    await message.reply_to_message.forward("QuotLyBot")

    is_sticker = False

    while not is_sticker:
        try:
            async for iii in client.get_chat_history("QuotLyBot", limit=1):
                await client.send_sticker(message.chat.id, iii.sticker.file_id)
            is_sticker = True
            await message.delete()
        except:
            await asyncio.sleep(1)


module_list['Quotes'] = f'{my_prefix()}q [reply]'
file_list['Quotes'] = 'quotes.py'
