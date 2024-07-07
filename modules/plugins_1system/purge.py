from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix


@Client.on_message(filters.command("del", prefixes=my_prefix()) & filters.me)
async def delete_messages(client, message):
    if message.reply_to_message:
        message_id = message.reply_to_message.id
        await client.delete_messages(message.chat.id, message_id)
    await message.delete()


@Client.on_message(filters.command("purge", prefixes=my_prefix()) & filters.me)
async def purge(client, message):
    try:
        try:
            g = message.command[1]
            try:
                g = int(g)
            except:
                g = str(g)
            r = int(message.command[2])
            m = int(message.command[3])
        except:
            if message.reply_to_message:
                r = message.reply_to_message.id
                m = message.id
                g = message.chat.id
            else:
                await message.edit("<i>I don't see reply</i>")

        await message.delete()
        while r != m:
            try:
                await client.delete_messages(g, int(r))
            except:
                pass
            r += 1

        await client.send_message(message.chat.id, f"<b>Messages deleted!</b>")
    except Exception as f:
        await message.edit(f"<i>Don't have permision.</i>{f}")

module_list['Purge'] = f'{my_prefix()}del [reply] | {my_prefix()}purge [reply] / [Group id] [Start ID] [Stop ID]'
file_list['Purge'] = 'purge.py'
