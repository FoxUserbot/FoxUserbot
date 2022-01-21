from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.settings.main_settings import module_list, file_list

from prefix import my_prefix
prefix = my_prefix()

@Client.on_message(filters.command('send_log', prefixes=prefix) & filters.me)
async def send_log(client: Client, message: Message):
	chat = message.chat.id
	await message.delete()
	await client.send_document(chat, "fox_userbot.log")

module_list['SendLog'] = f'{prefix}send_log'