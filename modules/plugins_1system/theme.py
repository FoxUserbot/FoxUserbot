from pyrogram import Client, filters
from pyrogram.types import Message
import configparser
import os
from pathlib import Path
from modules.plugins_1system.settings.main_settings import module_list
from prefix import my_prefix

THEME_PATH = "userdata/theme.ini"


@Client.on_message(filters.command('theme', prefixes=my_prefix()) & filters.me)
async def theme_command(client, message):
    if len(message.command) < 2:
        text = ""
        if Path(THEME_PATH).exists():
            config = configparser.ConfigParser()
            config.read(THEME_PATH)
            url = config.get("help", "image_url", fallback="Not set")
            text += f"🦊 Current help image: `{url}`\n"
            url = config.get("info", "image_url", fallback="Not set")
            text += f"🦊 Current info image: `{url}`\n"
        else:
            text += "🦊 Using default image\n"

        await message.edit(text)
        return
        
    if message.command[1] == "help":
        if message.command[2] == "set":
            if len(message.command) < 4:
                await message.edit("**Usage:** `.theme help set [image_url]`")
                return
                
            os.makedirs(os.path.dirname(THEME_PATH), exist_ok=True)
            config = configparser.ConfigParser()
            
            if Path(THEME_PATH).exists():
                config.read(THEME_PATH)
            
            if not config.has_section("help"):
                config.add_section("help")
                
            config.set("help", "image_url", message.command[3])
            
            with open(THEME_PATH, 'w') as f:
                config.write(f)
                
            await message.edit("✅ Help image updated")
        
        elif message.comman[2] == "reset":
            if Path(THEME_PATH).exists():
                os.remove(THEME_PATH)
            await message.edit("✅ Theme reset to default")
    elif message.command[1] == "info":
        if message.command[2] == "set":
            if len(message.command) < 4:
                await message.edit("**Usage:** `.theme info set [image_url]`")
                return
                
            os.makedirs(os.path.dirname(THEME_PATH), exist_ok=True)
            config = configparser.ConfigParser()
            
            if Path(THEME_PATH).exists():
                config.read(THEME_PATH)
            
            if not config.has_section("info"):
                config.add_section("info")
                
            config.set("info", "image_url", message.command[3])
            
            with open(THEME_PATH, 'w') as f:
                config.write(f)
                
            await message.edit("✅ Info image updated")
        
        elif message.comman[2] == "reset":
            if Path(THEME_PATH).exists():
                os.remove(THEME_PATH)
            await message.edit("✅ Theme reset to default")


module_list['Theme'] = f'{my_prefix()}theme [help/info] set [image_url]'
