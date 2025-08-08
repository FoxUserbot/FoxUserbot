from pyrogram import Client
from command import fox_command, fox_sudo, who_message
import os


@Client.on_message(fox_command("id", "FindIDThisChat", os.path.basename(__file__)) & fox_sudo())
async def find_id(client, message):
    message = await who_message(client, message)
    if message.reply_to_message is None:
        await message.edit(f"<emoji id='5974526806995242353'>🆔</emoji> Chat ID: `{message.chat.id}`")
    else:
        await message.edit(f"<emoji id='5974526806995242353'>🆔</emoji> User ID: `{message.reply_to_message.from_user.id}`\n<emoji id='5974526806995242353'>🆔</emoji> Chat ID: `{message.chat.id}`")

