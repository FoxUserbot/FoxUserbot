from pyrogram import Client
import os
import shutil
import tarfile
import tempfile
from pathlib import Path
from modules.plugins_1system.settings.main_settings import version
from modules.plugins_1system.restarter import restart
from command import fox_command, fox_sudo, who_message
from datetime import datetime

# backup_dirs
BACKUP_PATHS = [
    'userdata',
    'triggers', 
    'modules/plugins_2custom'
]

async def create_backup(backup_paths: list) -> str:
    def exclude_sudo_users(tarinfo):
        if tarinfo.name == "userdata/sudo_users.json":
            return None
        return tarinfo

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with tempfile.NamedTemporaryFile(suffix=f'_FoxUB_Backup_{timestamp}.tar.gz', delete=False) as tmp:
        with tarfile.open(tmp.name, mode='w:gz') as tar:
            for path in backup_paths:
                if os.path.exists(path):
                    tar.add(path, filter=exclude_sudo_users)
        return tmp.name


async def restore_backup(client, message):
    if not message.reply_to_message or not message.reply_to_message.document:
        await message.edit("<b><emoji id='5210952531676504517'>❌</emoji> Need to reply to a message with a backup archive!</b>")
        return

    try:
        download_path = await message.reply_to_message.download()
        
        with tarfile.open(download_path, 'r:gz') as tar:
            archive_members = tar.getnames()
            
            paths_to_clear = []
            for path in BACKUP_PATHS:
                has_files_from_path = any(member.startswith(path + '/') or member == path for member in archive_members)
                if has_files_from_path and os.path.exists(path):
                    paths_to_clear.append(path)

            for path in paths_to_clear:
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)

            tar.extractall()
        
        await message.edit("<b><emoji id='5237699328843200968'>✅</emoji> Data restored successfully!</b>")
        return True
        
    except Exception as e:
        await message.edit(f"<b><emoji id='5210952531676504517'>❌</emoji> Restore Error:</b>\n<code>{str(e)}</code>")
        return False
    finally:
        if 'download_path' in locals() and os.path.exists(download_path):
            os.remove(download_path)


@Client.on_message(fox_command("backup", "Backup", os.path.basename(__file__)) & fox_sudo())
async def backup_command(client, message):
    message = await who_message(client, message)
    try:
        msg = await message.edit("<b><emoji id='5264727218734524899'>🔄</emoji> Creating full backup...</b>")
        backup_file = await create_backup(BACKUP_PATHS)
        
        await client.send_document(
            chat_id=message.chat.id,
            document=backup_file,
            caption=f"<emoji id='5472308992514464048'>🔐</emoji> | Full Backup {Path(backup_file).name}\n"
                    f"<emoji id='5283051451889756068'>🦊</emoji> | Only for FoxUserbot\n"
                    f"<emoji id='5296369303661067030'>🔒</emoji> | Version: {version}\n"
                    f"<emoji id='5271604874419647061'>🔗</emoji> | https://github.com/FoxUserbot/FoxUserbot\n"
                    f"<emoji id='5332535072368296296'>📦</emoji> | Includes: userdata, triggers, custom modules",
            message_thread_id=message.message_thread_id
        )
        await msg.delete()
    except Exception as e:
        await message.edit(f"<b><emoji id='5210952531676504517'>❌</emoji> Error creating backup:</b>\n<code>{str(e)}</code>")
    finally:
        if 'backup_file' in locals() and os.path.exists(backup_file):
            os.remove(backup_file)


@Client.on_message(fox_command("backup_modules", "Backup", os.path.basename(__file__)) & fox_sudo())
async def backup_modules_command(client, message):
    message = await who_message(client, message)
    try:
        msg = await message.edit("<b><emoji id='5264727218734524899'>🔄</emoji> Creating modules backup...</b>")
        modules_backup_paths = ['modules/plugins_2custom']
        backup_file = await create_backup(modules_backup_paths)
        
        await client.send_document(
            chat_id=message.chat.id,
            document=backup_file,
            caption=f"<emoji id='5472308992514464048'>🔐</emoji> | Modules Backup {Path(backup_file).name}\n"
                    f"<emoji id='5283051451889756068'>🦊</emoji> | Only for FoxUserbot\n"
                    f"<emoji id='5296369303661067030'>🔒</emoji> | Version: {version}\n"
                    f"<emoji id='5271604874419647061'>🔗</emoji> | https://github.com/FoxUserbot/FoxUserbot\n"
                    f"<emoji id='5332535072368296296'>📦</emoji> | Includes: custom modules only",
            message_thread_id=message.message_thread_id
        )
        await msg.delete()
    except Exception as e:
        await message.edit(f"<b><emoji id='5210952531676504517'>❌</emoji> Error creating modules backup:</b>\n<code>{str(e)}</code>")
    finally:
        if 'backup_file' in locals() and os.path.exists(backup_file):
            os.remove(backup_file)


@Client.on_message(fox_command("restore", "Backup", os.path.basename(__file__), "[reply]") & fox_sudo())
async def restore_command(client, message):
    message = await who_message(client, message)
    try:
        await message.edit("<b><emoji id='5264727218734524899'>🔄</emoji> Restoring data from backup...</b>")
        
        success = await restore_backup(client, message)
        if success:
            await message.edit("<b><emoji id='5237699328843200968'>✅</emoji> Data restored successfully! Restarting...</b>")
            await restart(message, restart_type="restart")
        else:
            await message.edit("<b><emoji id='5210952531676504517'>❌</emoji> Restore failed!</b>")
            
    except Exception as e:
        await message.edit(f"<b><emoji id='5210952531676504517'>❌</emoji> Restore Error:</b>\n<code>{str(e)}</code>")