from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

from pathlib import Path


@Client.on_message(filters.text & filters.incoming & filters.regex("^\-$") & filters.reply)
async def repDown(client, message):
    try:
        if message.reply_to_message.from_user.is_self:
            if Path(f"temp/reputation").is_file():
                with open("temp/reputation", "r+") as f:
                    NowReputation = int(f.read())
                    f.close()
            else:
                NowReputation = 0
            with open("temp/reputation", "w+") as f:
                reputation = str(NowReputation - 1)
                f.write(reputation)
                f.close()
            await message.reply_text(f"❎ Reputation lowered (-1)\n🌐 Your reputation: {str(reputation)}")
    except:
        pass


@Client.on_message(filters.text & filters.incoming & filters.regex("^\+$") & filters.reply)
async def repUp(client, message):
    try:
        if message.reply_to_message.from_user.is_self:
            if Path(f"temp/reputation").is_file():
                with open("temp/reputation", "r+") as f:
                    NowReputation = int(f.read())
                    f.close()
            else:
                NowReputation = 0
            with open("temp/reputation", "w+") as f:
                reputation = str(NowReputation + 1)
                f.write(reputation)
                f.close()
            await message.reply_text(f"✅ Reputation increased (+1)\n🌐 Your reputation: {str(reputation)}")
    except:
        pass


@Client.on_message(filters.command("rep", prefixes=my_prefix()) & filters.me)
async def repNakrutka(client, message):
    try:
        with open("temp/reputation", "w+") as f:
            rep = str(int(message.command[1]))
            f.write(rep)
            f.close()
            text = f"Reputation edited.\nReputation: {str(rep)}"
            await message.edit(text)

    except Exception as error:
        await message.edit(
            f"Error! Reputation edited to '0'\n\nLog: {error}")
        with open("temp/reputation", "w+") as f:
            f.write(str(int(0)))
            f.close()


module_list['Reputation'] = f'reply "+" or "-" from another user | {my_prefix()}rep [number]'
file_list['Reputation'] = 'reputation.py'
