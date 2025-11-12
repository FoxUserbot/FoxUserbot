# -*- coding: utf-8 -*-
import configparser
import os
from pathlib import Path

from pyrogram import Client

from command import all_lang, fox_command, fox_sudo, my_prefix, who_message, set_global_lang, get_global_lang

filename = os.path.basename(__file__)
Module_Name = 'Language'

LANGUAGES = {
    "en": {
        "success": "✅ Language set to: {lang}",
        "error": "❌ Error setting language", 
        "invalid": "❌ Invalid language! Available: {langs}",
        "usage": "🌐 Available languages: {langs}\n💡 Usage: <code>{my_prefix}setlang en</code>"
    },
    "ru": {
        "success": "✅ Язык установлен: {lang}",
        "error": "❌ Ошибка установки языка",
        "invalid": "❌ Неверный язык! Доступно: {langs}",
        "usage": "🌐 Доступные языки: {langs}\n💡 Использование: <code>{my_prefix}setlang en</code>"
    },
    "ua": {
        "success": "✅ Мову встановлено: {lang}",
        "error": "❌ Помилка встановлення мови",
        "invalid": "❌ Невірна мова! Доступно: {langs}",
        "usage": "🌐 Доступні мови: {langs}\n💡 Використання: <code>{my_prefix}setlang en</code>"
    }
}

def get_lang_config():
    lang_config_path = Path("userdata/language.ini")
    
    if lang_config_path.exists():
        config = configparser.ConfigParser()
        config.read(lang_config_path)
        return config.get("language", "lang", fallback="en")  # исправлено на "lang"
    else:
        return "en"

def save_lang_config(lang: str):
    lang_config_path = Path("userdata/language.ini")
    
    lang_config_path.parent.mkdir(exist_ok=True)
    
    config = configparser.ConfigParser()
    
    if lang_config_path.exists():
        config.read(lang_config_path)
    
    if not config.has_section("language"):
        config.add_section("language")
    config.set("language", "lang", lang)  # исправлено на "lang"
    
    with open(lang_config_path, "w") as f:
        config.write(f)


@Client.on_message(fox_command("setlang", Module_Name, filename, "[lang]") & fox_sudo())
async def set_language(client, message):
    message = await who_message(client, message)
    
    if len(message.text.split()) < 2:
        available_langs = ", ".join(all_lang) 
        usage_text = LANGUAGES[get_lang_config()]["usage"].format(
            langs=available_langs, 
            my_prefix=my_prefix()
        )
        await message.edit(usage_text)
        return
    
    lang = message.text.split()[1].lower()
    current_lang = get_lang_config()
    
    if lang in all_lang: 
        save_lang_config(lang)
        
        if set_global_lang(lang):
            success_text = LANGUAGES.get(lang, LANGUAGES["en"])["success"].format(lang=lang.upper())
            await message.edit(success_text)
        else:
            error_text = LANGUAGES.get(current_lang, LANGUAGES["en"])["error"]
            await message.edit(error_text)
    else:
        available_langs = ", ".join(all_lang)
        invalid_text = LANGUAGES.get(current_lang, LANGUAGES["en"])["invalid"].format(langs=available_langs)
        await message.edit(invalid_text)


@Client.on_message(fox_command("getlang", Module_Name, filename) & fox_sudo())
async def get_current_language(client, message):
    message = await who_message(client, message)
    
    current_lang = get_lang_config()
    global_lang = get_global_lang()
    
    text = (f"🌐 <b>Current language:</b> {current_lang.upper()}\n"
            f"🔧 <b>Global lang:</b> {global_lang}\n"
            f"💡 <b>Available:</b> {', '.join(all_lang)}")
    
    await message.edit(text)