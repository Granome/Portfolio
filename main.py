"""
This script forward all videos from telegram chennel, so bot han have access to all this messages 
"""

import asyncio
from telethon.sync import events
from telethon import utils
from telethon import TelegramClient
from telethon.tl import functions, types

client = TelegramClient('Parser', '16559463', '757c0689271ce655b48df86483fdb51b')
client.start()

#sourse = ['https://t.me/+bxtLlx4sXU1mZWZi', 'https://t.me/melvoice_berserk_dub', 'https://t.me/+BtTt9W2LXxczYzVi', 'https://t.me/+Dtvtoq-jU0Y4NmVi', 'https://t.me/melvoice_magi_dub', 'https://t.me/+nJLauThWdYRmMzBi', 'https://t.me/melvoice_steinsgate_dub', 'https://t.me/+0Qpa6b7l6Ik0MWIy', 'https://t.me/+JaipwPFWj09hYWMy', 'https://t.me/+Pe__r5gk6QlkY2My', 'https://t.me/+Hucq0PCMYfJjMDdi', 'https://t.me/melvoice_killlakill_dub', 'https://t.me/+26T1siZ60ppmZjli', 'https://t.me/+-jqSnymrBGZhOGZi', 'https://t.me/+fR9tS9rGan4yYTE6', 'https://t.me/+FyQCL3N9k2o5MzYy', 'https://t.me/melvoice_overlord_dub', 'https://t.me/+dNhvS_q_A6pjNDIy', 'https://t.me/+t5UWVdBgVlc4OWEy', 'https://t.me/+NwDMnbAxsdBhNDEy', 'https://t.me/+V3EchtGWzT1mNTgy', 'https://t.me/+mRw14lzVpiVjZmM6', 'https://t.me/+Z0RBMNbRgEZhZTgy', 'https://t.me/melvoice_hyouka_dub', 'https://t.me/+qAdngUYcXSMzMGM6', 'https://t.me/melvoice_youjosenki_dub', 'https://t.me/+dQ6rWgkKgbo0MmNi', 'https://t.me/+1lYQx0rNLdo4MTMy', 'https://t.me/+FO1PjQH0CHw3NDNi', 'https://t.me/+mwy7PBkR95dkZTky', 'https://t.me/+fnZ-LG0ckUs5NmMy', 'https://t.me/+wTAWx3_Mg3thYTQy', 'https://t.me/melvoice_pte_dub', 'https://t.me/+R1HfCah8t6FkMjIy', 'https://t.me/+H1m4QYrx5Po1Y2I6', 'https://t.me/melvoice_senko_dub', 'https://t.me/+L6wtG146siM0Yjhi', 'https://t.me/+O_BCBi7bHLY1OGI6', 'https://t.me/+zqQLjHrupSwyNjdi', 'https://t.me/+qLC-lmHUSe5iMmNi', 'https://t.me/+OvwC33LP7iM0MWVi', 'https://t.me/+F6RwGbUdWQ40NWIy', 'https://t.me/+6yEeEAtJOLU5MGNi', 'https://t.me/+fGPAyOjDJcBlZjUy', 'https://t.me/melvoice_komi_dub', 'https://t.me/+WmGis1SOx8g4Nzli', 'https://t.me/+SRONH7p0AJE3MmQy', 'https://t.me/melvoice_violet_dub', 'https://t.me/+cv7DHaoyJwQwMWZi', 'https://t.me/+d9cyKWNeDo5kNDIy', 'https://t.me/+hXHKoncWI9IyYWNi', 'https://t.me/+mwDp0LHb1pE2NTM6']
sourse = ["https://t.me/PIZDATJULJENJA"]
botLink = "https://t.me/AnimeUkrDubBot"

async def main():
    for i in sourse:
        channel = await client.get_input_entity(i)
        messages = client.iter_messages(channel, reverse=True, limit=None, filter=types.InputMessagesFilterVideo)
        i = 1
        async for message in messages:
            if message.video != None:
                await client.forward_messages(botLink, messages=message)
            i+=1

    input("Finished")





with client:
    client.loop.run_until_complete(main())
