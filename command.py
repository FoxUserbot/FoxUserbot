import configparser
import json
import os
from pathlib import Path
from typing import List, Union

from pyrogram import filters
from pyrogram.types import ReplyParameters

from modules.core.settings.main_settings import (add_command_help,
                                                            file_list)


def my_prefix():
    PATH_FILE = "userdata/config.ini"

    config = configparser.ConfigParser()
    config.read(PATH_FILE)
    try:
        prefix = config.get("prefix", "prefix")
    except:
        config.add_section("prefix")
        config.set("prefix", "prefix", "!")
        with open(PATH_FILE, "w") as config_file:
            config.write(config_file)
        prefix = "!"
    return prefix


def load_aliases() -> dict:
    try:
        if os.path.exists("userdata/command_aliases.json"):
            with open("userdata/command_aliases.json", 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


async def who_message(client, message):
    me = await client.get_me()
    if message.from_user.id == me.id:
        return message
    else:
        try:
            reply_id = message.reply_to_message.id
        except:
            reply_id = message.id
        return await client.send_message(
            message.chat.id, 
            message.text, 
            message_thread_id=message.message_thread_id,
            reply_parameters=ReplyParameters(message_id=reply_id)
        )

def fox_sudo():
    sudo_file = Path("userdata/sudo_users.json")
    sudo_users_list = []
    try:
        with open(sudo_file, 'r', encoding='utf-8') as f:
            sudo_users_list = json.load(f)
            i = (filters.user(sudo_users_list) or filters.chat(sudo_users_list))
            return i
    except:
        return filters.me


def fox_command(
    command: Union[str, List[str]], 
    module_name: str, 
    filename: str, 
    arguments: str = ""
) -> filters.Filter:
    module_name = module_name.replace(" ", "_")
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
