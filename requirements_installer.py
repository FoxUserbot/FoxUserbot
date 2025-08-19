import pip
import os
import sys
import logging
import subprocess
from contextlib import contextmanager
from shutil import which

logger = logging.getLogger('FoxUserbot')

def is_venv():
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def get_python_path():
    return sys.executable

@contextmanager
def _preserve_logging_handlers():
    root_logger = logging.getLogger()
    original_handlers = root_logger.handlers.copy()
    try:
        yield
    finally:
        for handler in root_logger.handlers[:]:
            if handler not in original_handlers:
                root_logger.removeHandler(handler)
        root_logger.handlers = original_handlers

def check_uv_installed(python_path):
    # check global uv
    uv_path = which("uv")
    if uv_path:
        try:
            subprocess.run([uv_path, "--version"], check=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return ("global", uv_path)
        except subprocess.CalledProcessError:
            pass
    
    # check uv python
    try:
        subprocess.run([python_path, "-m", "uv", "--version"], check=True,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return ("python_module", python_path)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return (None, None)

def install_library(name):
    packages = name.split() if isinstance(name, str) else name
    python_path = get_python_path()
    
    # check uv
    uv_type, uv_path = check_uv_installed(python_path)
    
    if uv_type:
        if uv_type == "global":
            uv_cmd = [uv_path, "pip", "install"] + packages
            if not is_venv():
                uv_cmd.append("--system")
        else:  # python_module
            uv_cmd = [uv_path, "-m", "uv", "pip", "install"] + packages
            if not is_venv() and os.name == "nt":
                uv_cmd.append("--system")
        
        with _preserve_logging_handlers():
            try:
                result = subprocess.run(uv_cmd, check=True).returncode
                logger.info(f"Installed with {uv_type} uv: {packages}")
                return True
            except subprocess.CalledProcessError:
                logger.warning(f"UV install failed, falling back to pip")
    
    # Fallback pip
    logger.warning(f"Trying built-in pip: {packages}")
    
    with _preserve_logging_handlers():
        try:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = open(os.devnull, 'w')
            sys.stderr = open(os.devnull, 'w')
            
            result = pip.main(["install"] + packages)
            
            if result == 0:
                logger.info(f"Installed with built-in pip: {packages}")
                return True
        except Exception as e:
            logger.warning(f"Built-in pip failed: {e}")
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        logger.warning(f"Trying pip via subprocess: {packages}")
        try:
            result = subprocess.run(
                [python_path, "-m", "pip", "install"] + packages,
                check=True
            ).returncode
            logger.info(f"Installed with pip (subprocess): {packages}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"All pip attempts failed: {packages}\nError: {e}")
            return False