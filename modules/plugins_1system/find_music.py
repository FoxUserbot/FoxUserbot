from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

import json
import os
import requests
from bs4 import BeautifulSoup

api_token = '9JiBRxKAEgfssIWg3Yw8uxKyDO0HZr1IQS5qVYQiKMLwJ4d_9tEMxxYlm3w_mIML' # genius api key

def clear_html(url_1,text):
    text = text.replace('<br/>','\n').replace('<div class="Lyrics__Container-sc-1ynbvzw-1 kUgSbL" data-lyrics-container="true">','').replace('</div>','')
    listur_delete = ['<span class="ReferentFragmentdesktop__Highlight-sc-110r0d9-1 jAzSMw>',
    '<span class="ReferentFragmentdesktop__Highlight-sc-110r0d9-1 jAzSMw>','</a>','<a>','</span>','<span>', '</i>','<i>',
    '<span style="position:absolute;opacity:0;width:0;height:0;pointer-events:none;z-index:-1" tabindex="0">','<span class="ReferentFragmentdesktop__Highlight-sc-110r0d9-1 jAzSMw">',
    '<a class="ReferentFragmentdesktop__ClickTarget-sc-110r0d9-0 cesxpW"', 'href=',f'/{url_1}/">','&amp;','<b>','</b>',"'","/",'>',"<",'"'] + [str(i) for i in range(0,10)]
    for i in listur_delete:
        text = text.replace(i,'')
    return text


@Client.on_message(filters.command(["l", "lyrics"], prefixes=my_prefix()) & filters.me)
async def send_music(client, message):
    if len(message.text.split()) >= 2:
        await client.edit_message_text(message.chat.id, message.id, 'Searching text...')
        url = {"Authorization": f"Bearer {api_token}"}
        song_name = ' '.join(message.text.split()[1:])
        text = song_name.lower().replace(' ', '%20')
        q = requests.get(f'https://api.genius.com/search?q={text}', headers=url).text
        data_dict = json.loads(q)
        try:
            url_song = data_dict['response']['hits'][0]['result']['url']
            url_1 = url_song.split('/')[-1].replace('-lyrics', '')
            link_res = requests.get(url_song)
            words = []
            bs = BeautifulSoup(link_res.text, 'html.parser')
            all_lyrics = bs.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-1 kUgSbL')
            with open('song_text.txt', 'w+', encoding='utf-8') as file:
                for i in all_lyrics:
                    text = i.prettify()
                    links = i.find_all('a', href=True)
                    for link in links:
                        url = link['href'][1:]
                        link_to_remove = ''.join(url.split('/')[1:])
                        words.append(link_to_remove)
                    file.write(clear_html(url_1, text))
            with open('song_text.txt', 'r', encoding='utf-8') as file:
                lyrics = file.read()
            for i in words:
                lyrics = lyrics.replace(i,'')
            with open('song_text.txt', 'w', encoding='utf-8') as file:
                file.write(lyrics)
            await client.send_document(message.chat.id, 'song_text.txt', caption='Keep the lyrics this song!')
            os.remove('song_text.txt')
        except Exception as e:
            await client.edit_message_text(message.chat.id, message.id, "I can't find text!")

    else:
        await client.edit_message_text(message.chat.id, message.id, 'Give me a name song!')

module_list['FindMusic'] = f'{my_prefix()}lyrics [Title on music]'
file_list['FindMusic'] = 'find_music.py'
