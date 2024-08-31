from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

import asyncio
import json
import os
import requests
from lyricsgenius import Genius


api_token = '9JiBRxKAEgfssIWg3Yw8uxKyDO0HZr1IQS5qVYQiKMLwJ4d_9tEMxxYlm3w_mIML' # genius api key
l = Genius(api_token)


@Client.on_message(filters.command(["l", "lyrics"], prefixes=my_prefix()) & filters.me)
async def send_music(client, message):
    if len(message.text.split()) >= 2:
        await client.edit_message_text(message.chat.id, message.id, 'Searching text...')
        url = {"Authorization": f"Bearer {api_token}"}
        song_name = ' '.join(message.text.split()[1:])
        text = song_name.lower().replace(' ', '%20')
        q = requests.get(f'https://api.genius.com/search?q={text}', headers=url).text
        data_dict = json.loads(q)
        try:
            url_song = data_dict['response']['hits'][0]['result']['url']
            lyrics = l.lyrics(song_url=url_song).replace('Embed','')
            with open('song_text.txt','w+',encoding='utf-8') as file:
                file.write(lyrics)
            await client.send_document(message.chat.id, 'song_text.txt', caption='Keep the lyrics this song!')
            os.remove('song_text.txt')
        except Exception as e:
            await client.edit_message_text(message.chat.id, message.id, "I can't find text!")
    else:
        await client.edit_message_text(message.chat.id, message.id, 'Give me a name song!')


@Client.on_message(filters.command(["dm", "dmusic"], prefixes=my_prefix()) & filters.me)
async def d_send_music(client, message):
    bots = "DeezerMusicBot"

    await message.edit("Search...")
    song_name = ""
    if len(message.command) > 1:
        song_name = " ".join(message.command[1:])
    elif message.reply_to_message and len(message.command) == 1:
        song_name = (
                message.reply_to_message.text or message.reply_to_message.caption
        )
    elif not message.reply_to_message and len(message.command) == 1:
        await message.edit("Enter the name of the music")
        await asyncio.sleep(2)
        await message.delete()
        return

    song_results = await client.get_inline_bot_results(bots, song_name)

    try:
        # send to Saved Messages because hide_via doesn't work sometimes
        saved = await client.send_inline_bot_result(
            chat_id="me",
            query_id=song_results.query_id,
            result_id=song_results.results[0].id,
        )

        # forward as a new message from Saved Messages
        saved = await client.get_messages("me", int(saved.updates[1].message.id))
        reply_to = (
            message.reply_to_message.id
            if message.reply_to_message
            else None
        )
        await client.send_audio(
            chat_id=message.chat.id,
            audio=str(saved.audio.file_id),
            reply_to_message_id=reply_to,
        )

        # delete the message from Saved Messages
        await client.delete_messages("me", saved.id)
    except TimeoutError:
        await message.edit("That didn't work out")
    except: 
        await message.edit("I can't find music!")
    await asyncio.sleep(2)
    await message.delete()


@Client.on_message(filters.command(["lm", "lmusic"], prefixes=my_prefix()) & filters.me)
async def l_send_music(client, message):
    bots = "LosslessRobot"
    await message.edit("Search...")
    song_name = ""
    if len(message.command) > 1:
        song_name = " ".join(message.command[1:])
    elif message.reply_to_message and len(message.command) == 1:
        song_name = (
                message.reply_to_message.text or message.reply_to_message.caption
        )
    elif not message.reply_to_message and len(message.command) == 1:
        await message.edit("Enter the name of the music")
        await asyncio.sleep(2)
        await message.delete()
        return

    song_results = await client.get_inline_bot_results(bots, song_name)

    try:
        # send to Saved Messages because hide_via doesn't work sometimes
        saved = await client.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=song_results.query_id,
            result_id=song_results.results[0].id,
        )
    except TimeoutError:
        await message.edit("That didn't work out")
    except:
        await message.edit("I can't find music!")
    await asyncio.sleep(2)
    await message.delete()



module_list['FindMusic'] = f'{my_prefix()}lyrics [Title on music] | [{my_prefix()}dmusic] or [{my_prefix()}lmusic] [Title on music]'
file_list['FindMusic'] = 'find_music.py'
