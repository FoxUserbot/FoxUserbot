import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.settings.main_settings import module_list, file_list, settings

prefix = settings['prefix']


@Client.on_message(filters.command("statspam", prefixes=prefix) & filters.me)
async def statspam(client: Client, message: Message):
    quantity = message.command[1]
    spam_text = " ".join(message.command[2:])
    quantity = int(quantity)
    await message.delete()
    for _ in range(quantity):
        msg = await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.1)
        await msg.delete()
        await asyncio.sleep(0.1)


@Client.on_message(filters.command("spam", prefixes=prefix) & filters.me)
async def spam(client: Client, message: Message):
    quantity = message.command[1]
    spam_text = " ".join(message.command[2:])
    quantity = int(quantity)
    await message.delete()

    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
        for _ in range(quantity):
            await client.send_message(
                message.chat.id, spam_text, reply_to_message_id=reply_to_id
            )
            await asyncio.sleep(0.15)
        return

    for _ in range(quantity):
        await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.15)


@Client.on_message(filters.command("fastspam", prefixes=prefix) & filters.me)
async def fastspam(client: Client, message: Message):
    quantity = message.command[1]
    spam_text = " ".join(message.command[2:])
    quantity = int(quantity)
    await message.delete()

    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
        for _ in range(quantity):
            await client.send_message(
                message.chat.id, spam_text, reply_to_message_id=reply_to_id
            )
            await asyncio.sleep(0.02)
        return

    for _ in range(quantity):
        await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.02)


@Client.on_message(filters.command("slowspam", prefixes=prefix) & filters.me)
async def slowspam(client: Client, message: Message):
    quantity = message.command[1]
    spam_text = " ".join(message.command[2:])
    quantity = int(quantity)
    await message.delete()

    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
        for _ in range(quantity):
            await client.send_message(
                message.chat.id, spam_text, reply_to_message_id=reply_to_id
            )
            await asyncio.sleep(0.9)
        return

    for _ in range(quantity):
        msg = await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.9)

@Client.on_message(filters.command("help_spam", prefixes=prefix) & filters.me)
async def help_spam(client: Client, message: Message):
    await message.edit(f"""```{prefix}spam [amount of spam] [spam text]``` - **Start spam.**
```{prefix}statspam [amount of spam] [spam text]``` - **Send and delete.**
```{prefix}fastspam [amount of spam] [spam text]``` - **Start fast spam.**
```{prefix}slowspam [amount of spam] [spam text]``` - **Start slow spam**""")
    
module_list['Spam'] = f'Many commands. View them: {prefix}help_spam'
file_list['Spam'] = 'spam.py'
