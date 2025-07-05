from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix
import requests
import io


@Client.on_message(filters.command("webshot", prefixes=my_prefix()) & filters.me)
async def webshot(client, message):
    try:
        user_link = (message.command[1].replace("https://", "").replace("http://", ""))
        await message.edit("Try create screenshot...")
        full_link = f"https://mini.s-shot.ru/1920x1080/JPEG/1024/Z100/?{user_link}"
        try:
            response = requests.get(full_link)
            if response.status_code == 200:
                response.raise_for_status() 
                image_bytes = io.BytesIO(response.content)
                image_bytes.name = "webshot.jpg"
                image_bytes.seek(0)
                await client.send_photo(message.chat.id, image_bytes, caption=f"**Screenshot of the page ⟶** {user_link}")
            else:
                await message.edit(f"**Error:** {response.status_code}")
        except requests.exceptions.RequestException as e:
            await message.edit(f"**Error:** {e}")
            return 
        except Exception as error:
            await message.edit(f"**Error:** {error}")
            return 

    except IndexError:
        await message.edit("Don't have link!")
    except Exception as error:
        await message.edit(f"**Error:** {error}")
