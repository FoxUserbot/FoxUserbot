from pyrogram import Client, filters
from pyrogram.enums import ChatType
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

from datetime import datetime
import asyncio


@Client.on_message(filters.command(["stat", "stats"], prefixes=my_prefix()) & filters.me)
async def stats(client, message):
    await message.edit("Parsing stats...")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0
    group = ["supergroup", "group"]
    iter_dialog = client.get_dialogs()
    async for dialog in iter_dialog:
        if dialog.chat.type == ChatType.PRIVATE:
            u += 1
        elif dialog.chat.type == ChatType.BOT:
            b += 1
        elif dialog.chat.type == ChatType.GROUP:
            g += 1
        elif dialog.chat.type == ChatType.SUPERGROUP:
            sg += 1
            user_s = await dialog.chat.get_member(int(client.me.id))
            if user_s.status in ("creator", "administrator"):
                a_chat += 1
        elif dialog.chat.type == ChatType.CHANNEL:
            c += 1
    end = datetime.now()
    ms = (end - start).seconds

    private_chat = f"**Privates:** {u}\n"
    group_chat = f"**Groups:** {g}\n"
    supergroup_chat = f"**Supergroups:** {sg}\n"
    channel_chat = f"**Channels:** {c}\n"
    bot_chat = f"**Bots:** {b}\n"
    owner_chat = f"**Creators:** {a_chat}"
    statistic = private_chat + group_chat + supergroup_chat + channel_chat + bot_chat + owner_chat
    await message.edit(f"You stats:\n{statistic}\nParsed {ms} seconds")


module_list['Statistic'] = f'{my_prefix()}stats'
file_list['Statistic'] = 'stats.py'