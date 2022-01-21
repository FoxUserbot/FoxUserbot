from pyrogram import Client, filters
from plugins.settings.main_settings import module_list, file_list

from prefix import my_prefix
prefix = my_prefix()

@Client.on_message(filters.command('support', prefixes=prefix))
async def support(client, message):
    await message.delete()
    await client.send_photo(
    chat_id=message.chat.id,
    photo="logo.jpg",
    caption="""**FOX USERBOT**\n`По всем вопросам и предложениям обращаться к` @foxuserbot0"""
)

module_list['Support'] = f'{prefix}support'
file_list['Support'] = 'support.py'