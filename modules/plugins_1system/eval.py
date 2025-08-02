from pyrogram import Client, filters
from command import fox_command
import os
import sys
from io import StringIO

@Client.on_message(fox_command("eval", "Eval", os.path.basename(__file__), "[code/reply]") & filters.me)
def user_exec(client, message):
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

        message.edit(
            f"<emoji id='5300928913956938544'>👩‍💻</emoji> <b>Code:</b>\n"
            f"<code>{code}</code>\n\n"
            f"<emoji id='5447410659077661506'>🌐</emoji> <b>Result</b>:\n"
            f"<code>{result.getvalue()}</code>"
        )
    except:
        message.edit(
            f"<emoji id='5300928913956938544'>👩‍💻</emoji> <b>Code:</b>\n"
            f"<code>{code}</code>\n\n"
            f"<emoji id='5447410659077661506'>🌐</emoji> <b>Result</b>:\n"
            f"<code>{sys.exc_info()[0].__name__}: {sys.exc_info()[1]}</code>"
        )
