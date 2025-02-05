
#!/bin/bash
rm -rf my_account.session
rm -rf config.ini
api_id=${API_ID}
api_hash=${API_HASH}
echo "Pasting.. in config API ID : $api_id , API HASH : $api_hash"
sed -i "s/config_id = \".*\"/config_id = \"$api_id\"/" configurator.py
sed -i "s/config_hash = \".*\"/config_hash = \"$api_hash\"/" configurator.py
echo "Pasted in config API ID : $api_id , API HASH : $api_hash"