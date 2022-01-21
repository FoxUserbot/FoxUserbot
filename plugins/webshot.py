from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.settings.main_settings import module_list, file_list, settings

prefix = settings['prefix']

@Client.on_message(filters.command("webshot", prefixes=prefix) & filters.me)
async def webshot(client: Client, message: Message):
    try:
        user_link = message.command[1]
        await message.delete()
        full_link = f"https://webshot.deam.io/{user_link}/?delay=2000"
        await client.send_document(message.chat.id, full_link, caption=f"**Screenshot of the page ** ```{user_link}```.")
    except:
        await message.delete()
        await client.send_message(
            message.chat.id, "**Something went wrong...**"
        )
        
module_list['Webshot'] = f'{prefix}webshot [link]'
file_list['Webshot'] = 'webshot.py'
