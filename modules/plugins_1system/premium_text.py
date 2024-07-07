# https://github.com/ArThirtyFour

from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix


emoji_list = {
    'а': '<emoji id=5442667851246742007>🔤</emoji>',
    'б': '<emoji id=5442708515997100433>🔤</emoji>',
    'в': '<emoji id=5449413294953606262>🔤</emoji>',
    'г': '<emoji id=5452141660043488430>🔤</emoji>',
    'д': '<emoji id=5451814740017817067>🔤</emoji>',
    'е': '<emoji id=5195169080914486911>🔤</emoji>',
    'ё': '<emoji id=5197457624173389781>🔤</emoji>',
    'ж': '<emoji id=5452108017564657802>🔤</emoji>',
    'з': '<emoji id=5472327074326786286>🔤</emoji>',
    'и': '<emoji id=5449768699202381205>🔤</emoji>',
    'й': '<emoji id=5195365902085792989>🔤</emoji>',
    'к': '<emoji id=5456289915551622074>🔤</emoji>',
    'л': '<emoji id=5474517911374668774>🔤</emoji>',
    'м': '<emoji id=5469720553164122863>🔤</emoji>',
    'н': '<emoji id=5469708475716085118>🔤</emoji>',
    'о': '<emoji id=5449645429346020359>🔤</emoji>',
    'п': '<emoji id=5456332233864391674>🔤</emoji>',
    'р': '<emoji id=5465662534918875863>🔤</emoji>',
    'с': '<emoji id=5463032576119679082>🔤</emoji>',
    'т': '<emoji id=5442819107110004737>🔤</emoji>',
    'у': '<emoji id=5188633966051076002>🔤</emoji>',
    'ф': '<emoji id=5199539798548687111>🔤</emoji>',
    'х': '<emoji id=5453904585204704787>🔤</emoji>',
    'ц': '<emoji id=5199431226070412282>🔤</emoji>',
    'ч': '<emoji id=5204235000962098442>🔤</emoji>',
    'ш': '<emoji id=5451785663089224462>🔤</emoji>',
    'щ': '<emoji id=5201857350016708252>🔤</emoji>',
    'ъ': '<emoji id=5472079100094982899>🔤</emoji>',
    'ы': '<emoji id=5190588236300296545>🔤</emoji>',
    'ь': '<emoji id=5472419270094760054>🔤</emoji>',
    'э': '<emoji id=5447451113374624122>🔤</emoji>',
    'ю': '<emoji id=5188362206290388816>🔤</emoji>',
    'я': '<emoji id=5204256643302303428>🔤</emoji>',
    '1': '<emoji id=5235776368905562305>1️⃣</emoji>',
    '2': '<emoji id=5237704680372447424>2️⃣</emoji>',
    '3': '<emoji id=5238044171767393675>3️⃣</emoji>',
    '4': '<emoji id=5235533321001250232>4️⃣</emoji>',
    '5': '<emoji id=5238171599152097811>5️⃣</emoji>',
    '6': '<emoji id=5235500881113263583>6️⃣</emoji>',
    '7': '<emoji id=5237875542761417785>7️⃣</emoji>',
    '8': '<emoji id=5238067300166281132>8️⃣</emoji>',
    '9': '<emoji id=5237872922831367023>9️⃣</emoji>',
    '0': '<emoji id=5238055991517390123>0️⃣</emoji>',
    '!': '<emoji id=5211108619377977503>🔤</emoji>',
    '?': '<emoji id=5210880311801423356>🔤</emoji>',
    '(': '<emoji id=5256085766009793165>🔤</emoji>',
    ')': '<emoji id=5255844096789983205>🔤</emoji>',
    '.': '<emoji id=5255831662859660095>🔤</emoji>',
    ',': '<emoji id=5255809805771090545>🔤</emoji>',
    ' ': '<emoji id=4992465913241404107>🔤</emoji>',
    'a': '<emoji id=5226734466315067436>🔤</emoji>',
    'b': '<emoji id=5330453760395191684>🔤</emoji>', 
    'c': '<emoji id=5330523098347218561>🔤</emoji>', 
    'd': '<emoji id=5361630910816984823>🔤</emoji>', 
    'e': '<emoji id=5332587336939084375>🔤</emoji>', 
    'f': '<emoji id=5330369145244491360>🔤</emoji>', 
    'g': '<emoji id=5361861335812416268>🔤</emoji>',
    'h': '<emoji id=5330133162561380231>🔤</emoji>', 
    'i': '<emoji id=5381808177547321132>🔤</emoji>',
    'j': '<emoji id=5330383228442258084>🔤</emoji>',
    'k': '<emoji id=5330026574357996347>🔤</emoji>',
    'l': '<emoji id=5332396623211274002>🔤</emoji>',
    'm': '<emoji id=5332321341024508571>🔤</emoji>',
    'n': '<emoji id=5359736027080565026>🔤</emoji>',
    'o': '<emoji id=5361583176550457135>🔤</emoji>',
    'p': '<emoji id=5361909160273255840>🔤</emoji>',
    'q': '<emoji id=5361948540828393629>🔤</emoji>',
    'r': '<emoji id=5332514996804918116>🔤</emoji>',
    's': '<emoji id=5332807088940785741>🔤</emoji>',
    't': '<emoji id=5332558333024934589>🔤</emoji>',
    'u': '<emoji id=5330069773139059849>🔤</emoji>',
    'v': '<emoji id=5395613572531232916>🔤</emoji>',
    'w': '<emoji id=5332308237079288987>🔤</emoji>',
    'x': '<emoji id=5332575697577714724>🔤</emoji>',
    'y': '<emoji id=5332648110726323166>🔤</emoji>',
    'z': '<emoji id=5330309934825351007>🔤</emoji>'
}

@Client.on_message(filters.command("prem_text", prefixes=my_prefix()) & filters.me)
async def prem_text(client, message):
    full_text = ' '.join(message.text.lower().split()[1:])
    result = ''
    await client.edit_message_text(message.chat.id, message.id, "Generating text..")
    for i in full_text:
        try:
            result = result + emoji_list[i]
        except:
            result += i
    await client.edit_message_text(message.chat.id, message.id, result)

module_list['PremiumText'] = f'{my_prefix()}prem_text [Text]'
file_list['PremiumText'] = 'premium_text.py'
