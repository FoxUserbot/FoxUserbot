from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list

from prefix import my_prefix



@Client.on_message(filters.command("ladder", prefixes=my_prefix()) & filters.me)
async def ladder(client, message):
    try:
        orig_text = ' '.join(message.text.split()[1:])
        text = orig_text
        output = []
        for i in range(len(text) + 1):
            output.append(text[:i])
        ot = "\n".join(output)
        await message.edit(ot)
    except:
        await message.edit('Error in processing your request.')


module_list['Ladder'] = f'{my_prefix()}ladder [text]'
file_list['Ladder'] = 'ladder.py'
