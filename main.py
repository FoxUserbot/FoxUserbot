# -*- coding: utf-8 -*-
import logging
import pip
import os

requirements_install = [
    "install",
    "wheel",
    "telegraph",
    "requests",
    "wget",
    "pystyle",
    "wikipedia",
    "gTTS",
    "kurigram",
    "lyricsgenius",
    "flask",
    "--upgrade",
]


def check_structure():
    if os.path.exists("localtunnel_output.txt"):
        os.remove("localtunnel_output.txt")
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if not os.path.exists("temp/autoanswer_DB"):
        os.mkdir("temp/autoanswer_DB")


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
    
    api_id, api_hash, device_mod = my_api()

    if not os.path.exists("my_account.session"):
        print("🦊 First launch! Authorization required...")        
        success, user = start_web_auth(api_id, api_hash, device_mod)
        
        if not success or user is None:
            print("❌ Authorization failed!")
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

    client = Client(
        "my_account",
        api_id=api_id,
        api_hash=api_hash,
        device_model=device_mod,
        plugins=dict(root="modules"),
    ).run()


if __name__ == "__main__":
    check_structure()
    logger()
    autoupdater()
    userbot()
