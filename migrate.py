import os
import re
from pathlib import Path

def convert_module_new_format(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    module_name_match = re.search(r"module_list\['([^']+)'\]", content)
    if not module_name_match:
        return
    
    module_name = module_name_match.group(1)
    
    content = re.sub(r"module_list\['[^']+'\].*?\n", "", content)
    content = re.sub(r"file_list\['[^']+'\].*?\n", "", content)
    
    content = re.sub(r"^from command import fox_command\s*\n?", "", content, flags=re.MULTILINE)
    content = re.sub(r"^import os\s*\n?", "", content, flags=re.MULTILINE)
    
    new_imports = "from command import fox_command\nimport os\n\n"
    content = new_imports + content.lstrip()
    
    if "filename = os.path.basename(__file__)" not in content:
        insert_pos = 0
        lines = content.splitlines(keepends=True)
        
        for i, line in enumerate(lines):
            if not line.strip() or line.startswith(("from ", "import ")):
                continue
            insert_pos = i
            break
        
        new_code = "filename = os.path.basename(__file__)\nModule_Name = '{}'\n\n".format(module_name)
        content = "".join(lines[:insert_pos] + [new_code] + lines[insert_pos:])
    
    content = re.sub(
        r'filters\.command\(([\'"\[\]])([^\)]+)\1\s*,\s*prefixes\s*=\s*my_prefix\(\)\)',
        lambda m: f'fox_command({m.group(1)}{m.group(2)}{m.group(1)}, Module_Name, filename)',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"File {file_path} converted!")

def convert_module_filters_me(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Проверяем наличие необходимых импортов
    has_fox_sudo = "fox_sudo" in content
    has_who_message = "who_message" in content
    has_fox_command = "fox_command" in content

    # Умное добавление импортов
    if "from command import" in content and not (has_fox_sudo and has_who_message):
        content = re.sub(
            r'(from command import)([^\n]*)',
            lambda m: m.group(0) + 
                     ('' if has_fox_sudo else ', fox_sudo') + 
                     ('' if has_who_message else ', who_message'),
            content,
            count=1
        )
        # Обновляем флаги после добавления импортов
        has_fox_sudo = has_fox_sudo or "fox_sudo" in content
        has_who_message = has_who_message or "who_message" in content
    
    # Заменяем только filters.me без ~ перед ним
    if has_fox_sudo:
        def safe_replace(match):
            before = match.group(1)
            after = match.group(2)
            if not before.rstrip().endswith('~'):
                if after and after[0] in (' ', '&', '|', ')', '\n'):
                    return f'@Client.on_message({before}fox_sudo(){after}'
            return match.group(0)
        
        content = re.sub(
            r'@Client\.on_message\((.*?)filters\.me([^a-zA-Z0-9_]*)',
            safe_replace,
            content
        )
    
    # Умное добавление who_message в функции
    if has_who_message:
        def add_who_message(match):
            decorator = match.group(1)
            func_block = match.group(2)
            
            # Проверяем, есть ли fox_command в декораторе
            needs_who_message = "fox_command" in decorator
            
            if needs_who_message and 'message = await who_message(client, message)' not in func_block:
                func_block = func_block.replace("message = await who_message(client, message)", "message = await who_message(client, message, message.reply_to_message)")
                if needs_who_message and 'message = await who_message(client, message, message.reply_to_message)' not in func_block:
                    func_block = re.sub(
                        r'(async def \w+\(client, message\):\n)',
                        r'\1    message = await who_message(client, message, message.reply_to_message)\n',
                        func_block,
                        count=1
                    )
            return decorator + func_block
        
        content = re.sub(
            r'(@Client\.on_message\(.*?\)\n)(async def \w+\(client, message\):[\s\S]*?(?=\n\n|\Z))',
            add_who_message,
            content
        )
    
    content = content.replace("message.command[", "message.text.split()[")
    content = content.replace("message = await who_message(client, message)", "message = await who_message(client, message, message.reply_to_message)")
                
    content = re.sub(
        r'async def (\w+)\(client: Client, message: Message\)',
        r'async def \1(client, message)',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def process_modules_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(root, file)
                convert_module_new_format(file_path)
                convert_module_filters_me(file_path)

def convert_modules():
    process_modules_directory("modules/plugins_2custom")

convert_modules()