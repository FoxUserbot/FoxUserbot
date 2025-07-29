from pyrogram import Client, filters
from command import fox_command
import os


@Client.on_message(fox_command(command1="id", Module_Name="FindIDThisChat", names=os.path.basename(__file__)) & filters.me)
async def find_id(client, message):
    if message.reply_to_message is None:
        await message.edit(f"Chat ID: `{message.chat.id}`")
    else:
        await message.edit(f"User ID: `{message.reply_to_message.from_user.id}`\nChat ID: `{message.chat.id}`")
