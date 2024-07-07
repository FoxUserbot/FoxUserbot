# -*- coding: utf-8 -*-
import logging
import pip
import os

requirements = [
    "install",
    "wheel",
    "telegraph",
    "pyrogram",
    "requests",
    "wget",
    "pystyle",
    "wikipedia",
    "gTTS",
    "beautifulsoup4",
    "--upgrade"
]


def check_structure():
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if not os.path.exists("temp/autoanswer_DB"):
        os.mkdir("temp/autoanswer_DB")


def autoupdater():
    pip.main(requirements)


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
