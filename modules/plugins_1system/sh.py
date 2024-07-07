from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

from subprocess import Popen, PIPE, TimeoutExpired
from time import perf_counter
import random
import os


@Client.on_message(filters.command(["shell", "sh"], prefixes=my_prefix()) & filters.me)
async def example_edit(client, message):
    if not message.reply_to_message and len(message.command) == 1:
        return await message.edit(
            "<b>Specify the command in message text or in reply</b>"
        )
    cmd_text = (
        message.text.split(maxsplit=1)[1]
        if message.reply_to_message is None
        else message.reply_to_message.text
    )
    cmd_obj = Popen(cmd_text, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    await message.edit("<b>Running...</b>")
    text = f"$ <code>{cmd_text}</code>\n\n"
    try:
        start_time = perf_counter()
        stdout, stderr = cmd_obj.communicate(timeout=60)
    except TimeoutExpired:
        text += "<b>Timeout expired (60 seconds)</b>"
    else:
        stop_time = perf_counter()
        if stdout:
            stdout_output = f"{stdout}"
            text += "<b>Output:</b>\n" f"<code>{stdout}</code>\n"
        else:
            stdout_output = ""

        if stderr:
            stderr_output = f"{stderr}"
            text += "<b>Error:</b>\n" f"<code>{stderr}</code>\n"
        else:
            stderr_output = ""

        time = round(stop_time - start_time, 3) * 1000
        text += f"<b>Completed in {time} miliseconds with code {cmd_obj.returncode}</b> "

    try:
        await message.edit(text)
    except:
        output = f"{stdout_output}\n\n{stderr_output}"
        command = f"{cmd_text}"

        await message.edit("Result too much, send with document...")

        i = random.randint(1, 9999)
        with open(f"temp/result{i}.txt", "w") as file:
            file.write(f"{output}")

        try:
            await client.send_document(message.chat.id, f"temp/result{i}.txt", caption=f"<code>{command}</code>")
            await message.delete()
        except:
            await client.send_document(message.chat.id, f"temp/result{i}.txt", caption="Result")
            await message.edit(f"<code>{command}</code>")
        os.remove(f"result{i}.txt")
    cmd_obj.kill()


module_list['Sh'] = f'{my_prefix()}sh'
file_list['Sh'] = 'sh.py'
