def fox_command(command1, Module_Name, names):
    from prefix import my_prefix
    from pyrogram import filters
    from modules.plugins_1system.settings.main_settings import module_list, file_list, add_command_help
    import os

    text = ""
    if isinstance(command1, list):
        print("list YES")
        command = []
        for i in command1:
            command.append(i)
            text += f"{my_prefix()}{i} | "
    elif isinstance(command1, str):
        print("str YES")
        command = [command1]
        text += f"{my_prefix()}{command1}"

    add_command_help(Module_Name, text)
    file_list[Module_Name] = names
    return filters.command(command, prefixes=my_prefix())
