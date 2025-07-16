from pyrogram import Client, filters , __version__
from pyrogram.enums import ParseMode # Import ParseMode
from modules.plugins_1system.settings.main_settings import module_list, file_list , version
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from prefix import my_prefix
from platform import python_version

def get_info(message):
    if message.from_user.is_premium:
        return f"""
<emoji id="5190875290439525089">😊</emoji><b> | FoxUserbot INFO</b>
<emoji id="5372878077250519677">📱</emoji><b> | Python: {python_version()}</b>
<emoji id="5190637731503415052">🦊</emoji><b> | Kurigram: {__version__}</b>
    
<emoji id="5330237710655306682">📱</emoji><a href="https://t.me/foxteam0"><b> | Official FoxTeam Channel.</b></a>
<emoji id="5346181118884331907">📱</emoji><a href="https://github.com/FoxUserbot/FoxUserbot"><b> | Github Repository.</b></a>
<emoji id="5379999674193172777">🔭</emoji><a href="https://github.com/FoxUserbot/FoxUserbot#how-to-install"><b> | Installation Guide.</b></a>
    
<emoji id=5350554349074391003>💻</emoji> | Developers:
<emoji id="5330237710655306682">📱</emoji> | <a href="https://t.me/a9_fm">A9FM</a>
<emoji id="5330237710655306682">📱</emoji> | <a href="https://t.me/ArThirtyFour">ArThirtyFour</a>

<emoji id="5359480394922082925">📱</emoji> | <b>Designer:</b>
<b><a href="https://t.me/nw_off">Nw_Off</a></b>
    """
    else:
        return f"""
<b>🦊 | FoxUserbot INFO</b>
<b>🐍 | Python: {python_version()}</b>
<b>🥧 | Kurigram: {__version__}</b>

<b><a href="https://t.me/foxteam0">💻 | Official FoxTeam Channel.</a></b>
<b><a href="https://github.com/FoxUserbot/FoxUserbot">🐈‍⬛ | Github Repository.</a></b>
<b><a href="https://github.com/FoxUserbot/FoxUserbot#how-to-install">🤔 | Installation Guide.</a></b>
<b>Developers:</b>
<b>📞 | <a href="https://t.me/a9_fm">A9FM</a></b>
<b>📞 | <a href="https://t.me/ArThirtyFour">ArThirtyFour</a></b>

<b>📞 | <b>Designer:</b>
<b><a href="https://t.me/nw_off">Nw_Off</a></b>
    """


@Client.on_message(filters.command('info', prefixes=my_prefix()) & filters.me)
async def info(client, message):
    await message.delete()
    await client.send_photo(
        chat_id=message.chat.id,
        photo="https://raw.githubusercontent.com/FoxUserbot/FoxUserbot/refs/heads/main/photos/info_banner.jpg",
        caption=get_info(message),
        message_thread_id=message.message_thread_id
    )


module_list['Info'] = f'{my_prefix()}info'
file_list['Info'] = 'info.py'
