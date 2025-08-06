from pyrogram import Client , filters
from modules.plugins_1system.restarter import restart
from command import fox_command, fox_sudo, who_message
import os
import json
from pathlib import Path

SUDO_USERS_FILE = Path("userdata/sudo_users.json")

def load_sudo_users():
    with open(SUDO_USERS_FILE, "r") as f:
        return json.load(f)

def save_sudo_users(users):
    with open(SUDO_USERS_FILE, "w") as f:
        json.dump(users, f)

@Client.on_message(fox_command("sudo", "SudoManager", os.path.basename(__file__), "[add/del/list] [@username/id]") & filters.me)
async def sudo_manager(client, message):
    message = await who_message(client, message)
    args = message.text.split(maxsplit=2)
    
    if len(args) < 2:
        from prefix import my_prefix
        return await message.edit(f"<emoji id='5283051451889756068'>🦊</emoji> <b>Usage:</b>\n<code>{my_prefix()}sudo add @username</code>\n<code>{my_prefix()}sudo del @username</code>\n<code>{my_prefix()}sudo list</code>")

    action = args[1].lower()
    sudo_users = load_sudo_users()

    if action == "list":
        users_list = "\n".join([f"• <code>{user}</code>" for user in sudo_users]) or "No sudo users"
        return await message.edit(f"<emoji id='5283051451889756068'>🦊</emoji> <b>Sudo users:</b>\n<blockquote expandable>{users_list}</blockquote>")

    if len(args) < 3:
        return await message.edit(f"<emoji id='5210952531676504517'>❌</emoji> <b>Please specify a user!</b>")

    user_input = args[2].strip()
    user_id = None

    if user_input.startswith("@"):
        try:
            user = await client.get_users(user_input)
            user_id = int(user.id)
        except Exception:
            return await message.edit(f"<emoji id='5210952531676504517'>❌</emoji> <b>User not found!</b>")
    else:
        user_id = user_input  

    if action == "add":
        if int(user_id) in sudo_users:
            await message.edit(f"<emoji id='5210952531676504517'>❌</emoji> <b>User <code>{user_input}</code> is already in the list!</b>")
        else:
            sudo_users.append(int(user_id))
            save_sudo_users(sudo_users)
            await message.edit(f"<emoji id='5237699328843200968'>✅</emoji>  <b>User <code>{user_input}</code> added to sudo!</b>\n<emoji id='5264727218734524899'>🔄</emoji> Rebooting...")
            await restart(message, restart_type="restart")

    elif action == "del":
        if int(user_id) in sudo_users:
            sudo_users.remove(int(user_id))
            save_sudo_users(sudo_users)
            await message.edit(f"<emoji id='5237699328843200968'>✅</emoji>  <b>User <code>{user_input}</code> removed from sudo!</b>\n<emoji id='5264727218734524899'>🔄</emoji> Rebooting...")
            await restart(message, restart_type="restart")
        else:
            await message.edit(f"<emoji id='5210952531676504517'>❌</emoji> <b>User <code>{user_input}</code> not found in the list!</b>")

    else:
        await message.edit(f"<emoji id='5210952531676504517'>❌</emoji> <b>Unknown action! Use add/del/list</b>")

