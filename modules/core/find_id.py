# -*- coding: utf-8 -*-
import os

from pyrogram import Client

from command import fox_command, fox_sudo, who_message, get_text

LANGUAGES = {
    "en": {
        "chat_id": "<emoji id='5974526806995242353'>🆔</emoji> Chat ID: `{chat_id}`",
        "user_and_chat": "<emoji id='5974526806995242353'>🆔</emoji> User ID: `{user_id}`\n<emoji id='5974526806995242353'>🆔</emoji> Chat ID: `{chat_id}`"
    },
    "ru": {
        "chat_id": "<emoji id='5974526806995242353'>🆔</emoji> ID чата: `{chat_id}`",
        "user_and_chat": "<emoji id='5974526806995242353'>🆔</emoji> ID пользователя: `{user_id}`\n<emoji id='5974526806995242353'>🆔</emoji> ID чата: `{chat_id}`"
    },
    "ua": {
        "chat_id": "<emoji id='5974526806995242353'>🆔</emoji> ID чату: `{chat_id}`",
        "user_and_chat": "<emoji id='5974526806995242353'>🆔</emoji> ID користувача: `{user_id}`\n<emoji id='5974526806995242353'>🆔</emoji> ID чату: `{chat_id}`"
    }
}

@Client.on_message(fox_command("id", "FindIDThisChat", os.path.basename(__file__)) & fox_sudo())
async def find_id(client, message):
    message = await who_message(client, message)
    if message.reply_to_message is None:
        text = get_text("find_id", "chat_id", LANGUAGES=LANGUAGES, chat_id=message.chat.id)
        await message.edit(text)
    else:
        text = get_text("find_id", "user_and_chat", LANGUAGES=LANGUAGES, 
                       user_id=message.reply_to_message.from_user.id, 
                       chat_id=message.chat.id)
        await message.edit(text)