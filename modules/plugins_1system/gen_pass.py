from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

import string
from random import choice

@Client.on_message(filters.command('gen_password', prefixes=my_prefix()) & filters.me)
async def gen_pass(client, message):
    try:
        char = message.command[1]
        alphabet = string.ascii_letters + string.digits
        password = ''
        for _ in range(int(char)):
            password = password + choice(alphabet)
        await message.edit(f"**Generated password:** {password}`")
    except ValueError:
        await message.edit(f'Input a number!')
    except IndexError:
        await message.edit(f'Not input a argument!')

module_list['GeneratePassword'] = f'{my_prefix()}gen_password [password length]'
file_list['GeneratePassword'] = 'gen_pass.py'
