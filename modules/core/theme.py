import configparser
import os
from pathlib import Path

from pyrogram import Client

from command import fox_command, fox_sudo, who_message, get_text, my_prefix

filename = os.path.basename(__file__)
Module_Name = 'Theme'

THEME_PATH = "userdata/theme.ini"

LANGUAGES = {
    "en": {
        "current_help_image": "<b><emoji id='5283051451889756068'>🦊</emoji> Current help image:</b> `{url}`\n",
        "current_info_image": "<b><emoji id='5283051451889756068'>🦊</emoji> Current info image:</b> `{url}`\n",
        "current_help_text": "<b><emoji id='5283051451889756068'>🦊</emoji> Current help text:</b> \n<blockquote expandable>{text}</blockquote>\n",
        "current_info_text": "<b><emoji id='5283051451889756068'>🦊</emoji> Current info text:</b> \n<blockquote expandable>{text}</blockquote>\n",
        "using_default": "<b><emoji id='5283051451889756068'>🦊</emoji> Using default image</b>\n",
        "usage_help_image": "**Usage:** `{prefix}theme help set image [image_url]`",
        "usage_help_text": "**Usage:** `{prefix}theme help set text [text]`",
        "usage_help_set": "**Usage:** `{prefix}theme help set [image/text] [value]`",
        "usage_info_image": "**Usage:** `{prefix}theme info set image [image_url]`",
        "usage_info_text": "**Usage:** `.theme info set text [text]`",
        "usage_info_set": "**Usage:** `.theme info set [image/text] [value]`",
        "help_updated": "<emoji id='5237699328843200968'>✅</emoji> Help settings updated",
        "help_reset": "<emoji id='5237699328843200968'>✅</emoji> Help theme reset to default",
        "info_updated": "<emoji id='5237699328843200968'>✅</emoji> Info settings updated",
        "info_reset": "<emoji id='5237699328843200968'>✅</emoji> <b>Info theme reset to default</b>",
        "help_text": """
<blockquote expandable><b><emoji id='5283051451889756068'>🎨</emoji> <u>How to create your own theme:</u></b>

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

<b><emoji id='5444856076954520455'>📝</emoji> <u>Available aliases for info:</u></b>

• <code>{version}</code> - Kurigram version
• <code>{python_version}</code> - Python version
• <code>{uptime}</code> - bot uptime
• <code>{platform}</code> - platform information

<b><emoji id='5444856076954520455'>📝</emoji> <u>Available aliases for help:</u></b>

• <code>{version}</code> - FoxUserbot version
• <code>{modules_count}</code> - number of modules
• <code>{prefix}</code> - command prefix
• <code>{commands_link}</code> - link to all commands list
• <code>{safe_mode}</code> - safe mode status

<b><emoji id='5422439311196834318'>💡</emoji> <u>Example custom text for info:</u></b>

<code>{[your prefix]}theme info set text 🦊 FoxUserbot  {version}
Kurigram: {version}
🐍 Python {python_version}
⏰ Uptime: {uptime}
💻 Platform: {platform}</code>
❓ Safe Mod: {safe_mod}

<b><emoji id='5422439311196834318'>💡</emoji> <u>Example custom text for help:</u></b>

<code>{[your prefix]}theme help set text 🦊 FoxUserbot {version}
📦 Modules: {modules_count}
🔧 Prefix: {prefix}
❓ <a href="{commands_link}">List of all commands</a></code>
</blockquote>
        """
    },
    "ru": {
        "current_help_image": "<b><emoji id='5283051451889756068'>🦊</emoji> Текущее изображение помощи:</b> `{url}`\n",
        "current_info_image": "<b><emoji id='5283051451889756068'>🦊</emoji> Текущее изображение инфо:</b> `{url}`\n",
        "current_help_text": "<b><emoji id='5283051451889756068'>🦊</emoji> Текущий текст помощи:</b> \n<blockquote expandable>{text}</blockquote>\n",
        "current_info_text": "<b><emoji id='5283051451889756068'>🦊</emoji> Текущий текст инфо:</b> \n<blockquote expandable>{text}</blockquote>\n",
        "using_default": "<b><emoji id='5283051451889756068'>🦊</emoji> Используется изображение по умолчанию</b>\n",
        "usage_help_image": "**Использование:** `{prefix}theme help set image [image_url]`",
        "usage_help_text": "**Использование:** `{prefix}theme help set text [text]`",
        "usage_help_set": "**Использование:** `{prefix}theme help set [image/text] [value]`",
        "usage_info_image": "**Использование:** `{prefix}theme info set image [image_url]`",
        "usage_info_text": "**Использование:** `.theme info set text [text]`",
        "usage_info_set": "**Использование:** `.theme info set [image/text] [value]`",
        "help_updated": "<emoji id='5237699328843200968'>✅</emoji> Параметры помощи обновлены",
        "help_reset": "<emoji id='5237699328843200968'>✅</emoji> Тема помощи сброшена на стандартную",
        "info_updated": "<emoji id='5237699328843200968'>✅</emoji> Параметры инфо обновлены",
        "info_reset": "<emoji id='5237699328843200968'>✅</emoji> <b>Тема инфо сброшена на стандартную</b>",
        "help_text": """
<blockquote expandable><b><emoji id='5283051451889756068'>🎨</emoji> <u>Как создать свою тему:</u></b>

<b>1. Установить изображение для инфо:</b>
<code>[ваш префикс]theme info set image [image_URL]</code>

<b>2. Установить пользовательский текст для инфо:</b>
<code>[ваш префикс]theme info set text [ваш_текст]</code>

<b>3. Установить изображение для помощи:</b>
<code>[ваш префикс]theme help set image [image_URL]</code>

<b>4. Установить пользовательский текст для помощи:</b>
<code>[ваш префикс]theme help set text [ваш_текст]</code>

<b>5. Сбросить параметры:</b>
<code>{[ваш префикс]}theme info reset</code>
<code>{[ваш префикс]}theme help reset</code>

<b><emoji id='5444856076954520455'>📝</emoji> <u>Доступные переменные для инфо:</u></b>

• <code>{version}</code> - версия Kurigram
• <code>{python_version}</code> - версия Python
• <code>{uptime}</code> - время работы бота
• <code>{platform}</code> - информация о платформе

<b><emoji id='5444856076954520455'>📝</emoji> <u>Доступные переменные для помощи:</u></b>

• <code>{version}</code> - версия FoxUserbot
• <code>{modules_count}</code> - количество модулей
• <code>{prefix}</code> - префикс команды
• <code>{commands_link}</code> - ссылка на список всех команд
• <code>{safe_mode}</code> - статус безопасного режима

<b><emoji id='5422439311196834318'>💡</emoji> <u>Пример пользовательского текста для инфо:</u></b>

<code>{[ваш префикс]}theme info set text 🦊 FoxUserbot  {version}
Kurigram: {version}
🐍 Python {python_version}
⏰ Время работы: {uptime}
💻 Платформа: {platform}</code>
❓ Безопасный режим: {safe_mod}

<b><emoji id='5422439311196834318'>💡</emoji> <u>Пример пользовательского текста для помощи:</u></b>

<code>{[ваш префикс]}theme help set text 🦊 FoxUserbot {version}
📦 Модули: {modules_count}
🔧 Префикс: {prefix}
❓ <a href="{commands_link}">Список всех команд</a></code>
</blockquote>
        """
    },
    "ua": {
        "current_help_image": "<b><emoji id='5283051451889756068'>🦊</emoji> Поточне зображення допомоги:</b> `{url}`\n",
        "current_info_image": "<b><emoji id='5283051451889756068'>🦊</emoji> Поточне зображення інфо:</b> `{url}`\n",
        "current_help_text": "<b><emoji id='5283051451889756068'>🦊</emoji> Поточний текст допомоги:</b> \n<blockquote expandable>{text}</blockquote>\n",
        "current_info_text": "<b><emoji id='5283051451889756068'>🦊</emoji> Поточний текст інфо:</b> \n<blockquote expandable>{text}</blockquote>\n",
        "using_default": "<b><emoji id='5283051451889756068'>🦊</emoji> Використовується зображення за замовчуванням</b>\n",
        "usage_help_image": "**Використання:** `{prefix}theme help set image [image_url]`",
        "usage_help_text": "**Використання:** `{prefix}theme help set text [text]`",
        "usage_help_set": "**Використання:** `{prefix}theme help set [image/text] [value]`",
        "usage_info_image": "**Використання:** `{prefix}theme info set image [image_url]`",
        "usage_info_text": "**Використання:** `.theme info set text [text]`",
        "usage_info_set": "**Використання:** `.theme info set [image/text] [value]`",
        "help_updated": "<emoji id='5237699328843200968'>✅</emoji> Параметри допомоги оновлено",
        "help_reset": "<emoji id='5237699328843200968'>✅</emoji> Тема допомоги скинута на стандартну",
        "info_updated": "<emoji id='5237699328843200968'>✅</emoji> Параметри інфо оновлено",
        "info_reset": "<emoji id='5237699328843200968'>✅</emoji> <b>Тема інфо скинута на стандартну</b>",
        "help_text": """
<blockquote expandable><b><emoji id='5283051451889756068'>🎨</emoji> <u>Як створити власну тему:</u></b>

<b>1. Встановити зображення для інфо:</b>
<code>[ваш префікс]theme info set image [image_URL]</code>

<b>2. Встановити користувацький текст для інфо:</b>
<code>[ваш префікс]theme info set text [ваш_текст]</code>

<b>3. Встановити зображення для допомоги:</b>
<code>[ваш префікс]theme help set image [image_URL]</code>

<b>4. Встановити користувацький текст для допомоги:</b>
<code>[ваш префікс]theme help set text [ваш_текст]</code>

<b>5. Скинути параметри:</b>
<code>{[ваш префікс]}theme info reset</code>
<code>{[ваш префікс]}theme help reset</code>

<b><emoji id='5444856076954520455'>📝</emoji> <u>Доступні змінні для інфо:</u></b>

• <code>{version}</code> - версія Kurigram
• <code>{python_version}</code> - версія Python
• <code>{uptime}</code> - час роботи бота
• <code>{platform}</code> - інформація про платформу

<b><emoji id='5444856076954520455'>📝</emoji> <u>Доступні змінні для допомоги:</u></b>

• <code>{version}</code> - версія FoxUserbot
• <code>{modules_count}</code> - кількість модулів
• <code>{prefix}</code> - префікс команди
• <code>{commands_link}</code> - посилання на список всіх команд
• <code>{safe_mode}</code> - статус безпечного режиму

<b><emoji id='5422439311196834318'>💡</emoji> <u>Приклад користувацького тексту для інфо:</u></b>

<code>{[ваш префікс]}theme info set text 🦊 FoxUserbot  {version}
Kurigram: {version}
🐍 Python {python_version}
⏰ Час роботи: {uptime}
💻 Платформа: {platform}</code>
❓ Безпечний режим: {safe_mod}

<b><emoji id='5422439311196834318'>💡</emoji> <u>Приклад користувацького тексту для допомоги:</u></b>

<code>{[ваш префікс]}theme help set text 🦊 FoxUserbot {version}
📦 Модулі: {modules_count}
🔧 Префікс: {prefix}
❓ <a href="{commands_link}">Список всіх команд</a></code>
</blockquote>
        """
    }
}


@Client.on_message(fox_command("theme", Module_Name, filename, "[help/info/vars] [set/reset] [image/text] [value]") & fox_sudo())
async def theme_command(client, message):
    message = await who_message(client, message)
    if len(message.text.split()) < 2:
        text = ""
        if Path(THEME_PATH).exists():
            config = configparser.ConfigParser()
            config.read(THEME_PATH)
            url = config.get("help", "image", fallback="Not set")
            text += get_text("theme", "current_help_image", LANGUAGES=LANGUAGES, url=url)
            url = config.get("info", "image", fallback="Not set")
            text += get_text("theme", "current_info_image", LANGUAGES=LANGUAGES, url=url)
            custom_text = config.get("help", "text", fallback="Not set")
            text += get_text("theme", "current_help_text", LANGUAGES=LANGUAGES, text=custom_text)
            custom_text = config.get("info", "text", fallback="Not set")
            text += get_text("theme", "current_info_text", LANGUAGES=LANGUAGES, text=custom_text)
        else:
            text += get_text("theme", "using_default", LANGUAGES=LANGUAGES)

        await message.edit(text)
        return

    if message.text.split()[1] == "help":
        parts = message.text.split()
        if len(parts) < 3:
            help_text = get_text("theme", "help_text", LANGUAGES=LANGUAGES)
            await message.edit(help_text)
            return
        
        if parts[2] == "set":
            if len(parts) < 4:
                usage_text = get_text("theme", "usage_help_set", LANGUAGES=LANGUAGES, prefix=my_prefix())
                await message.edit(usage_text)
                return
            
            if parts[3] == "image":
                if len(parts) < 5:
                    usage_text = get_text("theme", "usage_help_image", LANGUAGES=LANGUAGES, prefix=my_prefix())
                    await message.edit(usage_text)
                    return
                value = parts[4]
            elif parts[3] == "text":
                if len(parts) < 5:
                    usage_text = get_text("theme", "usage_help_text", LANGUAGES=LANGUAGES, prefix=my_prefix())
                    await message.edit(usage_text)
                    return
                
                full_text = message.text.html
                text_pos = full_text.find("text")
                if text_pos == -1:
                    usage_text = get_text("theme", "usage_help_text", LANGUAGES=LANGUAGES, prefix=my_prefix())
                    await message.edit(usage_text)
                    return
                value = '\n'.join(full_text[text_pos + 5:].strip().split("\n"))
            else:
                usage_text = get_text("theme", "usage_help_set", LANGUAGES=LANGUAGES, prefix=my_prefix())
                await message.edit(usage_text)
                return
                
            os.makedirs(os.path.dirname(THEME_PATH), exist_ok=True)
            config = configparser.ConfigParser()
            
            if Path(THEME_PATH).exists():
                config.read(THEME_PATH)
            
            if not config.has_section("help"):
                config.add_section("help")
            config.set("help", "text" if parts[3] == "text" else "image", value)
            
            with open(THEME_PATH, 'w') as f:
                config.write(f)
                
            updated_text = get_text("theme", "help_updated", LANGUAGES=LANGUAGES)
            await message.edit(updated_text)
        
        elif parts[2] == "reset":
            if Path(THEME_PATH).exists():
                config = configparser.ConfigParser()
                config.read(THEME_PATH)
                if config.has_section("help"):
                    config.remove_section("help")
                with open(THEME_PATH, 'w') as f:
                    config.write(f)
            reset_text = get_text("theme", "help_reset", LANGUAGES=LANGUAGES)
            await message.edit(reset_text)
        else:
            help_text = get_text("theme", "help_text", LANGUAGES=LANGUAGES)
            await message.edit(help_text)

    elif message.text.split()[1] == "info":
        parts = message.text.split()
        if len(parts) < 3:
            help_text = get_text("theme", "help_text", LANGUAGES=LANGUAGES)
            await message.edit(help_text)
            return
        
        if parts[2] == "set":
            if len(parts) < 4:
                usage_text = get_text("theme", "usage_info_set", LANGUAGES=LANGUAGES)
                await message.edit(usage_text)
                return
            
            if parts[3] == "image":
                if len(parts) < 5:
                    usage_text = get_text("theme", "usage_info_image", LANGUAGES=LANGUAGES, prefix=my_prefix())
                    await message.edit(usage_text)
                    return
                value = parts[4]
            elif parts[3] == "text":
                if len(parts) < 5:
                    usage_text = get_text("theme", "usage_info_text", LANGUAGES=LANGUAGES)
                    await message.edit(usage_text)
                    return
                
                full_text = message.text.html
                text_pos = full_text.find("text")
                if text_pos == -1:
                    usage_text = get_text("theme", "usage_info_text", LANGUAGES=LANGUAGES)
                    await message.edit(usage_text)
                    return
                value = '\n'.join(full_text[text_pos + 5:].strip().split("\n"))
            else:
                usage_text = get_text("theme", "usage_info_set", LANGUAGES=LANGUAGES)
                await message.edit(usage_text)
                return
                
            os.makedirs(os.path.dirname(THEME_PATH), exist_ok=True)
            config = configparser.ConfigParser()
            
            if Path(THEME_PATH).exists():
                config.read(THEME_PATH)
            
            if not config.has_section("info"):
                config.add_section("info")
                
            config.set("info", "text" if parts[3] == "text" else "image", value)
            
            with open(THEME_PATH, 'w') as f:
                config.write(f)
                
            updated_text = get_text("theme", "info_updated", LANGUAGES=LANGUAGES)
            await message.edit(updated_text)
        
        elif parts[2] == "reset":
            if Path(THEME_PATH).exists():
                config = configparser.ConfigParser()
                config.read(THEME_PATH)
                if config.has_section("info"):
                    config.remove_section("info")
                with open(THEME_PATH, 'w') as f:
                    config.write(f)
            reset_text = get_text("theme", "info_reset", LANGUAGES=LANGUAGES)
            await message.edit(reset_text)
        else:
            help_text = get_text("theme", "help_text", LANGUAGES=LANGUAGES)
            await message.edit(help_text)
    else:
        help_text = get_text("theme", "help_text", LANGUAGES=LANGUAGES)
        await message.edit(help_text)
