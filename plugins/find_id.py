from pyrogram import Client, filters
from plugins.settings.main_settings import module_list, file_list, settings
from pyrogram.types import Message
import asyncio

prefix = settings['prefix']

@Client.on_message(filters.command('find_id', prefixes=prefix) & filters.me)
async def find_id(client: Client, message: Message):
  await message.edit(f'**ID of this chat: ** ```{message.chat.id}```')
  
module_list['FindIDThisChat'] = f'{prefix}fing_id'
file_list['FindIDThisChat'] = 'find_id.py'
