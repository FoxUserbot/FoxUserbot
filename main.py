# -*- coding: utf-8 -*-
import logging
import pip
import os
import time

requirements_install = [
    "install",
    "wheel",
    "telegraph",
    "wget",
    "pystyle",
    "flask",
    "--upgrade",
]


def check_structure():
    if os.path.exists("localtunnel_output.txt"):
        os.remove("localtunnel_output.txt")
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
        with open("firstlaunch.temp", "w", encoding="utf-8") as f:
            f.write("1")

    pip.main(requirements_install)
    pip.main(["install", "kurigram==2.1.37"]) # Куримузон мудила не ломай ебучий куриграм



def logger():
    logging.basicConfig(
        filename="temp/fox_userbot.log",
        filemode="w",
        format="%(asctime)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        level=logging.INFO
    )



async def start_userbot(app):
    await app.start()
    user = await app.get_me()
    import sys
    session_file = "my_account.session"
    if os.path.exists(session_file):
        print("📝 Logging: Session already exists, restart not required")
    else:
        print("📝 Logging: First authorization, restarting main script")
        if os.path.exists("localtunnel_output.txt"):
            os.remove("localtunnel_output.txt")
        os.execv(sys.executable, [sys.executable] + sys.argv)


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
        print("🦊 Starting in safe mode (only system plugins)...")
    
    
    api_id, api_hash, device_mod = my_api()

    if not os.path.exists("my_account.session"):
        print("🦊 First launch! Authorization required...")  
        if "--cli" in sys.argv:
            print("🦊 Running in CLI mode...")
            client = Client(
                "my_account",
                api_id=api_id,
                api_hash=api_hash,
                device_model=device_mod,
            )
            client.start()
            client.stop()
        else:      
            success, user = start_web_auth(api_id, api_hash, device_mod)
            
            if not success or user is None:
                print("❌ Authorization failed! ")
                return
            else:
                if not os.path.exists("my_account.session"):
                    print("📝 Restarting...")
                    if os.path.exists("localtunnel_output.txt"):
                        os.remove("localtunnel_output.txt")
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                    
                else:
                    print("🦊 Session already exists, authorization not required")
    else:
        print("🦊 Session already exists, authorization not required")
    
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
            print(f"🦊 Error detected: {e}")
            print("🦊 Restarting in safe mode (only system plugins)...")
            os.execv(sys.executable, [sys.executable] + sys.argv + ["--safe"])
        else:
            print(f"🦊 Critical error in safe mode: {e}")
            logging.critical(f"Critical error in safe mode: {e}")


if __name__ == "__main__":
    check_structure()
    logger()
    autoupdater()
    userbot()
