from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, version
from command import fox_command
import os
from telegraph import Telegraph
import random
import configparser
from pathlib import Path

# Default
DEFAULT_HELP_IMAGE = "https://raw.githubusercontent.com/FoxUserbot/FoxUserbot/main/photos/foxuserbot_info.jpg"
THEME_PATH = "userdata/theme.ini"

def get_help_image():
    if not Path(THEME_PATH).exists():
        return DEFAULT_HELP_IMAGE

    try:
        config = configparser.ConfigParser()
        config.read(THEME_PATH)
        return config.get("help", "image", fallback=DEFAULT_HELP_IMAGE)
    except:
        return DEFAULT_HELP_IMAGE


def get_help_text(message):
    from prefix import my_prefix
    lists = []
    for module_name, commands in module_list.items():
        text = ""
        if isinstance(commands, list):
            for i in commands:
                text += f"{i} | "
            text = text[:-2]
            commands = text
        command_list = [cmd.strip() for cmd in commands.split("|")]

        module_block = [
            f"➣ Module <b>[{module_name}]</b>",
            *[f"Command: <code>{cmd}</code>" for cmd in command_list],
            "" 
        ]
        lists.extend(module_block)

    a = "<br>".join(lists)
    
    
    telegraph = Telegraph()
    telegraph.create_account(short_name='FoxServices')
    link = f"https://telegra.ph/{telegraph.create_page(f'FoxUserbot Help {random.randint(10000, 99999)}', html_content=f'{a}')['path']}"
    
    custom_text = None
    if Path(THEME_PATH).exists():
        try:
            config = configparser.ConfigParser()
            config.read(THEME_PATH)
            custom_text = config.get("help", "text", fallback=None)
            if custom_text and custom_text.strip() and custom_text != "Not set":
                aliases = {
                    '{version}': version,
                    '{modules_count}': str(len(module_list)),
                    '{prefix}': my_prefix(),
                    '{commands_link}': link,
                }
                for alias, value in aliases.items():
                    custom_text = custom_text.replace(alias, str(value))
                return custom_text
        except Exception as e:
            pass
    
    if message.from_user.is_premium:
        return f"""
<emoji id="5190875290439525089">😊</emoji><b> | FoxUserbot RUNNING</b>
<emoji id="5197288647275071607">🛡</emoji><b> | Version: </b><b>{version}</b>
<emoji id="5193177581888755275">💻</emoji><b> | Modules: {len(module_list)}</b>
<emoji id="5444856076954520455">🧾</emoji><b> | Prefix: {my_prefix()}</b>
<emoji id="5436113877181941026">❓</emoji><a href="{link}"><b> | List of all commands. </b></a>
"""
    else:
        return f"""
<b>🦊 | FoxUserbot RUNNING</b>
<b>🔒 | Version: {version}</b>
<b>💼 | Modules: {len(module_list)}</b>
<b>🔒 | Prefix: {my_prefix()}</b>
<b><a href={link}>❓ | List of all commands. </a></b>
"""

@Client.on_message(fox_command(command1="help", Module_Name="Help", names=os.path.basename(__file__)) & filters.me)
async def helps(client, message):
    try:
        image_url = get_help_image()
        da = await client.send_photo(
            message.chat.id, 
            photo=image_url, 
            caption="Loading the help menu...", 
            message_thread_id=message.message_thread_id
        )
        await message.delete()
        caption = get_help_text(message)
        await client.edit_message_caption(message.chat.id, da.id, caption)
    except:
        try:
            da = await client.send_photo(
                message.chat.id, 
                photo=DEFAULT_HELP_IMAGE, 
                caption="Loading the help menu...", 
                message_thread_id=message.message_thread_id
            )
            await message.delete()
            caption = get_help_text(message)
            await client.edit_message_caption(message.chat.id, da.id, caption)
        except:
            try:
                da = await client.send_photo(
                    message.chat.id, 
                    photo="photos/foxuserbot_info.jpg", 
                    caption="Loading the help menu...", 
                    message_thread_id=message.message_thread_id
                )
                await message.delete()
                caption = get_help_text(message)
                await client.edit_message_caption(message.chat.id, da.id, caption)
            except:
                await message.edit("Loading the help menu...")
                await message.edit(get_help_text(message))
