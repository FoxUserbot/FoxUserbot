from prefix import my_prefix
from pyrogram import filters
from modules.plugins_1system.settings.main_settings import module_list, file_list, add_command_help
from typing import Union, List
import json
import os


def load_aliases() -> dict:
    try:
        if os.path.exists("userdata/command_aliases.json"):
            with open("userdata/command_aliases.json", 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def fox_command(
    command: Union[str, List[str]], 
    module_name: str, 
    filename: str, 
    arguments: str = ""
) -> filters.Filter:
    commands = [command] if isinstance(command, str) else command.copy()
    aliases = load_aliases()

    alias_list = []
    for cmd in commands:
        for alias, target_cmd in aliases.items():
            if target_cmd.startswith(f"{my_prefix()}{cmd}") or target_cmd == cmd:
                alias_list.append(alias)
    
    all_commands = commands + alias_list
    
    help_text = " | ".join(f"{my_prefix()}{cmd} {arguments}".strip() for cmd in commands)
    if alias_list:
        help_text += f" (Aliases: {my_prefix()}{f', {my_prefix()}'.join(alias_list)})"
    
    add_command_help(module_name, help_text)
    file_list[module_name] = filename
    
    return filters.command(all_commands, prefixes=my_prefix())