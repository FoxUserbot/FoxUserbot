from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix


@Client.on_message(filters.command('uploadmod', prefixes=my_prefix()) & filters.me)
async def uploadmod(client, message):
    try:
        module_name = message.text.replace(f'{my_prefix()}uploadmod', '')
        params = module_name.split()
        module_name = params[0]
        file = file_list[module_name]
        await client.send_document(
            message.chat.id,
            f"modules/plugins_2custom/{file}",
            caption=f"Module `{module_name}`\nfor FoxUserbot 🦊"
        )
        await message.delete()
    except Exception as error:
        await message.edit(f"**An error has occurred.**\nLog: {error}")


module_list['Uploadmod'] = f'{my_prefix()}uploadmod [module name]'
