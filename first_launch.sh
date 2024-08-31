#!/bin/bash
rm -rf my_account.session
rm -rf config.ini
echo "Enter Your api id"
read api_id
echo "Enter Your api hash"
read api_hash
echo "Pasting.. in config API ID : $api_id , API HASH : $api_hash"
sed -i "s/config_id = \".*\"/config_id = \"$api_id\"/" configurator.py
sed -i "s/config_hash = \".*\"/config_hash = \"$api_hash\"/" configurator.py
echo "Starting Userbot..."
python3 main.py