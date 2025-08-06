from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import version
from modules.plugins_1system.restarter import restart
from command import fox_command
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
    args = message.text.split(maxsplit=2)
    
    if len(args) < 2:
        from prefix import my_prefix
        return await message.edit(f"<b>Использование:</b>\n<code>{my_prefix()}sudo add @username</code>\n<code>{my_prefix()}sudo del @username</code>\n<code>{my_prefix()}sudo list</code>")

    action = args[1].lower()
    sudo_users = load_sudo_users()

    if action == "list":
        users_list = "\n".join([f"• <code>{user}</code>" for user in sudo_users]) or "Нет sudo-пользователей"
        return await message.edit(f"<b>Sudo-пользователи:</b>\n{users_list}")

    if len(args) < 3:
        return await message.edit("<b>Укажите пользователя!</b>")

    user_input = args[2].strip()
    user_id = None

    if user_input.startswith("@"):
        try:
            user = await client.get_users(user_input)
            user_id = int(user.id)
        except Exception:
            return await message.edit("<b>Пользователь не найден!</b>")
    else:
        user_id = user_input  

    if action == "add":
        if user_id in sudo_users:
            await message.edit(f"<b>Пользователь <code>{user_input}</code> уже в списке!</b>")
        else:
            sudo_users.append(user_id)
            save_sudo_users(sudo_users)
            await message.edit(f"<b>✅ Пользователь <code>{user_input}</code> добавлен в sudo!</b>\nребутаюсь")
            await restart(message, restart_type="restart")

    elif action == "del":
        if user_id in sudo_users:
            sudo_users.remove(user_id)
            save_sudo_users(sudo_users)
            await message.edit(f"<b>❌ Пользователь <code>{user_input}</code> удален из sudo!</b>")
            await restart(message, restart_type="restart")
        else:
            await message.edit(f"<b>Пользователь <code>{user_input}</code> не найден в списке!</b>")

    else:
        await message.edit("<b>Неизвестное действие! Используйте add/del/list</b>")
