import os
import json
from pathlib import Path
from pyrogram import Client, filters
from command import fox_command
from typing import Dict, List
from prefix import my_prefix
from modules.plugins_1system.restarter import restart

ALIASES_DB_PATH = "userdata/command_aliases.json"

class AliasManager:
    def __init__(self):
        self.aliases: Dict[str, str] = {}
        self.load_aliases()

    def load_aliases(self):
        try:
            if os.path.exists(ALIASES_DB_PATH):
                with open(ALIASES_DB_PATH, 'r') as f:
                    self.aliases = json.load(f)
        except Exception as e:
            print(f"Error loading aliases: {e}")

    def save_aliases(self):
        try:
            with open(ALIASES_DB_PATH, 'w') as f:
                json.dump(self.aliases, f, indent=4)
        except Exception as e:
            print(f"Error saving aliases: {e}")

    def add_alias(self, alias: str, command: str):
        self.aliases[alias] = command
        self.save_aliases()

    def remove_alias(self, alias: str):
        if alias in self.aliases:
            del self.aliases[alias]
            self.save_aliases()
            return True
        return False

    def get_command(self, alias: str) -> str:
        return self.aliases.get(alias)

alias_manager = AliasManager()

@Client.on_message(fox_command("alias", "AliasManager", os.path.basename(__file__), "[add/del/list] [alias] [command]") & filters.me)
async def handle_aliases(client, message):
    args = message.text.split(maxsplit=3)
    
    if len(args) < 2:
        return await show_help(message)

    action = args[1].lower()

    if action == "add" and len(args) == 4:
        await add_alias(message, args[2], args[3])
    elif action == "del" and len(args) == 3:
        await remove_alias(message, args[2])
    elif action == "list":
        await list_aliases(message)
    else:
        await show_help(message)

async def show_help(message):
    help_text = (
        "<b>Manager:</b>\n"
        f"<code>{my_prefix()}alias add h help</code> - add alias\n"
        f"<code>{my_prefix()}del h</code> - delete alias\n"
        f"<code>{my_prefix()}list</code> - list aliases"
    )
    await message.edit(help_text)

async def add_alias(message, alias: str, command: str):
    if alias in alias_manager.aliases:
        await message.edit(f"❌ | Alias <code>{alias}</code> already exists")
    else:
        alias_manager.add_alias(alias, command)
        await message.edit(f"✅ | Alias <code>{alias}</code> for command <code>{command}</code> added \n🔄 | Rebooting...")
        await restart(message, restart_type="restart")

async def remove_alias(message, alias: str):
    if alias_manager.remove_alias(alias):
        await message.edit(f"✅ | Alias <code>{alias}</code> deleted \n🔄 | Rebooting...")
        await restart(message, restart_type="restart")

    else:
        await message.edit("❌ | Alias not found")

async def list_aliases(message):
    if not alias_manager.aliases:
        await message.edit("ℹ️ | Aliases not specified")
        return
    
    aliases_list = "\n".join(
        f"<code>{alias}</code> → <code>{cmd}</code>" 
        for alias, cmd in alias_manager.aliases.items()
    )
    await message.edit(f"<b>List aliases:</b>\n{aliases_list}")