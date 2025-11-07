import importlib
import logging
import os
import sys
from importlib.machinery import SourceFileLoader

from pyrogram import Client


def _iter_plugin_handlers(module):
    for obj in module.__dict__.values():
        if callable(obj) and hasattr(obj, "handlers"):
            for h in getattr(obj, "handlers", []):
                yield h


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
            _load_module_handlers(client, module_qualname)
            loaded_count += 1
            logging.info(f"[PluginLoader] Loaded {filename}")
        except Exception as e:
            logging.error(f"[PluginLoader] Failed to load {filename}: {e}")
    
    logging.info(f"[PluginLoader] Successfully loaded {loaded_count} external plugins")