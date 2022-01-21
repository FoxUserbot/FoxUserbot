from pyrogram import Client, filters
from pyrogram.types import Message
from covid import Covid
from plugins.settings.main_settings import module_list, file_list, settings, requirements_list

prefix = settings['prefix']

@Client.on_message(filters.command("covid", prefixes=prefix) & filters.me)
async def covid_local(client: Client, message: Message):
    region = " ".join(message.command[1:])
    await message.edit("<code>Data retrieval...</code>")
    covid = Covid(source="worldometers")
    try:
        local_status = covid.get_status_by_country_name(region)
        await message.edit(
            "<b>=======🦠 COVID-19 STATUS 🦠=======</b>\n"
            + f"<b>Region</b>: <code>{local_status['country']}</code>\n"
            + "<b>====================================</b>\n"
            + f"<b>🤧 New cases</b>: <code>{local_status['new_cases']}</code>\n"
            + f"<b>😷 New deaths</b>: <code>{local_status['new_deaths']}</code>\n"
            + "<b>====================================</b>\n"
            + f"<b>😷 Сonfirmed</b>: <code>{local_status['confirmed']}</code>\n"
            + f"<b>❗️ Active:</b> <code>{local_status['active']}</code>\n"
            + f"<b>⚠️ Critical</b>: <code>{local_status['critical']}</code>\n"
            + f"<b>💀 Deaths</b>: <code>{local_status['deaths']}</code>\n"
            + f"<b>🚑 Recovered</b>: <code>{local_status['recovered']}</code>\n"
        )
    except ValueError:
        await message.edit(f'<code>There is no region called "{region}"</code>')


@Client.on_message(filters.command("regions", prefixes=prefix) & filters.me)
async def regions(client: Client, message: Message):
    countr = ""
    await message.edit("<code>Data retrieval...</code>")
    covid = Covid(source="worldometers")
    regions = covid.list_countries()
    for region in regions:
        region = f"{region}\n"
        countr += region
    await message.edit(f"<code>{countr}</code>")

module_list['StatisticsCovid19'] = f'{prefix}covid [region]'
requirements_list.append('covid')
file_list['StatisticsCovid19'] = 'covid.py'