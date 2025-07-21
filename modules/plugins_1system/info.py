from pyrogram import Client, filters , __version__
from pyrogram.errors import WebpageMediaEmpty , ChatSendPhotosForbidden
from modules.plugins_1system.settings.main_settings import module_list, file_list 
from prefix import my_prefix
from platform import python_version
import configparser
from pathlib import Path


# Default
DEFAULT_INFO_IMAGE = "https://raw.githubusercontent.com/FoxUserbot/FoxUserbot/refs/heads/main/photos/system_info.jpg"
THEME_PATH = "userdata/theme.ini"


def get_info_image():
    if not Path(THEME_PATH).exists():
        return DEFAULT_INFO_IMAGE

    try:
        config = configparser.ConfigParser()
        config.read(THEME_PATH)
        return config.get("info", "image_url", fallback=DEFAULT_INFO_IMAGE)
    except:
        return DEFAULT_INFO_IMAGE


def get_info_text(message):
    if message.from_user.is_premium:
        return f"""
<emoji id="5190875290439525089">😊</emoji><b> | FoxUserbot INFO</b>
<emoji id="5372878077250519677">📱</emoji><b> | Python: {python_version()}</b>
<emoji id="5190637731503415052">🦊</emoji><b> | Kurigram: {__version__}</b>
    
<emoji id="5330237710655306682">📱</emoji><a href="https://t.me/foxteam0"><b> | Official FoxTeam Channel.</b></a>
<emoji id="5346181118884331907">📱</emoji><a href="https://github.com/FoxUserbot/FoxUserbot"><b> | Github Repository.</b></a>
<emoji id="5379999674193172777">🔭</emoji><a href="https://github.com/FoxUserbot/FoxUserbot#how-to-install"><b> | Installation Guide.</b></a>
    
<emoji id=5350554349074391003>💻</emoji> | <b>Developers:</b>
<emoji id="5330237710655306682">📱</emoji> | <a href="https://t.me/a9_fm">A9FM</a>
<emoji id="5330237710655306682">📱</emoji> | <a href="https://t.me/ArThirtyFour">ArThirtyFour</a>

<emoji id="5359480394922082925">📱</emoji> | <b>Designer:</b>
<emoji id="5330237710655306682">📱</emoji> | <a href="https://t.me/nw_off">Nw_Off</a>
    """
    else:
        return f"""
<b>🦊 | FoxUserbot INFO</b>
<b>🐍 | Python: {python_version()}</b>
<b>🥧 | Kurigram: {__version__}</b>

<b><a href="https://t.me/foxteam0">💻 | Official FoxTeam Channel.</a></b>
<b><a href="https://github.com/FoxUserbot/FoxUserbot">🐈‍⬛ | Github Repository.</a></b>
<b><a href="https://github.com/FoxUserbot/FoxUserbot#how-to-install">🤔 | Installation Guide.</a></b>

💻 | <b>Developers:</b>
📞 | <a href="https://t.me/a9_fm">A9FM</a>
📞 | <a href="https://t.me/ArThirtyFour">ArThirtyFour</a>

<b>🖼 | <b>Designer:</b>
📞 | <a href="https://t.me/nw_off">Nw_Off</a>
    """


@Client.on_message(filters.command('info', prefixes=my_prefix()) & filters.me)
async def info(client, message):
    try:
        image_url = get_info_image()
        da = await client.send_photo(
            message.chat.id, 
            photo=image_url, 
            caption="Loading the info...", 
            message_thread_id=message.message_thread_id
        )
        await message.delete()
        caption = get_info_text(message)
        await client.edit_message_caption(message.chat.id, da.id, caption)
    except:
        try:
            da = await client.send_photo(
                message.chat.id, 
                photo=DEFAULT_INFO_IMAGE, 
                caption="Loading the info...", 
                message_thread_id=message.message_thread_id
            )
            await message.delete()
            caption = get_info_text(message)
            await client.edit_message_caption(message.chat.id, da.id, caption)
        except:
            try:
                da = await client.send_photo(
                    message.chat.id, 
                    photo="photos/system_info.jpg", 
                    caption="Loading the info...", 
                    message_thread_id=message.message_thread_id
                )
                await message.delete()
                caption = get_info_text(message)
                await client.edit_message_caption(message.chat.id, da.id, caption)
            except:
                await message.edit("Loading the info...")
                await message.edit(get_info_text(message))


module_list['Info'] = f'{my_prefix()}info'
