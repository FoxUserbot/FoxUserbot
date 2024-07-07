from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix


@Client.on_message(filters.command("send", prefixes=my_prefix()) & filters.me)
async def sendtoid(client, message):
    await client.unblock_user(message.command[1])
    await client.send_message(message.command[1], "Hi")
    await message.edit(f"Message send to {message.command[1]}")


module_list['SendToId'] = f'{my_prefix()}send [ID | Username]'
file_list['SendToId'] = 'SendToId.py'
