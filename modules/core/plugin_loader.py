import importlib
import logging
import os
import sys
from importlib.machinery import SourceFileLoader

from pyrogram import Client


def load_all_external_plugins(client: Client):
    loaded_dir = "modules/loaded"
    if not os.path.exists(loaded_dir):
        logging.info("[PluginLoader] No external plugins directory found")
        return
    
    files = [f for f in os.listdir(loaded_dir) if f.endswith(".py") and not f.startswith("_")]
    if not files:
        logging.info("[PluginLoader] No external plugins found in modules/loaded")
        return
    
    loaded_count = 0
    
    for filename in files:
        try:
            module_stem = os.path.splitext(filename)[0]
            module_qualname = f"modules.loaded.{module_stem}"
            
            if module_qualname in sys.modules:
                mod = importlib.reload(sys.modules[module_qualname])
            else:
                module_path = os.path.join(loaded_dir, filename)
                mod = SourceFileLoader(module_qualname, module_path).load_module()
                sys.modules[module_qualname] = mod
            
            loaded_count += 1
            logging.info(f"[PluginLoader] Loaded {filename}")
            
        except Exception as e:
            logging.error(f"[PluginLoader] Failed to load {filename}: {e}")
    
    logging.info(f"[PluginLoader] Successfully loaded {loaded_count} external plugins")


def load_single_plugin(plugin_name: str):
    try:
        module_qualname = f"modules.loaded.{plugin_name}"
        module_path = os.path.join("modules/loaded", f"{plugin_name}.py")
        
        if not os.path.exists(module_path):
            return False, f"Plugin {plugin_name} not found"
        
        if module_qualname in sys.modules:
            mod = importlib.reload(sys.modules[module_qualname])
        else:
            mod = SourceFileLoader(module_qualname, module_path).load_module()
            sys.modules[module_qualname] = mod
        
        logging.info(f"[PluginLoader] Loaded {plugin_name}")
        return True, f"Plugin {plugin_name} loaded successfully"
        
    except Exception as e:
        logging.error(f"[PluginLoader] Failed to load {plugin_name}: {e}")
        return False, f"Failed to load {plugin_name}: {e}"


def unload_single_plugin(plugin_name: str):
    try:
        module_qualname = f"modules.loaded.{plugin_name}"
        if module_qualname in sys.modules:
            del sys.modules[module_qualname]
            logging.info(f"[PluginLoader] Unloaded {plugin_name}")
            return True, f"Plugin {plugin_name} unloaded successfully"
        else:
            return False, f"Plugin {plugin_name} not loaded"
    except Exception as e:
        logging.error(f"[PluginLoader] Failed to unload {plugin_name}: {e}")
        return False, f"Failed to unload {plugin_name}: {e}"