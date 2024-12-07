@echo off
chcp 65001
cls
echo Install Python 3.12..
winget install --id 9NCVDN91XZQP
set /p api_id=Enter api id:
set /p api_hash=Enter api hash:
python help_first_launch.py %api_id% %api_hash%
pip install pyrogram
python main.py
