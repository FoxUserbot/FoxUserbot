import os
from modules.plugins_1system.settings.main_settings import version
from prefix import my_prefix

from pystyle import  Write, Colors
os.system("cls" if os.name == "nt" else "clear")

Write.Print(f"""
╔═╗┌─┐─┐ ┬           
╠╣ │ │┌┴┬┘           
╚  └─┘┴ └─           
╦ ╦┌─┐┌─┐┬─┐┌┐ ┌─┐┌┬┐
║ ║└─┐├┤ ├┬┘├┴┐│ │ │ 
╚═╝└─┘└─┘┴└─└─┘└─┘ ┴ 
Github: https://github.com/FoxUserbot/FoxUserbot
Version: {version}
Prefix: {my_prefix()}
""", Colors.red_to_yellow, interval=0.0)

Write.Print(f"""[LOADER] Loading system modules...\n""", Colors.green_to_blue, interval=0.0)
