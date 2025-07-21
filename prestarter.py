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
    print("📝 Logging: Checking connection to Telegram")
    
    async def check_connection():
        await app.connect()
        print("📝 Logging: Connection successful")
        await app.disconnect()
        print("📝 Logging: Disconnection after checking")
    
    loop.run_until_complete(check_connection())
    with app:
        if len(sys.argv) >= 4:
            restart_type = sys.argv[3]
            thread_id = None
            if len(sys.argv) >= 5 and sys.argv[4] != "None":
                try:
                    thread_id = int(sys.argv[4])
                except ValueError:
                    thread_id = None
                    
            if restart_type == "1":
                text = "<code>Update process completed!</code>"
            else:
                text = "**Userbot succesfully Restarted**"
            try:
                app.send_message(int(sys.argv[1]), text, message_thread_id=thread_id)
            except Exception as f:
                app.send_message("me", f"Got error: {f}\n\n" + text)
                
        # check triggers
        for i in os.listdir("triggers"):
            with open(f"triggers/{i}", 'r') as f:
                text = f.read().strip()
                app.send_message("me", text, schedule_date=(datetime.now() + timedelta(seconds=70)))
