from pyrogram import Client, filters
from plugins.settings.main_settings import module_list, file_list

from prefix import my_prefix
prefix = my_prefix()


@Client.on_message(filters.command('kickall', prefixes=prefix) & filters.me)
async def kickall(client, message):
    await message.edit("kick all chat members!")
    member = client.iter_chat_members(message.chat.id)
    async for alls in member:
        try:
            await client.ban_chat_member(message.chat.id, alls.user.id, 0)
        except:
            pass


@Client.on_message(filters.command('kickall_hide', prefixes=prefix) & filters.me)
async def kickall_hide(client, message):
    await message.delete()
    member = client.iter_chat_members(message.chat.id)
    async for alls in member:
        try:
            await client.ban_chat_member(message.chat.id, alls.user.id, 0)
        except:
            pass


module_list['KickallSubs'] = f'{prefix}kickall'
file_list['KickallSubs'] = 'kickall.py'
