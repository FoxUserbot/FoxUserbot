from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

import asyncio


@Client.on_message(filters.command("tagallone", prefixes=my_prefix()) & filters.me)
async def tagallone(client, message):
    try:
        delay = message.command[1]
    except:
        delay = 0

    if len(message.text.split()) >= 2:
        text = f'{message.text.split(my_prefix() + "tagallone " + delay, maxsplit=1)[1]}'
    else:
        text = ""

    await message.edit("Loading...")
    chat_id = message.chat.id
    gg = client.get_chat_members(chat_id)

    await message.delete()
    async for member in gg:
        string = f"{member.user.mention('*')} "
        await client.send_message(chat_id, text=(f"||{string}|| | {text}"), disable_web_page_preview=True)
        try:
            delay = int(delay)
        except ValueError:
            delay = float(delay)
        await asyncio.sleep(delay)



@Client.on_message(filters.command("tagall", prefixes=my_prefix()) & filters.me)
async def tagall(client, message):
    maxTag = 5

    try:
        delay = message.command[1]
    except:
        delay = 0

    if len(message.text.split()) >= 2:
        text = f'{message.text.split(my_prefix() + "tagall " + delay, maxsplit=1)[1]}'
    else:
        text = ""

    await message.edit("Loading...")
    icm = []
    chat_id = message.chat.id

    gg = client.get_chat_members(chat_id)
    async for member in gg:
        icm.append(member)

    useres = len(icm)
    limit = 0
    i = useres // maxTag
    g = useres % maxTag
    l = 0
    string = ""

    await message.delete()
    for member in icm:
        if int(l) == int(i):
            if int(limit) == (g - 1):
                await client.send_message(chat_id, text=(f"{text}\n||{string}||"), disable_web_page_preview=True)
                string = ""
                limit = 0
            else:
                string += f"{member.user.mention('*')} "
                limit += 1

        else:
            if limit < maxTag:
                string += f"{member.user.mention('*')} "
                limit += 1
            else:
                await client.send_message(chat_id, text=(f"{text}\n||{string}||"), disable_web_page_preview=True)
                string = ""
                limit = 0
                l += 1

        try:
            delay = int(delay)
        except ValueError:
            delay = float(delay)
        await asyncio.sleep(delay)


module_list['Tagall'] = f'{my_prefix()}tagall [delay] [text] | {my_prefix()}tagallone [delay] [text]'
file_list['Tagall'] = 'tagall.py'
