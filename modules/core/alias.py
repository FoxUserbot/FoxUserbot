# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path
from typing import Dict, List

from pyrogram import Client

from command import fox_command, fox_sudo, who_message, get_text, my_prefix
from modules.core.restarter import restart

ALIASES_DB_PATH = "userdata/command_aliases.json"

LANGUAGES = {
    "en": {
        "help": """<emoji id='5283051451889756068'>🦊</emoji> <b>Manager:</b>
<code>{prefix}alias add h help</code> - add alias
<code>{prefix}alias del h</code> - delete alias
<code>{prefix}alias list</code> - list aliases""",
        "alias_exists": "<emoji id='5210952531676504517'>❌</emoji> | Alias <code>{alias}</code> already exists",
        "alias_added": "<emoji id='5237699328843200968'>✅</emoji> | Alias <code>{alias}</code> for command <code>{command}</code> added \n<emoji id='5264727218734524899'>🔄</emoji> | Rebooting...",
        "alias_deleted": "<emoji id='5237699328843200968'>✅</emoji> | Alias <code>{alias}</code> deleted \n<emoji id='5264727218734524899'>🔄</emoji> | Rebooting...",
        "alias_not_found": "<emoji id='5210952531676504517'>❌</emoji> | Alias not found",
        "no_aliases": "<emoji id='5278753302023004775'>ℹ️</emoji> | Aliases not specified",
        "list_title": "<emoji id='5283051451889756068'>🦊</emoji> <b>List aliases:</b>\n{aliases_list}"
    },
    "ru": {
        "help": """<emoji id='5283051451889756068'>🦊</emoji> <b>Менеджер:</b>
<code>{prefix}alias add h help</code> - добавить алиас
<code>{prefix}alias del h</code> - удалить алиас
<code>{prefix}alias list</code> - список алиасов""",
        "alias_exists": "<emoji id='5210952531676504517'>❌</emoji> | Алиас <code>{alias}</code> уже существует",
        "alias_added": "<emoji id='5237699328843200968'>✅</emoji> | Алиас <code>{alias}</code> для команды <code>{command}</code> добавлен \n<emoji id='5264727218734524899'>🔄</emoji> | Перезагружаю...",
        "alias_deleted": "<emoji id='5237699328843200968'>✅</emoji> | Алиас <code>{alias}</code> удален \n<emoji id='5264727218734524899'>🔄</emoji> | Перезагружаю...",
        "alias_not_found": "<emoji id='5210952531676504517'>❌</emoji> | Алиас не найден",
        "no_aliases": "<emoji id='5278753302023004775'>ℹ️</emoji> | Алиасы не указаны",
        "list_title": "<emoji id='5283051451889756068'>🦊</emoji> <b>Список алиасов:</b>\n{aliases_list}"
    },
    "ua": {
        "help": """<emoji id='5283051451889756068'>🦊</emoji> <b>Менеджер:</b>
<code>{prefix}alias add h help</code> - додати аліас
<code>{prefix}alias del h</code> - видалити аліас
<code>{prefix}alias list</code> - список аліасів""",
        "alias_exists": "<emoji id='5210952531676504517'>❌</emoji> | Аліас <code>{alias}</code> вже існує",
        "alias_added": "<emoji id='5237699328843200968'>✅</emoji> | Аліас <code>{alias}</code> для команди <code>{command}</code> додано \n<emoji id='5264727218734524899'>🔄</emoji> | Перезавантажую...",
        "alias_deleted": "<emoji id='5237699328843200968'>✅</emoji> | Аліас <code>{alias}</code> видалено \n<emoji id='5264727218734524899'>🔄</emoji> | Перезавантажую...",
        "alias_not_found": "<emoji id='5210952531676504517'>❌</emoji> | Аліас не знайдено",
        "no_aliases": "<emoji id='5278753302023004775'>ℹ️</emoji> | Аліаси не вказані",
        "list_title": "<emoji id='5283051451889756068'>🦊</emoji> <b>Список аліасів:</b>\n{aliases_list}"
    }
}

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

@Client.on_message(fox_command("alias", "AliasManager", os.path.basename(__file__), "[add/del/list] [alias] [command]") & fox_sudo())
async def handle_aliases(client, message):
    message = await who_message(client, message)
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
    help_text = get_text("alias", "help", LANGUAGES=LANGUAGES, prefix=my_prefix())
    await message.edit(help_text)

async def add_alias(message, alias: str, command: str):
    if alias in alias_manager.aliases:
        exists_text = get_text("alias", "alias_exists", LANGUAGES=LANGUAGES, alias=alias)
        await message.edit(exists_text)
    else:
        alias_manager.add_alias(alias, command)
        added_text = get_text("alias", "alias_added", LANGUAGES=LANGUAGES, alias=alias, command=command)
        await message.edit(added_text)
        await restart(message, restart_type="restart")

async def remove_alias(message, alias: str):
    if alias_manager.remove_alias(alias):
        deleted_text = get_text("alias", "alias_deleted", LANGUAGES=LANGUAGES, alias=alias)
        await message.edit(deleted_text)
        await restart(message, restart_type="restart")
    else:
        not_found_text = get_text("alias", "alias_not_found", LANGUAGES=LANGUAGES)
        await message.edit(not_found_text)

async def list_aliases(message):
    if not alias_manager.aliases:
        no_aliases_text = get_text("alias", "no_aliases", LANGUAGES=LANGUAGES)
        await message.edit(no_aliases_text)
        return
    
    aliases_list = "\n".join(
        f"<code>{alias}</code> → <code>{cmd}</code>" 
        for alias, cmd in alias_manager.aliases.items()
    )

    list_text = get_text("alias", "list_title", LANGUAGES=LANGUAGES, aliases_list=aliases_list)
    await message.edit(list_text)