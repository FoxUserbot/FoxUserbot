  
from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.settings.main_settings import settings, module_list, version

prefix = settings['prefix'] 

@Client.on_message(filters.command('version', prefixes=prefix) & filters.me) 
async def version(client: Client, message: Message):
    await message.edit(f'**Version:** ```{version}```')

module_list['Version'] = f'{prefix}version'
