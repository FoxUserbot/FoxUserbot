from pyrogram import Client, filters
from command import fox_command
import os
from time import perf_counter


@Client.on_message(fox_command(command1="ping", Module_Name="Ping", names=os.path.basename(__file__)) & filters.me)
async def ping(client, message):
    start = perf_counter()
    await message.edit("🏓| ⚾=== |🏓")
    await message.edit("🏓| =⚾== |🏓")
    await message.edit("🏓| ==⚾= |🏓")
    await message.edit("🏓| ===⚾ |🏓")
    end = perf_counter()

    pinges = ((end - start) / 4)
    ping = pinges * 1000

    if 0 <= ping <= 199:
        connect = "🟢 Stable"
    if 199 <= ping <= 400:
        connect = "🟠 Good"
    if 400 <= ping <= 600:
        connect = "🔴 Unstable"
    if 600 <= ping:
        connect = "⚠ Check you network connection"
    await message.edit(f"<b>🏓 Pong\n📶</b> {round(ping)} ms\n{connect}")
