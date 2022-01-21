from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.settings.main_settings import module_list, file_list, settings, requirements_list
import asyncio

prefix = settings['prefix']

def get_pic(city):
    file_name = f"{city}.png"
    with open(file_name, "wb") as pic:
        response = requests.get("http://wttr.in/{citys}_2&lang=ru.png", stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            pic.write(block)
        return file_name


@Client.on_message(filters.command("weather", prefixes=prefix) & filters.me)
async def weather(client: Client, message: Message):
    city = message.command[1]
    await message.edit("🕑 Просматриваю погоду в вашей стране")
    r = requests.get(f"https://wttr.in/{city}?m?M?0?q?T&lang=ru")
    await message.edit(f"🗺 Ваш город : {r.text}")
    await app.send_photo(
        chat_id=message.chat.id,
        photo=get_pic(city),
        reply_to_message_id=message.message_id)
    os.remove(f"{city}.png")

module_list['Weather'] = f'{prefix}weather [city]'
file_list['Weather'] = 'weather.py'