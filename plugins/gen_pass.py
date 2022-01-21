from pyrogram import Client, filters
from plugins.settings.main_settings import module_list, file_list, settings
from pyrogram.types import Message
import secrets
import string
import asyncio

prefix = settings['prefix']

@Client.on_message(filters.command('gen_password', prefixes=prefix) & filters.me)
async def gen_pass(client: Client, message: Message):
    char = message.command[1]
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(int(char)))
    await message.edit(f"**Generated password:** ```{password}```")
    
module_list['GeneratePassword'] = f'{prefix}gen_password [password length]'
file_list['GeneratePassword'] = 'gen_pass.py'