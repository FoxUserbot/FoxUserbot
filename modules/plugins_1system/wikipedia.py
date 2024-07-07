from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

import wikipedia


@Client.on_message(filters.command("wiki", prefixes=my_prefix()) & filters.me)
async def wiki(client, message):
    lang = message.command[1]
    user_request = " ".join(message.command[2:])
    await message.edit("<b>Search info</b>")
    if user_request == "":
        wikipedia.set_lang("en")
        user_request = " ".join(message.command[1:])
    try:
        if lang == "ru":
            wikipedia.set_lang("ru")

        result = wikipedia.summary(user_request)
        await message.edit(
            f"""<b>Слово:</b>
<code>{user_request}</code>

<b>Info:</b>
<code>{result}</code>"""
        )
    except Exception as exc:
        await message.edit(
            f"""<b>Request:</b>
<code>{user_request}</code>
<b>Result:</b>
<code>{exc}</code>"""
        )


module_list['Wikipedia'] = f'{my_prefix()}wiki [RU/EN] [WORD]'
file_list['Wikipedia'] = 'wiki.py'
