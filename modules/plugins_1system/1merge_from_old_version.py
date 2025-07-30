from pystyle import Write, Colors
import random
import os
import shutil
import wget
from modules.plugins_1system.restarter import restart_executor

# 1.0 > 2.0
if os.path.isdir("plugins"):
    i = random.randint(10000, 99999)
    os.rename("plugins", f"modules_old_{i}")
    print(f"""[WARNING] Old incompatible modules (modules_old_{i}) detected!
[WARNING] Please rewrite them in a new format and upload them to the
[WARNING] ==> .modules/plugins_2custom directory\n""")

# 2.1 > 2.2
if os.path.exists("modules/plugins_1system/support.py"):
    os.remove("modules/plugins_1system/support.py")

# 2.2 > 2.3
if os.path.isdir("temp/autoanswer_DB"):
    shutil.move("temp/autoanswer_DB", "userdata/autoanswer_DB")
if os.path.exists("temp/autoanswer"):
    os.replace("temp/autoanswer", "userdata/autoanswer")
if os.path.exists("temp/lastfm_username.txt"):
    os.replace("temp/lastfm_username.txt", "userdata/lastfm_username")
if os.path.exists("temp/lastfm_current_song.txt"):
    os.replace("temp/lastfm_current_song.txt", "userdata/lastfm_current_song")
if os.path.exists("temp/lastfm_channel.txt"):
    os.replace("temp/lastfm_channel.txt", "userdata/lastfm_channel")
if os.path.exists("temp/lastfm_id_in_channel_telegram.txt"):
    os.replace("temp/lastfm_id_in_channel_telegram.txt", "userdata/lastfm_id_in_channel_telegram")
if os.path.exists("temp/lastfm_autostart.txt"):
    os.replace("temp/lastfm_autostart.txt", "triggers/lastfm_autostart")
    autostartF = open("triggers/lastfm_autostart", "w+", encoding="utf-8")
    autostartF.write("last_fm_trigger_start")
    autostartF.close()

# 2.2 > 2.3
# modules
modules = ["user_info.py", "weather.py", "webshot.py", "wikipedia.py", "switch.py", "tagall.py",
           "time_now.py", "type.py", "stats.py", "spamban.py", "spam.py", "speech.py", "short.py",
           "sendToId.py", "qr.py", "quotes.py", "reputation.py", "premium_text.py", "progressbar.py",
           "purge.py", "ignore.py", "kickall.py", "ladder.py", "lastfm.py", "link.py",
           "find_music.py", "gen_pass.py", "hearts.py", "afk.py", "autoanswer.py", "autoonline.py",
           "autoread.py", "chance.py", "demotivator.py"]
modules_value = 0
for _ in modules:
    try:
        if os.path.exists(f"modules/plugins_1system/{_}"):
            link = f"https://raw.githubusercontent.com/FoxUserbot/CustomModules/refs/heads/main/{_}"
            wget.download(link, f"temp/{_}")
            os.replace(f"temp/{_}", f"modules/plugins_2custom/{_}")
            os.remove(f"modules/plugins_1system/{_}")
            modules_value += 1
    except Exception as fff:
        print(fff)
if modules_value >= 1:
    restart_executor()

# 2.3 > 2.3.3
if os.path.exists("first_launch.bat"):
    os.remove("first_launch.bat")
if os.path.exists("check.py"):
    os.remove("check.py")
if os.path.exists("help_first_launch.py"):
    os.remove("help_first_launch.py")

# 2.3.3 > 2.3.4
if os.path.exists("config.ini"):
    os.replace("config.ini", "userdata/config.ini")
    restart_executor()

# 2.3.5 > 2.4
if os.path.isdir("modules/plugins_3finished"):
    shutil.rmtree("modules/plugins_3finished")
    os.remove("firstlaunch.temp")
    restart_executor()

if os.path.exists("logo.png"):
    os.remove("logo.png")
