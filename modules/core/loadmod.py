import importlib
import os
import sys
from importlib.machinery import SourceFileLoader

import wget
from pyrogram import Client

from command import fox_command, fox_sudo, who_message
from modules.core.plugin_validator import PluginValidator


def _iter_plugin_handlers(module):
    for obj in module.__dict__.values():
        if callable(obj) and hasattr(obj, "handlers"):
            for h in getattr(obj, "handlers", []):
                yield h


def _remove_module_handlers(client: Client, module_qualname: str):
    try:
        mod = importlib.import_module(module_qualname)
    except Exception:
        module_stem = module_qualname.rsplit('.', 1)[-1]
        module_path = os.path.join('modules', 'loaded', f'{module_stem}.py')
        if os.path.exists(module_path):
            mod = SourceFileLoader(module_qualname, module_path).load_module()
        else:
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
        try:
            mod = importlib.import_module(module_qualname)
        except Exception:
            module_stem = module_qualname.rsplit('.', 1)[-1]
            module_path = os.path.join('modules', 'loaded', f'{module_stem}.py')
            mod = SourceFileLoader(module_qualname, module_path).load_module()
    for h in _iter_plugin_handlers(mod):
        client.add_handler(*h)


@Client.on_message(fox_command("loadmod", "Loadmod", os.path.basename(__file__), "[link to the module/reply]") & fox_sudo())
async def loadmod(client, message):
    message = await who_message(client, message)
    await message.edit(f"<emoji id='5190903199137013741'>🔍</emoji> <b>Checking and loading module</b>")
    
    validator = PluginValidator()
    
    try:
        text = (message.text or "").strip()
        parts = text.split(maxsplit=1)
        arg = parts[1].strip() if len(parts) > 1 else None

        filename = None

        if arg and (arg.startswith("http://") or arg.startswith("https://")):
            temp_file = wget.download(arg, out="temp/")
            
            original_filename = os.path.basename(arg)
            if not original_filename.endswith('.py'):
                original_filename += '.py'
                
            success, final_path, error_message = validator.validate_and_convert_plugin(temp_file, original_filename)
            
            if not success:
                await message.edit(f"<emoji id='5210952531676504517'>❌</emoji> <b>Plugin validation failed</b>\n<code>{error_message}</code>")
                return
                
            filename = final_path
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        elif getattr(message, "reply_to_message", None) and getattr(message.reply_to_message, "document", None):
            original_filename = message.reply_to_message.document.file_name
            temp_file = await client.download_media(message.reply_to_message.document, file_name='temp/')
            
            success, final_path, error_message = validator.validate_and_convert_plugin(temp_file, original_filename)
            
            if not success:
                await message.edit(f"<emoji id='5210952531676504517'>❌</emoji> <b>Plugin validation failed</b>\n<code>{error_message}</code>")
                return
                
            filename = final_path
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        elif arg:
            filename = arg if arg.endswith('.py') else f"{arg}.py"
            
        if not filename:
            await message.edit("<emoji id='5210952531676504517'>❌</emoji> <b>Specify a link, reply with a .py file, or module name</b>")
            return
            
        module_stem = os.path.splitext(os.path.basename(str(filename)))[0]
        module_qualname = f"modules.loaded.{module_stem}"
        _remove_module_handlers(client, module_qualname)
        _load_module_handlers(client, module_qualname)

        await message.edit(
            f"<emoji id='5237699328843200968'>✅</emoji> <b>Module {module_stem} loaded successfully!</b>"
        )
        
    except Exception as error:
        await message.edit(
            f"<emoji id='5210952531676504517'>❌</emoji> <b>Error while loading</b>\n<code>{error}</code>"
        )