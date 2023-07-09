"""
This script forward all videos from telegram chennel, so bot сan have access to all this messages 
"""

import asyncio
from telethon.sync import events
from telethon import utils
from telethon import TelegramClient
from telethon.tl import functions, types

client = TelegramClient('Parser', '111111111', '1111111111111111111111111')
client.start()

sourse = ["https://t.me/somechannel"]
botLink = "https://t.me/mybot"

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
