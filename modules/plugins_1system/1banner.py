import logging
import os

from pystyle import Colors, Write

from modules.plugins_1system.settings.main_settings import version
from prefix import my_prefix

logger = logging.getLogger('FoxUserbot')

def show_banner():
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
Prefix: {my_prefix()}\n""", Colors.red_to_yellow, interval=0)
    
    logger.info("[LOADER] Loading system modules...")

show_banner()
