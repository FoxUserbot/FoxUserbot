from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list

from prefix import my_prefix



i = filters.user([])


@Client.on_message(i & ~filters.me)
async def ignored(client, message):
    await message.delete()


@Client.on_message(filters.command("ignore", prefixes=my_prefix()) & filters.me)
async def add_ignore(client, message):
    try:
        users = message.command[1]
    except:
        users = message.reply_to_message.from_user.id


    if users in i:
        i.remove(int(users))
        await message.edit(f"`{str(users)}` no longer ignored")
    else:
        i.add(int(users))
        await message.edit(f"`{str(users)}` ignored")


module_list['IgnoreUser'] = f'{my_prefix()}ignore [ID/Reply]'
file_list['IgnoreUser'] = 'ignore.py'
