from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import file_list
from command import fox_command
import os


@Client.on_message(fox_command("uploadmod", "Uploadmod", os.path.basename(__file__), "[module name]") & filters.me)
async def uploadmod(client, message):
    try:
        from prefix import my_prefix
        module_name = message.text.replace(f'{my_prefix()}uploadmod', '')
        params = module_name.split()
        module_name = params[0]
        file = file_list[module_name]
        await client.send_document(
            message.chat.id,
            f"modules/plugins_2custom/{file}",
            caption=f"<emoji id='5283051451889756068'>🦊</emoji> Module `{module_name}`\nfor FoxUserbot <emoji id='5283051451889756068'>🦊</emoji>\n<b>You can install the module by replying [prefix]loadmod</b>",
            message_thread_id=message.message_thread_id
        )
        await message.delete()
    except Exception as error:
        await message.edit(f"<emoji id='5210952531676504517'>❌</emoji> **An error has occurred.**\nLog: {error}")
