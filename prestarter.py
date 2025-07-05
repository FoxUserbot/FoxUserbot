from pyrogram import Client, filters
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os
import asyncio


def prestart(api_id, api_hash, device_mod):
    from pyrogram.client import Client
    import asyncio

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    app = Client("my_account", api_id=api_id, api_hash=api_hash, device_model=device_mod)
    print("📝 Логирование: Проверка подключения к Telegram")
    
    async def check_connection():
        await app.connect()
        print("📝 Логирование: Подключение успешно")
        await app.disconnect()
        print("📝 Логирование: Отключение после проверки")
    
    loop.run_until_complete(check_connection())
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
