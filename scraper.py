"""
This script forwards videos to bot, starting from saved date/time
Used to update bot's videobase
"""

import datetime
import asyncio

from telethon.sync import events
from telethon import utils
from telethon import TelegramClient
from telethon.tl import functions, types

client = TelegramClient('Parser', '1111111111', '1111111111111111111111111')
client.start()


async def main():
    dubbers = ["https://t.me/someFollowedChannels"]
    quantity = 0

    with open("lastDate.txt", "r") as fp:
        lastDate = datetime.datetime.strptime(fp.read(), "%Y-%m-%d %H:%M:%S")

    for i in dubbers:
        async for message in client.iter_messages(i, reverse = True, offset_date = lastDate):
            if message.video != None and message.text != None:

                await client.forward_messages("https://t.me/MyBot", messages=message)
                quantity += 1
    deltaTime = datetime.datetime.utcnow() - lastDate

    with open("lastDate.txt", "w") as fp:
        fp.write(str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")))

    await client.send_message("https://t.me/MyBot", "/getFile")
    print(f"Перекинуто {quantity} відео за {deltaTime} часу")
    i = input("Enter Щоб закінчити")


with client:    
    client.loop.run_until_complete(main())
