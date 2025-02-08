# -*- coding: utf-8 -*-
import logging
import pip
import os

requirements_install = [
    "install",
    "wheel",
    "telegraph",
    "kurigram",
    "requests",
    "wget",
    "pystyle",
    "wikipedia",
    "gTTS",
    "lyricsgenius",
    "--upgrade"
]


def check_structure():
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if not os.path.exists("temp/autoanswer_DB"):
        os.mkdir("temp/autoanswer_DB")


def autoupdater():
    # Check pyrogram and kurigram
    try:
        from pyrogram import Client
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


def userbot():
    from pyrogram import Client
    from configurator import my_api
    from prestarter import prestart
    api_id, api_hash, device_mod = my_api()
    prestart(api_id, api_hash, device_mod)

    Client = Client(
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
