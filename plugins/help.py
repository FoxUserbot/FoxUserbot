from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.settings.main_settings import module_list, settings, requirements_list, version
import asyncio
from telegraph import Telegraph

prefix = settings['prefix']

@Client.on_message(filters.command('help', prefixes=prefix) & filters.me)
async def help(client: Client, message: Message):
    list = []
    for k, v in module_list.items():
        list.append(f'• {k}: {v}<br>')
    a = " "
    for i in list:
        a = a.lstrip() + f'{i}'
    help = f"""
{len(module_list)} available modules.<br>
<br>
{a}
"""
    await message.edit('Loading the help menu. Please, wait...')
    telegraph = Telegraph()
    telegraph.create_account(short_name='FoxServices')
    link = f"https://telegra.ph/{telegraph.create_page('FoxUserbot Help.', html_content=f'{help}')['path']}"
    await message.edit(f"""
<b>🚑 | Help menu. </b>
<b>🔒 | Version: {version}</b>

<b><a href={link}>❓ | List of all commands. </a></b>
<b><a href="https://t.me/foxteam0">💻 | Official FoxTeam Channel.</a></b>
<b><a href="https://t.me/foxteamchat">🛡 | Official User Support Chat.</a></b>
<b><a href="https://github.com/gh0stc0der1/FoxUserbot">⛔️ | Github Repository.</a></b>
<b><a href="https://telegra.ph/Kak-ustanovit-FoxUserbot-01-20">🤔 | Installation Guide.</a></b>

❤️ | Thanks for using FoxUserbot.
❤️ | If you find a malfunction, write to the support chat.""", disable_web_page_preview=True)

module_list['Help'] = f'{prefix}help'
requirements_list.append('telegraph')
