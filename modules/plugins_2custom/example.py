from pyrogram import Client, filters
from command import fox_command
import os


@Client.on_message(fox_command("example_edit", Module_Name='Example', names=os.path.basename(__file__), arg="[Example Arg]") & filters.me)
async def example_edit(client, message):
    await message.edit("<code>This is an example module</code>")
