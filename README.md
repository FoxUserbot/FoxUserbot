<p align="center">
    <img src="photos/logo.png" width="500" alt="FoxUserbot">
    </a>
    <br>
    <b>FoxUserbot 2.4</b>
    <br>
    <b>Telegram userbot with the easiest installation</b>
    <br>
    <b>Used Kurigram (Fork Pyrogram)</b>
    <br>
    <a href='https://github.com/FoxUserbot/CustomModules'>
        Custom modules
    </a>
<br><br>
<a href="https://github.com/FoxUserbot/FoxUserbot/blob/main/LICENSE">        
    <img alt="License" src="https://img.shields.io/github/license/FoxUserbot/FoxUserbot?style=for-the-badge">
</a>

<a href="https://github.com/FoxUserbot/FoxUserbot/commits/main">
    <img alt="last-commit" src="https://img.shields.io/github/last-commit/FoxUserbot/FoxUserbot?style=for-the-badge">
</a>

<a href="https://github.com/FoxUserbot/FoxUserbot/issues">        
    <img alt="Issues" src="https://img.shields.io/github/issues/FoxUserbot/FoxUserbot?style=for-the-badge">
</a>

<a href="https://github.com/FoxUserbot/FoxUserbot">
    <img alt="CodeFactor" src="https://www.codefactor.io/repository/github/FoxUserbot/FoxUserbot/badge?style=for-the-badge">
    <img alt="Stars" src="https://img.shields.io/github/stars/FoxUserbot/FoxUserbot?style=for-the-badge">
    <img alt="Size" src="https://img.shields.io/github/repo-size/FoxUserbot/FoxUserbot?style=for-the-badge">
    <img alt="Language" src="https://img.shields.io/github/languages/top/FoxUserbot/FoxUserbot?style=for-the-badge">
    <img alt="Python" src="https://img.shields.io/badge/python->=%203.7-blue?style=for-the-badge">
</a>

</p>

<h1>Custom modules</h1>

<p>To add your module to the bot, create a pull request in the <a href='https://github.com/FoxUserbot/CustomModules/'>custom_modules</a> repository</p>

```python3
from pyrogram import Client, filters
from command import fox_command
import os

# If you need to install an external module via pip
# import the following line of code and install the library with the required parameter
#
# from requirements_installer import install_library
# install_library("requests -U") 
#
# ^^^ pip3 install requests -U
#
# =================================================
#
# from requirements_installer import install_library
# install_library("requests==2.32.3") 
#
# ^^^ pip3 install requests==2.32.3
#
# =================================================
#
# if you need to call any command after restarting
# with open("triggers/example_autostart", "w", encoding="utf-8") as f:
#        f.write("example_edit")
#        ^^^ enter the command that should be run after the userbot is restarted
#
# if you need write data config
# with open("userdata/example_config", "w", encoding="utf-8") as f:
#        f.write("example_data")
#        ^^^ enter the need data


# fox_command(command, module_name, filename=os.path.basename(__file__), "[Arguments]"
@Client.on_message(fox_command("example", "Example", os.path.basename(__file__), "[Arguments]") & filters.me)
async def example_edit(client, message):
    await message.edit("<code>This is an example module</code>")


```

<h2>How to add Hikka/Heroku modules?</h2>

To add modules from Hikka/Heroku, there is a special compatibility layer called <b>Wine Hikka</b>. To use it, download the module file itself from the <a href='https://github.com/FoxUserbot/CustomModules'>modules repository</a> and reply to the Hikka module with <code>[prefix]wine_hikka</code> or <code>[prefix]wine_hikka [link]</code>.

AI will automatically convert the module from Telethon to Pyrogram for this UserBot, save it in the <code>modules/plugins_2custom/</code> folder and restart it.

<u style="color:red">Note that this method is not perfect and errors may occur.</u>

<h1>Install and Start</h1>
<h2>How to install?</h2>

- Termux

```
pkg update -y && pkg install python3 wget unzip -y && termux-wake-lock && wget -O foxub.$$ https://github.com/FoxUserbot/FoxUserbot/archive/refs/heads/main.zip && (unzip foxub.$$ && rm -rf foxub.$$ && cd FoxUserbot-main && python3 -m venv venv && source venv/bin/activate && python3 main.py)
```
> [!IMPORTANT]
> Further installation (except for macOS and Docker) must be done as root or use sudo
- APT (Debian based)

```
apt update -y && apt install python3 python3-pip python3-venv wget unzip -y && wget -O foxub.$$ https://github.com/FoxUserbot/FoxUserbot/archive/refs/heads/main.zip && (unzip foxub.$$ && rm -rf foxub.$$ && cd FoxUserbot-main && python3 -m venv venv && source venv/bin/activate && python3 main.py)
```

- Astra Linux (if python < 3.7, else go to "Debian based")

```
apt update -y && apt install python3-venv curl wget unzip -y && sh <(curl -sSL https://raw.githubusercontent.com/FoxUserbot/FoxUserbot/main/HowToGetPython3_8.sh) && wget -O foxub.$$ https://github.com/FoxUserbot/FoxUserbot/archive/refs/heads/main.zip && (unzip foxub.$$ && rm -rf foxub.$$ && cd FoxUserbot-main && python3 -m venv venv && source venv/bin/activate && python3 main.py)
```

- YUM (RHEL based)

```
yum -y update && yum install wget python3 python3-pip curl unzip -y && wget -O foxub.$$ https://github.com/FoxUserbot/FoxUserbot/archive/refs/heads/main.zip && (unzip foxub.$$ && rm -rf foxub.$$ && cd FoxUserbot-main && python3 -m venv venv && source venv/bin/activate && python3 main.py)
```

- PACMAN (Arch based)

```
pacman -Sy python3 python-pip wget curl unzip && wget -O foxub.$$ https://github.com/FoxUserbot/FoxUserbot/archive/refs/heads/main.zip && (unzip foxub.$$ && rm -rf foxub.$$ && cd FoxUserbot-main && python3 -m venv venv && source venv/bin/activate && python3 main.py)
```

- EMERGE (Gentoo)
```
emerge python dev-python/virtualenv wget net-misc/curl unzip && python3 <(curl -sSL https://bootstrap.pypa.io/get-pip.py) && wget -O foxub.$$ https://github.com/FoxUserbot/FoxUserbot/archive/refs/heads/main.zip && (unzip foxub.$$ && rm -rf foxub.$$ && cd FoxUserbot-main && python3 -m venv venv && source venv/bin/activate && python3 main.py)
```

- MacOS

```
xcode-select --install ; /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)" && brew install python3 && pip3 install --upgrade pip && pip3 install wheel && brew install wget unzip && wget -O foxub.$$ https://github.com/FoxUserbot/FoxUserbot/archive/refs/heads/main.zip && (unzip foxub.$$ && rm foxub.$$ && cd FoxUserbot-main && python3 -m venv venv && source venv/bin/activate && python3 main.py)
```
- Docker

```
docker build -t foxuserbot .
docker run -it foxuserbot
```
> [!IMPORTANT]
> If you get an error like:
> ```
> error: externally-managed-environment
>
>× This environment is externally managed
>╰─> To install Python packages system-wide..
>```
>Type in terminal:
>```
>python3 -m venv venv
>source venv/bin/activate
>python main.py
>```

<h4>How to start?</h3>

```
termux-wake-lock ; cd FoxUserbot-main && python3 main.py
```

<h3>Windows</h2>
<h4>Install</h3>

- Install <a href="https://www.python.org/downloads/">python3</a>

- Download and Unzip <a href="https://github.com/FoxUserbot/FoxUserbot/archive/refs/heads/main.zip">This file</a>

- Open main.py

<h4>How to start</h3>

- Open windows.bat

<h2>How to start in repl.it?</h2>
<a href="https://replit.com/@A9-FMFM/FoxUserbot"><img alt="Run on Repl.it" src="https://replit.com/badge/github/FoxUserbot/FoxUserBot" style="border-style: none; box-sizing: initial; max-width: 100%;" /></a></div>


<h1>Groups and support</h1>
<a href="https://t.me/foxteam0">
<img alt="Telegram" src="https://img.shields.io/badge/Telegram_Channel-0a0a0a?style=for-the-badge&logo=telegram">
</a>

---

<p>We will steal your sessions and publish them on our Telegram channel :)</p>
