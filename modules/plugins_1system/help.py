from pyrogram import Client, filters, __version__
from pyrogram.errors import ChatSendPhotosForbidden
from modules.plugins_1system.settings.main_settings import module_list, version
from prefix import my_prefix

from telegraph import Telegraph
from platform import python_version
import random


def get_text(message):
    lists = []
    for k, v in module_list.items():
        lists.append(f'➣ Module [{k}] - Command: {v}<br>')
    a = " "
    for i in lists:
        a = a.lstrip() + f'{i}'
    helpes = f"""
{len(module_list)} available modules.<br>
<br>
{a}
"""
    telegraph = Telegraph()
    telegraph.create_account(short_name='FoxServices')
    link = f"https://telegra.ph/{telegraph.create_page(f'FoxUserbot Help {random.randint(10000, 99999)}', html_content=f'{helpes}')['path']}"
    if message.from_user.is_premium:
        return f"""
<emoji id="5190875290439525089">😊</emoji><b> | FoxUserbot RUNNING</b>
<emoji id="5197288647275071607">🛡</emoji><b> | Version: </b><b>{version}</b>
<emoji id="5193177581888755275">💻</emoji><b> | Modules: {len(module_list)}</b>
<emoji id="5444856076954520455">🧾</emoji><b> | Prefix: {my_prefix()}</b>
<emoji id="5436113877181941026">❓</emoji><a href="{link}"><b> | List of all commands. </b></a>

"""
    else:
        return f"""
<b>🦊 | FoxUserbot RUNNING</b>
<b>🔒 | Version: {version}</b>
<b>💼 | Modules: {len(module_list)}</b>
<b>🔒 | Prefix: {my_prefix()}</b>
<b><a href={link}>❓ | List of all commands. </a></b>

"""



@Client.on_message(filters.command('help', prefixes=my_prefix()) & filters.me)
async def helps(client, message):
    try:
        await message.delete()
        da = await client.send_photo(message.chat.id, "https://raw.githubusercontent.com/FoxUserbot/FoxUserbot/refs/heads/main/photos/userbot_info.png", caption="Loading the help menu. Please, wait...", message_thread_id=message.message_thread_id)
        await client.edit_message_caption(message.chat.id, da.id, get_text(message))
    except ChatSendPhotosForbidden:
        await message.delete()
        await client.send_message(message.chat.id, get_text(message), message_thread_id=message.message_thread_id)


module_list['Help'] = f'{my_prefix()}help'
