from pyrogram import Client
from colorama import Fore

plugins = dict(root="plugins")

Client("my_account", plugins=plugins).run()