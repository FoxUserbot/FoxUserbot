from pyrogram import Client, filters
import configparser
import os
from pathlib import Path
from command import fox_command

THEME_PATH = "userdata/theme.ini"

@Client.on_message(fox_command(command1="theme", Module_Name="Theme", names=os.path.basename(__file__), arg="[help/info/vars] [set/reset] [image/text] [value]") & filters.me)
async def theme_command(client, message):
    from prefix import my_prefix
    if len(message.command) < 2:
        text = ""
        if Path(THEME_PATH).exists():
            config = configparser.ConfigParser()
            config.read(THEME_PATH)
            url = config.get("help", "image", fallback="Not set")
            text += f"<b>🦊 Current help image:</b> `{url}`\n"
            url = config.get("info", "image", fallback="Not set")
            text += f"<b>🦊 Current info image:</b> `{url}`\n"
            custom_text = config.get("help", "text", fallback="Not set")
            text += f"<b>🦊 Current help text:</b> \n<blockquote expandable>{custom_text}</blockquote>\n"
            custom_text = config.get("info", "text", fallback="Not set")
            text += f"<b>🦊 Current info text:</b> \n<blockquote expandable>{custom_text}</blockquote>\n"
        else:
            text += "🦊 Using default image\n"

        await message.edit(text)
        return

    if message.command[1] == "help":
        if message.command[2] == "set":
            if message.command[3] == "image":
                if len(message.command) < 5:
                    await message.edit(f"**Usage:** `{my_prefix()}theme help set image [image_url]`")
                    return
                value = message.command[4]
            elif message.command[3] == "text":
                if len(message.command) < 5:
                    await message.edit(f"**Usage:** `{my_prefix()}theme help set text [text]`")
                    return
                
                full_text = message.text.html
                text_pos = full_text.find("text")
                if text_pos == -1:
                    await message.edit(f"**Usage:** `{my_prefix()}theme help set text [text]`")
                    return
                value = '\n'.join(full_text[text_pos + 5:].strip().split("\n"))
            else:
                await message.edit(f"**Usage:** `{my_prefix()}theme help set [image/text] [value]`")
                return
                
            os.makedirs(os.path.dirname(THEME_PATH), exist_ok=True)
            config = configparser.ConfigParser()
            
            if Path(THEME_PATH).exists():
                config.read(THEME_PATH)
            
            if not config.has_section("help"):
                config.add_section("help")
                
            # Используем "text" вместо "custom_text" для совместимости
            config.set("help", "text" if message.command[3] == "text" else "image", value)
            
            with open(THEME_PATH, 'w') as f:
                config.write(f)
                
            await message.edit("✅ Help settings updated")
        
        elif message.command[2] == "reset":
            if Path(THEME_PATH).exists():
                config = configparser.ConfigParser()
                config.read(THEME_PATH)
                if config.has_section("help"):
                    config.remove_section("help")
                with open(THEME_PATH, 'w') as f:
                    config.write(f)
            await message.edit("✅ Help theme reset to default")

    elif message.command[1] == "info":
        if message.command[2] == "set":
            if message.command[3] == "image":
                if len(message.command) < 5:
                    await message.edit(f"**Usage:** `{my_prefix()}theme info set image [image_url]`")
                    return
                value = message.command[4]
            elif message.command[3] == "text":
                if len(message.command) < 5:
                    await message.edit("**Usage:** `.theme info set text [text]`")
                    return
                
                full_text = message.text.html
                text_pos = full_text.find("text")
                if text_pos == -1:
                    await message.edit("**Usage:** `.theme info set text [text]`")
                    return
                value = '\n'.join(full_text[text_pos + 5:].strip().split("\n"))
            else:
                await message.edit("**Usage:** `.theme info set [image/text] [value]`")
                return
                
            os.makedirs(os.path.dirname(THEME_PATH), exist_ok=True)
            config = configparser.ConfigParser()
            
            if Path(THEME_PATH).exists():
                config.read(THEME_PATH)
            
            if not config.has_section("info"):
                config.add_section("info")
                
            # Используем "text" вместо "custom_text" для совместимости
            config.set("info", "text" if message.command[3] == "text" else "image", value)
            
            with open(THEME_PATH, 'w') as f:
                config.write(f)
                
            await message.edit("✅ Info settings updated")
        
        elif message.command[2] == "reset":
            if Path(THEME_PATH).exists():
                config = configparser.ConfigParser()
                config.read(THEME_PATH)
                if config.has_section("info"):
                    config.remove_section("info")
                with open(THEME_PATH, 'w') as f:
                    config.write(f)
            await message.edit("✅ Info theme reset to default")
    else:
        help_text = """
<blockquote expandable><b>🎨 <u>How to create your own theme:</u></b>

<b>1. Set image for info:</b>
<code>[your prefix]theme info set image [image_URL]</code>

<b>2. Set custom text for info:</b>
<code>[your prefix]theme info set text [your_text]</code>

<b>3. Set image for help:</b>
<code>[your prefix]theme help set image [image_URL]</code>

<b>4. Set custom text for help:</b>
<code>[your prefix]theme help set text [your_text]</code>

<b>5. Reset settings:</b>
<code>{[your prefix]}theme info reset</code>
<code>{[your prefix]}theme help reset</code>

<b>📝 <u>Available aliases for info:</u></b>

• <code>{version}</code> - Kurigram version
• <code>{python_version}</code> - Python version
• <code>{uptime}</code> - bot uptime
• <code>{platform}</code> - platform information

<b>📝 <u>Available aliases for help:</u></b>

• <code>{version}</code> - FoxUserbot version
• <code>{modules_count}</code> - number of modules
• <code>{prefix}</code> - command prefix
• <code>{commands_link}</code> - link to all commands list

<b>💡 <u>Example custom text for info:</u></b>

<code>{[your prefix]}theme info set text 🦊 FoxUserbot  {version}
Kurigram: {version}
🐍 Python {python_version}
⏰ Uptime: {uptime}
💻 Platform: {platform}</code>

<b>💡 <u>Example custom text for help:</u></b>

<code>{[your prefix]}theme help set text 🦊 FoxUserbot {version}
📦 Modules: {modules_count}
🔧 Prefix: {prefix}
❓ <a href="{commands_link}">List of all commands</a></code>
</blockquote>
        """
        await message.edit(help_text)
