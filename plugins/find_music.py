from pyrogram import Client, filters
from plugins.settings.main_settings import module_list, file_list
import asyncio

from prefix import my_prefix
prefix = my_prefix()


bots = "DeezerMusicBot"


@Client.on_message(filters.command(["m", "music"], prefixes=prefix) & filters.me)
async def send_music(client, message):
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
            hide_via=True,
        )

        # forward as a new message from Saved Messages
        saved = await client.get_messages("me", int(saved.updates[1].message.id))
        reply_to = (
            message.reply_to_message.message_id
            if message.reply_to_message
            else None
        )
        await client.send_audio(
            chat_id=message.chat.id,
            audio=str(saved.audio.file_id),
            reply_to_message_id=reply_to,
        )

        # delete the message from Saved Messages
        await client.delete_messages("me", saved.message_id)
    except TimeoutError:
        await message.edit("That didn't work out")
        await asyncio.sleep(2)
    await message.delete()


# from athphane userbot
@Client.on_message(filters.command(["l", "lyrics"], prefixes=prefix) & filters.me)
async def send_music(client, message):
    try:
        cmd = message.command
        song_name = ""
        if len(cmd) > 1:
            song_name = " ".join(cmd[1:])
        elif message.reply_to_message:
            if message.reply_to_message.audio:
                song_name = f"{message.reply_to_message.audio.title} {message.reply_to_message.audio.performer}"
            elif len(cmd) == 1:
                song_name = message.reply_to_message.text
        elif not message.reply_to_message and len(cmd) == 1:
            await message.edit("Give a song name")
            await asyncio.sleep(2)
            await message.delete()
            return

        await message.edit(f"Getting lyrics for `{song_name}`")
        lyrics_results = await client.get_inline_bot_results("ilyricsbot", song_name)

        try:
            # send to Saved Messages because hide_via doesn't work sometimes
            saved = await client.send_inline_bot_result(
                chat_id="me",
                query_id=lyrics_results.query_id,
                result_id=lyrics_results.results[0].id,
                hide_via=True,
            )
            await asyncio.sleep(3)

            # forward from Saved Messages
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id="me",
                message_id=saved.updates[1].message.id,
            )

            # delete the message from Saved Messages
            await client.delete_messages("me", saved.updates[1].message.id)
        except TimeoutError:
            await message.edit("That didn't work out")
            await asyncio.sleep(2)
        await message.delete()
    except Exception as e:
        print(e)
        await message.edit("`Failed to find lyrics`")
        await asyncio.sleep(2)
        await message.delete()


module_list['FindMusic'] = f'{prefix}music [Title of music] | {prefix}lyrics [Title on music]'
file_list['FindMusic'] = 'find_music.py'
