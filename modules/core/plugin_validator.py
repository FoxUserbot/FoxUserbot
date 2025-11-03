import logging
import os
import re
from pathlib import Path


class PluginValidator:
    def __init__(self):
        self.broken_dir = "broken_modules"
        self.loaded_dir = "modules/loaded"
        self._ensure_directories()
    
    def _ensure_directories(self):
        os.makedirs(self.broken_dir, exist_ok=True)
        os.makedirs(self.loaded_dir, exist_ok=True)
    
    def validate_and_convert_plugin(self, file_path, original_filename=None):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                original_content = f.read()
            
            if not self._validate_syntax(original_content):
                return False, None, "Syntax error in original plugin"
            
            validation_result = self._validate_content(original_content)
            if not validation_result[0]:
                return False, None, validation_result[1]
            
            if self._needs_conversion(original_content):
                converted_content = self._safe_convert_content(original_content, original_filename)
                if converted_content and self._validate_syntax(converted_content):
                    final_path = self._save_final_plugin(converted_content, original_filename)
                    return True, final_path, "Plugin converted successfully"
                else:
                    return False, None, "Conversion failed or resulted in syntax errors"
            
            final_path = self._save_final_plugin(original_content, original_filename)
            return True, final_path, "Plugin is valid"
            
        except Exception as e:
            logging.error(f"Validation error: {e}")
            return False, None, f"Validation error: {str(e)}"
    
    def _needs_conversion(self, content):
        old_patterns = [
            r"module_list\['[^']+'\]",
            r"file_list\['[^']+'\]",
            r"filters\.command\([^)]*prefixes=my_prefix\(\)\)",
            r"from prefix import my_prefix",
        ]
        
        return any(re.search(pattern, content) for pattern in old_patterns)
    
    def _safe_convert_content(self, content, filename):
        try:
            module_name_match = re.search(r"module_list\['([^']+)'\]", content)
            module_name = module_name_match.group(1) if module_name_match else Path(filename).stem
            
            content = re.sub(r"module_list\['[^']+'\].*?\n", "", content)
            content = re.sub(r"file_list\['[^']+'\].*?\n", "", content)
            
            if "from command import fox_command" not in content:
                lines = content.splitlines()
                insert_pos = 0
                for i, line in enumerate(lines):
                    if line.strip() and not line.startswith(('import ', 'from ')):
                        insert_pos = i
                        break
                
                new_imports = ["from command import fox_command", "import os", ""]
                lines[insert_pos:insert_pos] = new_imports
                content = '\n'.join(lines)
            
            if "filename = os.path.basename(__file__)" not in content:
                lines = content.splitlines()
                insert_pos = 0
                for i, line in enumerate(lines):
                    if line.strip() and not line.startswith(('import ', 'from ')):
                        insert_pos = i
                        break
                
                new_code = [f"filename = os.path.basename(__file__)", f"Module_Name = '{module_name}'", ""]
                lines[insert_pos:insert_pos] = new_code
                content = '\n'.join(lines)
            
            content = content.replace("from modules.plugins_1system", "from modules.core")
            content = content.replace("import modules.plugins_1system", "import modules.core")
            
            content = re.sub(
                r'filters\.command\(["\']([^"\']+)["\']\s*,\s*prefixes\s*=\s*my_prefix\(\)\)',
                lambda m: f'fox_command("{m.group(1)}", Module_Name, filename)',
                content
            )
            
            # Заменяем импорты
            content = content.replace("from prefix import my_prefix", "from command import my_prefix")
            
            # Простые замены без сложной логики
            content = content.replace("message.command[", "message.text.split()[")
            
            return content
        
        except Exception as e:
            logging.error(f"Conversion error: {e}")
            return None
    
    def _validate_syntax(self, content):
        try:
            compile(content, '<string>', 'exec')
            return True
        except SyntaxError as e:
            logging.error(f"Syntax error at line {e.lineno}: {e.msg}")
            return False
    
    def _validate_content(self, content):
        if "@Client.on_message" not in content:
            return False, "No message handlers found"
        
        if "from pyrogram" not in content and "import pyrogram" not in content:
            return False, "Pyrogram imports not found"
        
        return True, "Content validation passed"
    
    def _save_final_plugin(self, content, original_filename):
        final_filename = self._get_final_filename(original_filename)
        final_path = os.path.join(self.loaded_dir, final_filename)
        
        with open(final_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return final_path
    
    def _get_final_filename(self, original_filename):
        name = Path(original_filename).stem
        name = re.sub(r'[()\s]', '_', name)
        return f"{name}.py"
    
    def validate_existing_plugins(self):
        if not os.path.exists(self.loaded_dir):
            return
        
        valid_count = 0
        broken_count = 0
        
        for filename in os.listdir(self.loaded_dir):
            if filename.endswith('.py'):
                file_path = os.path.join(self.loaded_dir, filename)
                success, new_path, message = self.validate_and_convert_plugin(file_path, filename)
                
                if success:
                    valid_count += 1
                    logging.info(f"Validated plugin: {filename}")
                else:
                    broken_count += 1
                    logging.warning(f"Plugin failed validation: {filename} - {message}")
        
        logging.info(f"Plugin validation completed: {valid_count} valid, {broken_count} broken")