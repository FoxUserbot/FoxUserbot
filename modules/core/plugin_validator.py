import os
import re
import logging
from pathlib import Path

class PluginValidator:
    def __init__(self):
        self.broken_dir = "broken_modules"
        self.loaded_dir = "modules/loaded"
        self._ensure_directories()
    
    def _ensure_directories(self):
        os.makedirs(self.broken_dir, exist_ok=True)
        os.makedirs(self.loaded_dir, exist_ok=True)
        os.makedirs("temp", exist_ok=True)
    
    def validate_and_convert_plugin(self, file_path, original_filename=None):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            try:
                compile(content, '<string>', 'exec')
            except SyntaxError as e:
                return False, None, f"Syntax error: {e}"
            
            if self._needs_conversion(content):
                content = self._convert_content(content, original_filename)
                try:
                    compile(content, '<string>', 'exec')
                except SyntaxError as e:
                    return False, None, f"Syntax error after conversion: {e}"
            
            final_filename = self._get_final_filename(original_filename or os.path.basename(file_path))
            final_path = os.path.join(self.loaded_dir, final_filename)
            
            with open(final_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, final_path, "Plugin validated and converted successfully"
            
        except Exception as e:
            logging.error(f"Validation error: {e}")
            return False, None, f"Validation error: {str(e)}"
    
    def validate_existing_plugins(self):
        if not os.path.exists(self.loaded_dir):
            logging.info("[PluginValidator] No plugins directory found")
            return
        
        valid_count = 0
        broken_count = 0
        
        for filename in os.listdir(self.loaded_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                file_path = os.path.join(self.loaded_dir, filename)
                success, _, message = self.validate_and_convert_plugin(file_path, filename)
                
                if success:
                    valid_count += 1
                    logging.info(f"[PluginValidator] Validated: {filename}")
                else:
                    broken_count += 1
                    logging.warning(f"[PluginValidator] Failed: {filename} - {message}")
        
        logging.info(f"[PluginValidator] Validation complete: {valid_count} valid, {broken_count} broken")
    
    def _needs_conversion(self, content):
        old_patterns = [
            r"module_list\['[^']+'\]",
            r"file_list\['[^']+'\]",
            r"filters\.command\([^)]*prefixes=my_prefix\(\)\)",
            r"from prefix import my_prefix",
            r"from modules\.plugins_1system",
        ]
        return any(re.search(pattern, content) for pattern in old_patterns)
    
    def _convert_content(self, content, filename):
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
        content = content.replace("from prefix import my_prefix", "from command import my_prefix")
        
        content = re.sub(
            r'filters\.command\(["\']([^"\']+)["\']\s*,\s*prefixes\s*=\s*my_prefix\(\)\)',
            lambda m: f'fox_command("{m.group(1)}", Module_Name, filename)',
            content
        )
        
        content = content.replace("message.command[", "message.text.split()[")
        
        return content
    
    def _get_final_filename(self, original_filename):
        name = Path(original_filename).stem
        name = re.sub(r'[()\s]', '_', name)
        return f"{name}.py"