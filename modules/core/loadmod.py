import os

import wget
from command import fox_command, fox_sudo, who_message
from modules.core.plugin_loader import load_single_plugin
from modules.core.plugin_validator import PluginValidator
from pyrogram import Client

validator = PluginValidator()

@Client.on_message(fox_command("loadmod", "Loadmod", os.path.basename(__file__), "[link to the module/reply]") & fox_sudo())
async def loadmod(client, message):
    message = await who_message(client, message)
    await message.edit(f"<emoji id='5190903199137013741'>🔍</emoji> <b>Checking and loading module</b>")
    
    temp_file_path = None
    try:
        text = (message.text or "").strip()
        parts = text.split(maxsplit=1)
        arg = parts[1].strip() if len(parts) > 1 else None

        filename = None
        original_filename = None

        if arg and (arg.startswith("http://") or arg.startswith("https://")):
            original_filename = os.path.basename(arg)
            if not original_filename.endswith('.py'):
                original_filename += '.py'
            
            temp_dir = "temp"
            os.makedirs(temp_dir, exist_ok=True)
            temp_file_path = os.path.join(temp_dir, original_filename)
            
            await message.edit(f"<emoji id='5308082115103414795'>📥</emoji> <b>Downloading module...</b>")
            filename = wget.download(arg, temp_file_path)
            print()
            
        elif getattr(message, "reply_to_message", None) and getattr(message.reply_to_message, "document", None):
            original_filename = message.reply_to_message.document.file_name
            temp_dir = "temp"
            os.makedirs(temp_dir, exist_ok=True)
            temp_file_path = os.path.join(temp_dir, original_filename)
            
            await message.edit(f"<emoji id='5308082115103414795'>📥</emoji> <b>Downloading file...</b>")
            filename = await client.download_media(message.reply_to_message.document, file_name=temp_file_path)
            
        elif arg:
            filename = os.path.join('modules/loaded', arg if arg.endswith('.py') else f"{arg}.py")
            if not os.path.exists(filename):
                await message.edit(f"<emoji id='5210952531676504517'>❌</emoji> <b>Module {arg} not found</b>")
                return
            original_filename = os.path.basename(filename)
        
        if not filename or not os.path.exists(filename):
            await message.edit("<emoji id='5210952531676504517'>❌</emoji> <b>File not found or download failed</b>")
            return
        
        await message.edit(f"<emoji id='5197687813709120954'>🔧</emoji> <b>Validating plugin...</b>")
        
        success, converted_path, error_message = validator.validate_and_convert_plugin(filename, original_filename)
        
        if not success:
            await message.edit(
                f"<emoji id='5210952531676504517'>❌</emoji> <b>Plugin validation failed</b>\n<code>{error_message}</code>"
            )
            return
        
        module_stem = os.path.splitext(os.path.basename(str(converted_path)))[0]
        
        await message.edit(f"<emoji id='5456298971529814649'>⚡</emoji> <b>Loading module {module_stem}...</b>")
        handlers_loaded = load_single_plugin(client, module_stem)

        await message.edit(
            f"<emoji id='5237699328843200968'>✅</emoji> <b>Module `{module_stem}` loaded successfully!</b>\n"
            f"<code>{handlers_loaded} handlers registered</code>"
        )
        
    except Exception as error:
        await message.edit(
            f"<emoji id='5210952531676504517'>❌</emoji> <b>Error while loading</b>\n<code>{error}</code>"
        )
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as e:
                logging.warning(f"Failed to remove temp file {temp_file_path}: {e}")