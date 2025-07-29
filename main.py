# -*- coding: utf-8 -*-
import logging
import pip
import os
import time
import sys
import re

from requirements_installer import install_library
from migrate import convert_modules

def check_structure():
    if os.path.exists("localhost_run_output.txt"):
        os.remove("localhost_run_output.txt")
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if not os.path.exists("userdata"):
        os.mkdir("userdata")
    if not os.path.exists("triggers"):
        os.mkdir("triggers")


def autoupdater():
    try:
        from pyrogram.client import Client
    except ImportError:
        try:
            os.remove("firstlaunch.temp")
        except OSError:
            pass

    first_launched = False
    try:
        with open("firstlaunch.temp", "r", encoding="utf-8") as f:
            if (f.readline().strip() == "1"):
                first_launched = True
    except FileNotFoundError:
        pass

    if not first_launched:
        pip.main(["uninstall", "pyrogram", "kurigram", "-y"])

        try:
            install_library('uv -U')
        except Exception as f:
            logger.warning(f)

        try:
            install_library('tgcrypto -U')
        except Exception as f:
            logger.warning(f)

        with open("firstlaunch.temp", "w", encoding="utf-8") as f:
            f.write("1")
    
    # install requirements for userbot
    install_library('-r requirements.txt -U')
    setup_logging()
    logger.info("Logging restored after installing dependencies")


async def start_userbot(app):
    await app.start()
    user = await app.get_me()
    import sys
    session_file = "my_account.session"
    if os.path.exists(session_file):
        logger.info("[Session]: Session already exists, restart not required")
    else:
        logger.info("[Session]: First authorization, restarting main script")
        if os.path.exists("localhost_run_output.txt"):
            os.remove("localhost_run_output.txt")
        os.execv(sys.executable, [sys.executable] + sys.argv)


def setup_logging():
    if "--safe" in sys.argv:
        log_file = 'temp/fox_userbot_safe.log'
        try:
            if os.path.exists("temp/fox_userbot_safe.log"):
                os.remove("temp/fox_userbot_safe.log")
        except:
            pass
    else:
        log_file = 'temp/fox_userbot.log'
        try:
            if os.path.exists("temp/fox_userbot.log"):
                os.remove("temp/fox_userbot.log")
        except:
            pass

    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    console_handler = logging.StreamHandler()
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.INFO)
    
    return root_logger


def userbot():
    from pyrogram.client import Client
    from configurator import my_api
    from prestarter import prestart
    from web_auth.web_auth import start_web_auth
    import os
    import sys
    import asyncio
    
    
    safe_mode = False
    if "--safe" in sys.argv:
        safe_mode = True
        logger.warning("[Userbot] Starting in safe mode (only system plugins)...")
        
    
    api_id, api_hash, device_mod = my_api()

    if not os.path.exists("my_account.session"):
        logger.warning("[Userbot] First launch! Authorization required...")  
        if "--cli" in sys.argv:
            logger.info("[Userbot] Running in CLI mode...")
            client = Client(
                "my_account",
                api_id=api_id,
                api_hash=api_hash,
                device_model=device_mod,
            ).run()
        else:      
            success, user = start_web_auth(api_id, api_hash, device_mod)
            
            if not success or user is None:
                logger.warning("[Userbot] Authorization failed! ")
                return
            else:
                if not os.path.exists("my_account.session"):
                    logger.warning("[Userbot] Restarting...")
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                    
                else:
                    logger.info("[Userbot] Session already exists, authorization not required")
    else:
        logger.info("[Userbot] Session already exists, authorization not required")
    
    prestart(api_id, api_hash, device_mod)

    try: # try start with custom modules
        client = Client(
            "my_account",
            api_id=api_id,
            api_hash=api_hash,
            device_model=device_mod,
            plugins=dict(root="modules" if not safe_mode else "modules/plugins_1system"),
        ).run()
    except Exception as e: # emergency mode
        if not safe_mode:
            logger.warning(f"[Userbot] Error detected: {e}")
            logger.warning(f"[Userbot] Restarting in safe mode (only system plugins)...")
            os.execv(sys.executable, [sys.executable] + sys.argv + ["--safe"])
        else:
            logger.warning(f"[Userbot] Critical error in safe mode: {e}")
            logging.critical(f"Critical error in safe mode: {e}")


if __name__ == "__main__":
    check_structure()
    convert_modules()
    logger = setup_logging()
    logger.info("Starting FoxUserbot...")
    autoupdater()
    userbot()
