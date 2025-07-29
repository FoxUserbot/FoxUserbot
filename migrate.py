import os
import re
from pathlib import Path

def convert_module(file_path):
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

def process_modules_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(root, file)
                convert_module(file_path)

def convert_modules():
    process_modules_directory("modules/plugins_2custom")

convert_modules()