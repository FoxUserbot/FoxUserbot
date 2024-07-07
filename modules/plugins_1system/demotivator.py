from prefix import my_prefix
from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
import asyncio



username_dem = "KlounsBot"

@Client.on_message(filters.command("dem", prefixes=my_prefix()) & filters.me)
async def demotivator(client, message):
    await message.edit("Creating demotivator..")
    if message.reply_to_message.photo:
        await client.unblock_user(username_dem)
        capt = ' '.join(message.text.split()[1:])
        await client.send_photo(
            chat_id=username_dem,
            photo=message.reply_to_message.photo.file_id,
            caption=capt
        )
        photo = False

        while not photo:
            try:
                await asyncio.sleep(2)
                async for iii in client.get_chat_history(username_dem, limit=1):
                    await client.send_photo(chat_id=message.chat.id, photo=iii.photo.file_id)
                photo = True
                await message.delete()
            except Exception as f:
                await message.edit(f)
                await asyncio.sleep(2)
    else:
        await message.edit("Please, reply to photo")


module_list['Demotivator'] = f'{my_prefix()}dem [reply to photo]'
file_list['Demotivator'] = 'demotivator.py'
