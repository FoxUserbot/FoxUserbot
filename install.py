import os
from colorama import Fore
import time
from plugins.settings.main_settings import requirements_list

os.system("pip3 install -U pyrogram")
for rq in requirements_list:
    os.system(f"pip3 install {rq}")
    
os.system("cls" if os.name == "nt" else "clear")

print(Fore.GREEN + "Привет. Добро пожаловать в установщик FoxUserBot.")
time.sleep(1)
print(Fore.GREEN + "Для продолжения вам потребуються данные такие как api-id, и api-hash. Их можно найти на сайте my.telegram.org")
api_id = input(Fore.GREEN + "Введите ваш api-id >>> ")
api_hash = input(Fore.GREEN + "Введите api hash >>> ")
config = open('config.ini', '+w')
config.write(f"""[pyrogram]
api_id = {api_id}
api_hash = {api_hash}""")
config.close()
print(Fore.GREEN + "Спасибо. Данные сохранены. Сейчас вам предложат ввести номер телефона и код входа от вашего аккаунта в Telegram, сделайте это для установки FoxUserBot.")
os.system("python3 main.py")
