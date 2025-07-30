from prefix import my_prefix
from pyrogram import filters
from modules.plugins_1system.settings.main_settings import module_list, file_list, add_command_help
from typing import Union, List

def fox_command(
    command: Union[str, List[str]], 
    module_name: str, 
    filename: str, 
    arguments: str = ""
) -> filters.Filter:
    """
    Args:
        command: Command or List Commands
        module_name: Name module
        filename: filename
        arguments: Arguments after command
        
    Returns:
        filter command Pyrogram
    """
    commands = [command] if isinstance(command, str) else command.copy()

    help_text = " | ".join(
        f"{my_prefix()}{cmd} {arguments}".strip() 
        for cmd in commands
    )

    add_command_help(module_name, help_text)
    file_list[module_name] = filename
    
    return filters.command(commands, prefixes=my_prefix())
