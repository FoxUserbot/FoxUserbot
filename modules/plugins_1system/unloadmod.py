import importlib
import os
import sys

from pyrogram import Client

from command import fox_command, fox_sudo, who_message
from modules.plugins_1system.settings.main_settings import (file_list,
                                                            module_list)


@Client.on_message(fox_command("unloadmod", "Unloadmod", os.path.basename(__file__), "[module name]") & fox_sudo())
async def unloadmod(client, message):
    message = await who_message(client, message)
    try:
        text = (message.text or "").strip()
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            await message.edit("<emoji id='5210952531676504517'>❌</emoji> <b>Specify module name</b>")
            return
        module_stem = parts[1].strip().replace('.py', '')
        module_qualname = f"modules.plugins_2custom.{module_stem}"
        _remove_module_handlers(client, module_qualname)
        try:
            file = file_list.get(module_stem) or file_list.get(f"{module_stem}.py")
            if file:
                file_path = os.path.join('modules', 'plugins_2custom', file)
                if os.path.exists(file_path):
                    os.remove(file_path)
            module_list.pop(module_stem, None)
            file_list.pop(module_stem, None)
            file_list.pop(f"{module_stem}.py", None)
        except Exception:
            pass
        await message.edit(f"<emoji id='5237699328843200968'>✅</emoji> <b>Module successfully unloaded</b>")
    except Exception as e:
        await message.edit(f"<emoji id='5210952531676504517'>❌</emoji> <b>Error while unloading</b> \n <spolier>{e}</spolier>")



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



