from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix


@Client.on_message(filters.command("qr", prefixes=my_prefix()) & filters.me)
async def qr(client, message):
    texts = ""
    if message.reply_to_message:
        texts = message.reply_to_message.text
    elif len(message.text.split(maxsplit=1)) == 2:
        texts = message.text.split(maxsplit=1)[1]
    text = texts.replace(' ', '%20')
    QRcode = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={text}"
    await message.delete()
    await client.send_photo(message.chat.id, QRcode)


module_list['QRcode'] = f'{my_prefix()}qr [text]'
file_list['QRcode'] = 'qr.py'
