# -*- coding: utf-8 -*-
import importlib
import os
import sys

from pyrogram import Client

from command import fox_command, fox_sudo, who_message, get_text
from modules.core.settings.main_settings import file_list, module_list

filename = os.path.basename(__file__)
Module_Name = 'Unloadmod'

LANGUAGES = {
    "en": {
        "no_module": "<emoji id='5210952531676504517'>❌</emoji> <b>Specify module name</b>",
        "success": "<emoji id='5237699328843200968'>✅</emoji> <b>Module successfully unloaded</b>",
        "error": "<emoji id='5210952531676504517'>❌</emoji> <b>Error while unloading</b> \n <spoiler>{error}</spoiler>"
    },
    "ru": {
        "no_module": "<emoji id='5210952531676504517'>❌</emoji> <b>Укажите название модуля</b>",
        "success": "<emoji id='5237699328843200968'>✅</emoji> <b>Модуль успешно выгружен</b>",
        "error": "<emoji id='5210952531676504517'>❌</emoji> <b>Ошибка при выгрузке</b> \n <spoiler>{error}</spoiler>"
    },
    "ua": {
        "no_module": "<emoji id='5210952531676504517'>❌</emoji> <b>Вкажіть назву модуля</b>",
        "success": "<emoji id='5237699328843200968'>✅</emoji> <b>Модуль успішно вивантажено</b>",
        "error": "<emoji id='5210952531676504517'>❌</emoji> <b>Помилка при вивантаженні</b> \n <spoiler>{error}</spoiler>"
    }
}


@Client.on_message(fox_command("unloadmod", Module_Name, filename, "[module name]") & fox_sudo())
async def unloadmod(client, message):
    message = await who_message(client, message)
    try:
        text = (message.text or "").strip()
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            await message.edit(get_text("unloadmod", "no_module", LANGUAGES=LANGUAGES))
            return
        
        module_stem = parts[1].strip().replace('.py', '')
        module_qualname = f"modules.loaded.{module_stem}"
        _remove_module_handlers(client, module_qualname)
        
        try:
            file = file_list.get(module_stem) or file_list.get(f"{module_stem}.py")
            if file:
                file_path = os.path.join('modules', 'loaded', file)
                if os.path.exists(file_path):
                    os.remove(file_path)
            module_list.pop(module_stem, None)
            file_list.pop(module_stem, None)
            file_list.pop(f"{module_stem}.py", None)
        except Exception:
            pass
        
        await message.edit(get_text("unloadmod", "success", LANGUAGES=LANGUAGES))
    except Exception as e:
        await message.edit(get_text("unloadmod", "error", LANGUAGES=LANGUAGES, error=str(e)))


def _iter_plugin_handlers(module):
    for obj in module.__dict__.values():
        if callable(obj) and hasattr(obj, "handlers"):
            for h in getattr(obj, "handlers", []):
                yield h


def _remove_module_handlers(client: Client, module_qualname: str):
    try:
        mod = importlib.import_module(module_qualname)
    except Exception:
        return
    
    for h in list(_iter_plugin_handlers(mod)):
        try:
            handler, group = h
            if hasattr(client.dispatcher, 'groups') and group in client.dispatcher.groups:
                if handler in client.dispatcher.groups[group]:
                    client.remove_handler(handler, group)
        except Exception:
            pass
    sys.modules.pop(module_qualname, None)


def _load_module_handlers(client: Client, module_qualname: str):
    importlib.invalidate_caches()
    if module_qualname in sys.modules:
        mod = importlib.reload(sys.modules[module_qualname])
    else:
        mod = importlib.import_module(module_qualname)
    for h in _iter_plugin_handlers(mod):
        client.add_handler(*h)