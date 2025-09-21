import os
import shutil
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path

from pyrogram import Client

from command import fox_command, fox_sudo, who_message
from modules.plugins_1system.restarter import restart
from modules.plugins_1system.settings.main_settings import version

# backup_dirs
BACKUP_PATHS = [
    'userdata',
    'triggers', 
    'modules/plugins_2custom'
]

async def create_backup() -> str:
    def exclude_sudo_users(tarinfo):
        if tarinfo.name == "userdata/sudo_users.json":
            return None
        return tarinfo

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with tempfile.NamedTemporaryFile(suffix=f'_FoxUB_Backup_{timestamp}.tar.gz', delete=False) as tmp:
        with tarfile.open(tmp.name, mode='w:gz') as tar:
            for path in BACKUP_PATHS:
                if os.path.exists(path):
                    tar.add(path, filter=exclude_sudo_users)
        return tmp.name


async def restore_backup(client, message):
    if not message.reply_to_message or not message.reply_to_message.document:
        await message.edit("<b><emoji id='5210952531676504517'>❌</emoji> Need to reply to a message with a backup archive!</b>")
        return False

    try:
        download_path = await message.reply_to_message.download()
        
        try:
            with tarfile.open(download_path, 'r:gz') as test_tar:
                test_tar.getmembers()
        except:
            await message.edit("<b><emoji id='5210952531676504517'>❌</emoji> Invalid backup archive!</b>")
            return False
        
        for path in BACKUP_PATHS:
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)

        with tarfile.open(download_path, 'r:gz') as tar:
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
    backup_file = None
    try:
        msg = await message.edit("<b><emoji id='5264727218734524899'>🔄</emoji> Creating a backup copy...</b>")
        backup_file = await create_backup()
        
        if os.path.getsize(backup_file) == 0:
            raise Exception("Backup file is empty")
        
        await client.send_document(
            chat_id=message.chat.id,
            document=backup_file,
            caption=f"<emoji id='5472308992514464048'>🔐</emoji> | Backup {Path(backup_file).name}\n<emoji id='5283051451889756068'>🦊</emoji> | Only for FoxUserbot\n<emoji id='5296369303661067030'>🔒</emoji> | Version: {version}\n<emoji id='5271604874419647061'>🔗</emoji> | https://github.com/FoxUserbot/FoxUserbot",
            message_thread_id=message.message_thread_id
        )
        await msg.delete()
        
    except Exception as e:
        error_msg = f"<b><emoji id='5210952531676504517'>❌</emoji> Error creating backup:</b>\n<code>{str(e)}</code>"
        await message.edit(error_msg)
        
    finally:
        if backup_file and os.path.exists(backup_file):
            os.remove(backup_file)


@Client.on_message(fox_command("restore", "Backup", os.path.basename(__file__), "[reply]") & fox_sudo())
async def restore_command(client, message):
    message = await who_message(client, message)
    try:
        await message.edit("<b><emoji id='5264727218734524899'>🔄</emoji> Ready for restoration...</b>")
        success = await restore_backup(client, message)
        if success:
            await restart(message, restart_type="restart")
    except Exception as e:
        await message.edit(f"<b><emoji id='5210952531676504517'>❌</emoji> Error:</b>\n<code>{str(e)}</code>")


@Client.on_message(fox_command("backup_modules", "Backup", os.path.basename(__file__)) & fox_sudo())
async def backup_modules_command(client, message):
    message = await who_message(client, message)
    backup_file = None
    try:
        msg = await message.edit("<b><emoji id='5264727218734524899'>🔄</emoji> Creating modules backup...</b>")
        
        with tempfile.NamedTemporaryFile(suffix='_FoxUB_Modules_Backup.tar.gz', delete=False) as tmp:
            with tarfile.open(tmp.name, mode='w:gz') as tar:
                if os.path.exists('modules/plugins_2custom'):
                    tar.add('modules/plugins_2custom')
            backup_file = tmp.name
        
        if os.path.getsize(backup_file) == 0:
            raise Exception("Backup file is empty")
        
        await client.send_document(
            chat_id=message.chat.id,
            document=backup_file,
            caption=f"<emoji id='5472308992514464048'>🔐</emoji> | Modules Backup {Path(backup_file).name}\n<emoji id='5283051451889756068'>🦊</emoji> | Only for FoxUserbot\n<emoji id='5296369303661067030'>🔒</emoji> | Version: {version}\n<emoji id='5271604874419647061'>🔗</emoji> | https://github.com/FoxUserbot/FoxUserbot",
            message_thread_id=message.message_thread_id
        )
        await msg.delete()
        
    except Exception as e:
        error_msg = f"<b><emoji id='5210952531676504517'>❌</emoji> Error creating modules backup:</b>\n<code>{str(e)}</code>"
        await message.edit(error_msg)
        
    finally:
        if backup_file and os.path.exists(backup_file):
            os.remove(backup_file)
