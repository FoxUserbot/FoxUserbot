import asyncio
import datetime
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from plugins.settings.main_settings import module_list, file_list, settings

prefix = settings['prefix']

async def afk_handler(client: Client, message: Message):
    try:
        global start, end
        end = datetime.datetime.now().replace(microsecond=0)
        afk_time = end - start

        if message.from_user.is_bot is False:
            await message.reply_text(f"❕ Данный пользователь <b>AFK</b>.\n" f"<b>💬 Причина:</b> {reason}.\n" f"<b>⏳Длительность</b>: {afk_time}.")
    except NameError:
        pass


@Client.on_message(filters.command("afk", prefixes=prefix) & filters.me)
async def afk(client: Client, message: Message):
    try:
        global start, end, handler, reason
        start = datetime.datetime.now().replace(microsecond=0)
        handler = client.add_handler(
            MessageHandler(afk_handler, (filters.private & ~filters.me | filters.group & filters.mentioned & ~filters.me)))
        if len(message.text.split()) >= 2:
            reason = message.text.split(" ", maxsplit=1)[1]
        else:
            reason = "Неизвестно"
        await message.edit(f"❕ Вход в <b>AFK режим</b>.\n<b>💬 Причина:</b> {reason}.\n")
    except Exception as f:
        await message.edit(f"error {f}")

# No AFK
@Client.on_message(filters.command("unafk", prefixes=prefix) & filters.me)
async def unafk(client: Client, message: Message):
    try:
        global start, end
        end = datetime.datetime.now().replace(microsecond=0)
        afk_time = end - start
        await message.edit(
            f"❕ | Пользователь вышел с <b>AFK режима.</b> \n💬 Причина <b>AFK режима:</b> {reason}\n⏳ Длительность <b>AFK:</b> {afk_time}"
        )
        client.remove_handler(*handler)
    except Exception as error:
        await message.edit("<b>Я не был в АФК</b>")
        await asyncio.sleep(3)
        await message.delete()
        
module_list['AFK'] = f'{prefix}afk | {prefix}unafk'
file_list['AFK'] = 'afk.py'