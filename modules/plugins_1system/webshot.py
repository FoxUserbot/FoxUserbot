from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix


@Client.on_message(filters.command("webshot", prefixes=my_prefix()) & filters.me)
async def webshot(client, message):
    try:
        user_link = (message.command[1])
        await message.edit("Try create screenshot...")
        full_link = f"https://mini.s-shot.ru/1920x1080/JPEG/1024/Z100/?{user_link.replace('https://', '')}"
        await client.send_photo(message.chat.id, full_link, caption=f"**Screenshot of the page ⟶** {user_link}")
        await message.delete()
    except Exception as error:
        await message.delete()
        await client.send_message(
            message.chat.id, f"**Something went wrong\n\nLog:{error}...**"
        )


module_list['Webshot'] = f'{my_prefix()}webshot [link]'
file_list['Webshot'] = 'webshot.py'
