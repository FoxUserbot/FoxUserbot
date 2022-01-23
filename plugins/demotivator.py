from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.settings.main_settings import module_list, file_list
import asyncio
import time

from prefix import my_prefix
prefix = my_prefix()




# Демотиватор
@Client.on_message(filters.command("dem", prefix) & filters.me)
async def demotivator(client: Client, message: Message):
    await message.edit("Creating demotivator..")

    if message.reply_to_message.photo:
        await client.unblock_user("memegeneration_bot")
        capt = "1. " + message.text.split(prefix + "dem ", maxsplit=1)[1]
        await client.send_photo(chat_id="memegeneration_bot", photo=message.reply_to_message.photo.file_id, caption=capt)
        photo = False

        while not photo:
            try:
                await asyncio.sleep(1)
                iii = await client.get_history("memegeneration_bot")
                await client.send_photo(chat_id=message.chat.id, photo=iii[0].photo.file_id)
                photo = True
                await message.delete()
            except:
                await asyncio.sleep(0.5)
    else:
        await message.edit("Please, reply to photo")


module_list['Demotivator'] = f'{prefix}dem [reply to photo]'
file_list['Demotivator'] = 'demotivator.py'