import pip
import os
import sys
import logging
from contextlib import contextmanager

logger = logging.getLogger('FoxUserbot')

def is_venv():
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

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

def install_library(name):
    packages = name.split() if isinstance(name, str) else name
    
    uv_cmd = [sys.executable, "-m", "uv", "pip", "install"] + packages
    if not is_venv() and os.name == "nt":
        uv_cmd.append("--system")
    
    with _preserve_logging_handlers():
        uv_result = os.system(" ".join(uv_cmd))
    
    if uv_result == 0:
        logger.info(f"Installed successfully with uv: {packages}")
        return True
    
    logger.warning(f"Trying pip: {packages}")
    
    with _preserve_logging_handlers():
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        
        try:
            result = pip.main(["install"] + packages)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    
    if result == 0:
        logger.info(f"Installed successfully with pip: {packages}")
    else:
        logger.error(f"Failed: {packages}")
    
    return result == 0
