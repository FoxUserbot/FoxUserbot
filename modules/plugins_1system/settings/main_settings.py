"""Please, ignore this file."""

version = "2.4.1.0"
module_list = {}
file_list = {}


def add_command_help(module_name, text):
    if module_name not in module_list:
        module_list[module_name] = []
    module_list[module_name].append(text)
