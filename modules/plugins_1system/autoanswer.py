from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

import os
from pathlib import Path


def users():
    ignore = []
    i = os.listdir("temp/autoanswer_DB")
    for list in i:
        ignore.append(int(list))
    return ignore



@Client.on_message(filters.private & ~filters.me & ~filters.bot)
async def aws(client, message):
    ids = message.from_user.id
    if Path(f"./temp/autoanswer").is_file():
        if not ids in users():
            with open(f"./temp/autoanswer", encoding="utf-8") as f:
                fromuser = str(ids)
                status = f.read().split()
                chat_ids = status[0]
                message_ids = status[1]
                await client.forward_messages(message.chat.id, str(chat_ids), int(message_ids))
                with open(f"temp/autoanswer_DB/{fromuser}", "w+", encoding='utf-8') as w:
                    w.write(str(f"0"))
                    w.close()
            f.close()
    else:
        pass


@Client.on_message(filters.command("aws", prefixes=my_prefix()) & filters.me)
async def aws_start(client, message):
    try:
        chat_ids = message.text.split()[1]
        message_ids = message.text.split()[2]
        await message.edit(f"❕ AutoAnswer activated!.\n<b>💬 Chat id/tag:</b> {chat_ids}\n🆔 Message id: {message_ids}")
        with open(f"temp/autoanswer", "w+", encoding='utf-8') as f:
            f.write(str(f"{chat_ids} {message_ids}"))
            f.close()
    except Exception as f:
        await message.edit(f"error {f}")


module_list['AutoAnswer'] = f'{my_prefix()}aws [ID/Username] [Post ID]'
file_list['AutoAnswer'] = 'autoanswer.py'
