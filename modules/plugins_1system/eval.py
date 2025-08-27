from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
import os
import sys
from io import StringIO

@Client.on_message(fox_command("eval", "Eval", os.path.basename(__file__), "[code/reply]") & fox_sudo())
async def user_exec(client, message):
    message = await who_message(client, message, message.reply_to_message)
    reply = message.reply_to_message
    code = ""
    try:
        code = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        try:
            code = message.text.split(" \n", maxsplit=1)[1]
        except IndexError:
            pass

    result = sys.stdout = StringIO()
    try:
        exec(code)
        await message.edit(
            f"<emoji id='5300928913956938544'>👩‍💻</emoji> <b>Code:</b>\n"
            f"<code>{code}</code>\n\n"
            f"<emoji id='5447410659077661506'>🌐</emoji> <b>Result</b>:\n"
            f"<code>{result.getvalue()}</code>"
        )
    except Exception as e:
        await message.edit(
            f"<emoji id='5300928913956938544'>👩‍💻</emoji> <b>Code:</b>\n"
            f"<code>{code}</code>\n\n"
            f"<emoji id='5447410659077661506'>🌐</emoji> <b>Result</b>:\n"
            f"<code>{type(e).__name__}: {str(e)}</code>"
        )
