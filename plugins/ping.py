from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.settings.main_settings import module_list, file_list, settings

prefix = settings['prefix']

@Client.on_message(filters.command('ping', prefixes=prefix) & filters.me)
async def ping(client: Client, message: Message):
  await message.edit('🟢Pong!')

module_list['Ping'] = f'{prefix}ping'
file_list['Ping'] = 'ping.py'
