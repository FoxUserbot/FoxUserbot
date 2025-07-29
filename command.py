def fox_command(command, module_name, filename, arguments=""):
    from prefix import my_prefix
    from pyrogram import filters
    from modules.plugins_1system.settings.main_settings import module_list, file_list, add_command_help
    import os

    command1 = command
    text = ""
    if isinstance(command1, list):
        command = []
        for i in command1:
            command.append(i)
            text += f"{my_prefix()}{i} {arguments} | "
    elif isinstance(command1, str):
        command = [command1]
        text += f"{my_prefix()}{command1} {arguments}"

    add_command_help(module_name, text)
    file_list[module_name] = filename
    return filters.command(command, prefixes=my_prefix())
