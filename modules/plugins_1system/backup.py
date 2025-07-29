from pyrogram import Client, filters
from pyrogram.types import Message
import os
import shutil
import tarfile
import tempfile
from pathlib import Path
from modules.plugins_1system.settings.main_settings import version
from modules.plugins_1system.restarter import restart
from command import fox_command

# backup_dirs
BACKUP_PATHS = [
    'userdata',
    'triggers', 
    'modules/plugins_2custom'
]

async def create_backup() -> str:
    with tempfile.NamedTemporaryFile(suffix='_FoxUB_Backup.tar.gz', delete=False) as tmp:
        with tarfile.open(tmp.name, mode='w:gz') as tar:
            for path in BACKUP_PATHS:
                if os.path.exists(path):
                    tar.add(path)
        return tmp.name

async def restore_backup(client, message):
    if not message.reply_to_message or not message.reply_to_message.document:
        await message.edit("<b>❌ Need to reply to a message with a backup archive!</b>")
        return

    try:
        download_path = await message.reply_to_message.download()
        
        for path in BACKUP_PATHS:
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)

        with tarfile.open(download_path, 'r:gz') as tar:
            tar.extractall()
        
        await message.edit("<b>✅ Data restored successfully!</b>")
    except Exception as e:
        await message.edit(f"<b>❌ Restore Error:</b>\n<code>{str(e)}</code>")
    finally:
        if 'download_path' in locals() and os.path.exists(download_path):
            os.remove(download_path)

@Client.on_message(fox_command(command1="backup", Module_Name="Backup", names=os.path.basename(__file__)) & filters.me)
async def backup_command(client, message):
    try:
        msg = await message.edit("<b>🔄 Creating a backup copy...</b>")
        backup_file = await create_backup()
        
        await client.send_document(
            chat_id=message.chat.id,
            document=backup_file,
            caption=f"🔐 | Backup {Path(backup_file).name}\n🦊 | Only for FoxUserbot\n🔒 | Version: {version}\n🔗 | https://t.me/FoxUserbot",
            message_thread_id=message.message_thread_id
        )
        await msg.delete()
    except Exception as e:
        await message.edit(f"<b>❌ Error creating backup:</b>\n<code>{str(e)}</code>")
    finally:
        if 'backup_file' in locals() and os.path.exists(backup_file):
            os.remove(backup_file)

@Client.on_message(fox_command(command1="restore", Module_Name="Backup", names=os.path.basename(__file__) , arg="[reply]") & filters.me)
async def restore_command(client, message):
    await message.edit("<b>🔄 Ready for restoration...</b>")
    await restore_backup(client, message)
    await restart(message, restart_type="restart")

