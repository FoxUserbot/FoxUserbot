from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from modules.plugins_1system.restarter import restart
from command import fox_command
import os


@Client.on_message(fox_command("unloadmod", "Unloadmod", os.path.basename(__file__), "[module name]") & filters.me)
async def unloadmod(client, message):
    try:
        from prefix import my_prefix
        module_name = message.text.replace(f'{my_prefix()}unloadmod', '')
        params = module_name.split()
        module_name = params[0]
        del module_list[module_name]
        file = file_list[module_name]
        os.remove(f'modules/plugins_2custom/{file}')
        await message.edit("<emoji id='5237699328843200968'>✅</emoji> **The module has been successfully unloaded.**\n<emoji id='5264727218734524899'>🔄</emoji> Restart...")
        await restart(message, restart_type="restart")
    except Exception as error:
        await message.edit(f"<emoji id='5210952531676504517'>❌</emoji> **An error has occurred.**\nLog: not found {error}")
