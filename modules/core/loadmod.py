from pyrogram import Client
import os
import wget
import importlib
import sys
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_file_location

from command import fox_command, fox_sudo, who_message
from modules.core.plugin_validator import PluginValidator


async def load_plugin_from_file(file_path, plugin_name):
    try:
        module_qualname = f"modules.loaded.{plugin_name}"
        
        spec = spec_from_file_location(module_qualname, file_path)
        if spec is None:
            return False, f"Could not create spec for {plugin_name}"
        
        mod = module_from_spec(spec)
        sys.modules[module_qualname] = mod
        
        spec.loader.exec_module(mod)
        
        return True, f"Plugin {plugin_name} loaded successfully"
        
    except Exception as e:
        if module_qualname in sys.modules:
            del sys.modules[module_qualname]
        return False, f"Failed to load {plugin_name}: {e}"


@Client.on_message(fox_command("loadmod", "Loadmod", os.path.basename(__file__), "[link to the module/reply]") & fox_sudo())
async def loadmod(client, message):
    message = await who_message(client, message)
    
    temp_file = None
    validator = PluginValidator()
    
    try:
        if message.reply_to_message and message.reply_to_message.document:
            await message.edit("<b>📥 Downloading module from message...</b>")
            
            file_name = message.reply_to_message.document.file_name
            if not file_name.endswith('.py'):
                await message.edit("❌ <b>File must be a Python script (.py)</b>")
                return
                
            temp_file = await client.download_media(
                message.reply_to_message.document, 
                file_name="temp/"
            )
            
        else:
            if len(message.command) < 2:
                await message.edit("❌ <b>Please provide a link or reply to a file</b>")
                return
                
            link = message.command[1]
            await message.edit("<b>📥 Downloading module from link...</b>")
            
            try:
                file_name = os.path.basename(link)
                if not file_name.endswith('.py'):
                    file_name += '.py'
                    
                temp_file = wget.download(link, out="temp/")
                    
            except Exception as e:
                await message.edit(f"❌ <b>Download error:</b>\n<code>{e}</code>")
                return
        
        if not temp_file or not os.path.exists(temp_file):
            await message.edit("❌ <b>Download failed</b>")
            return

        await message.edit("<b>🔧 Validating and converting plugin...</b>")
        
        success, final_path, error_message = validator.validate_and_convert_plugin(temp_file, file_name)
        
        if not success:
            await message.edit(f"❌ <b>Plugin validation failed:</b>\n<code>{error_message}</code>")
            return

        plugin_name = os.path.splitext(os.path.basename(final_path))[0]
        await message.edit(f"<b>⚡ Loading module {plugin_name}...</b>")
        
        success, result = await load_plugin_from_file(final_path, plugin_name)
        
        if success:
            await message.edit(f"✅ <b>Module {plugin_name} loaded successfully!</b>")
        else:
            await message.edit(f"❌ <b>Error loading module:</b>\n<code>{result}</code>")
                
    except Exception as error:
        await message.edit(f"❌ <b>Error:</b>\n<code>{error}</code>")
    
    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass