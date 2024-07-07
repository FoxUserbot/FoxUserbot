from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

import requests
import os


def get_pic(city):
    city = city.lower()
    file_name = f"{city}.png"
    with open(file_name, "wb") as pic:
        response = requests.get(f"http://wttr.in/{city}_2&lang=en.png", stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            pic.write(block)
        return file_name


@Client.on_message(filters.command("weather", prefixes=my_prefix()) & filters.me)
async def weather(client, message):
    city = message.command[1]
    await message.edit("Check weather...")
    r = requests.get(f"https://wttr.in/{city}?m?M?0?q?T&lang=en")
    await message.edit(f"🗺 You sity/village: {city}\n{r.text}")
    await client.send_photo(
        chat_id=message.chat.id,
        photo=get_pic(city),
        reply_to_message_id=message.id)
    os.remove(f"{city}.png")


module_list['Weather'] = f'{my_prefix()}weather [city]'
file_list['Weather'] = 'weather.py'
