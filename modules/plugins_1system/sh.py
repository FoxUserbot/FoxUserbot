import os
import random
from subprocess import PIPE, Popen, TimeoutExpired
from time import perf_counter

from pyrogram import Client

from command import fox_command, fox_sudo, who_message


@Client.on_message(fox_command(["shell", "sh"], "Shell", os.path.basename(__file__), "[command/reply]") & fox_sudo())
async def shell(client, message):
    message = await who_message(client, message)
    if not message.reply_to_message and (len(message.text.split()) == 1):
        return await message.edit(
            "<emoji id='5210952531676504517'>❌</emoji> <b>Specify the command in message text or in reply</b>"
        )
    cmd_text = (
        " ".join(message.text.split()[1:])
        if message.text and len(message.text.split()) > 1
        else (
            message.reply_to_message.text
            if message.reply_to_message and message.reply_to_message.text
            else None
        )
    )
    if cmd_text is None: cmd_text = " ".join(message.text.split()[1:])
    cmd_obj = Popen(cmd_text, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    await message.edit("<emoji id='5264727218734524899'>🔄</emoji> <b>Running...</b>")
    text = f"$ <code>{cmd_text}</code>\n\n"
    try:
        start_time = perf_counter()
        stdout, stderr = cmd_obj.communicate(timeout=60)
    except TimeoutExpired:
        text += "<emoji id='5210952531676504517'>❌</emoji> <b>Timeout expired (60 seconds)</b>"
    else:
        stop_time = perf_counter()
        if stdout:
            stdout_output = f"{stdout}"
            text += "<emoji id='5447410659077661506'>🌐</emoji> <b>Output:</b>\n" f"""```
{stdout}
```\n"""
        else:
            stdout_output = ""

        if stderr:
            stderr_output = f"{stderr}"
            text += "<emoji id='5210952531676504517'>❌</emoji> <b>Error:</b>\n" f"""```
{stderr}
```\n"""
        else:
            stderr_output = ""

        time = round(stop_time - start_time, 3) * 1000
        text += f"<emoji id='5237699328843200968'>✅</emoji> <b>Completed in {time} miliseconds with code {cmd_obj.returncode}</b> "

    try:
        await message.edit(text)
    except:
        output = f"{stdout_output}\n\n{stderr_output}"
        command = f"{cmd_text}"

        await message.edit("<emoji id='5411225014148014586'>🔴</emoji> <b>Result too much, send with document...</b>")

        i = random.randint(1, 9999)
        with open(f"temp/result{i}.txt", "w") as file:
            file.write(f"{output}")

        try:
            await client.send_document(message.chat.id, f"temp/result{i}.txt", caption=f"<code>{command}</code>" , message_thread_id=message.message_thread_id)
            await message.delete()
        except:
            await client.send_document(message.chat.id, f"temp/result{i}.txt", caption="Result" , message_thread_id=message.message_thread_id)
            await message.edit(f"<code>{command}</code>")
        os.remove(f"result{i}.txt")
    cmd_obj.kill()


