import asyncio

import discord

client = discord.Client()

count = 0


@client.event
async def on_message(message):
    global count
    if count * 1000 >= 100000:
        await asyncio.sleep(3)
        await message.channel.send("+b feather")
        exit()
    if message.channel.id == bot_speaking_channel_id:
        if message.author.id == oldschool_bot_id:
            message_to_send = ""
            if '<@463640358019006464>, say `confirm` to confirm that you want to purchase 1,000x Feather for 10k.' in message.content:
                message_to_send = "confirm"
            elif 'You purchased 1,000x Feather for 10k.' in message.content:
                message_to_send = "+buy feather"
                count += 1
                print("I have bought " + str(count * 1000) + " feathers.")
            if message_to_send is not "":
                await asyncio.sleep(3)
                await message.channel.send(message_to_send)


oldschool_bot_id = 303730326692429825
bot_speaking_channel_id = 0
client.run("", bot=False)
