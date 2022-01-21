from pyrogram import Client, filters
from plugins.settings.main_settings import module_list, settings
import os

prefix = settings['prefix']

@Client.on_message(filters.command('unloadmod', prefixes=prefix))
async def unloadmod(client, message):
    try:
        module_name = message.text.replace('!unloadmod', '')
        params = module_name.split()
        module_name = params[0]
        del module_list[module_name]
        file = file_list[module_name]
        os.system(f'rm plugins/{file}')
        await message.edit("**The module has been successfully unloaded.**")
    except:
        await message.edit("**An error has occurred.**")
 
module_list['Unloadmod'] = f'{prefix}unloadmod [module name]'