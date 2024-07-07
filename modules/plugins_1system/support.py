from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix


@Client.on_message(filters.command('support', prefixes=my_prefix()) & filters.me)
async def support(client, message):
    await message.delete()
    await client.send_photo(
        chat_id=message.chat.id,
        photo="https://github.com/FoxUserbot/FoxUserbot/raw/main/logo.png",
        caption="Support: @a9_fm"
    )


module_list['Support'] = f'{my_prefix()}support'
file_list['Support'] = 'support.py'
