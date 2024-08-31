from pyrogram import Client, filters
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os


def prestart(api_id, api_hash, device_mod):
    app = Client("my_account", api_id=api_id, api_hash=api_hash, device_model=device_mod)
    with app:
        
        if len(sys.argv) == 4:
            restart_type = sys.argv[3]
            if restart_type == "1":
                text = "<code>Update process completed!</code>"
            else:
                text = "**Userbot succesfully Restarted**"
            try:
                app.send_message(int(sys.argv[1]), text)
            except Exception as f:
                app.send_message("me", f"Got error: {f}\n\n" + text)

        # last.fm trigger
        if Path(f"temp/lastfm_autostart.txt").is_file():
            app.send_message("me", "last_fm_trigger_start", schedule_date=(datetime.now() + timedelta(seconds=70)))
