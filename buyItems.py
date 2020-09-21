import asyncio
import configparser

import discord

client = discord.Client()

count = 0


@client.event
async def on_message(message):
    global count
    if count * 1000 >= 150000:
        await asyncio.sleep(3)
        await message.channel.send("+b feather")
        exit()
    if message.channel.id == bot_speaking_channel_id:
        if message.author.id == oldschool_bot_id:
            message_to_send = ""
            if ', say `confirm` to confirm that you want to purchase 1,000x Feather for 10k.' in message.content:
                if buy_from in message.content:
                    message_to_send = "confirm"
            elif 'You purchased 1,000x Feather for 10k.' in message.content:
                message_to_send = "+buy feather"
                count += 1
                print("I have bought " + str(count * 1000) + " feathers.")
            if message_to_send != "":
                await asyncio.sleep(3)
                await message.channel.send(message_to_send)


config = configparser.ConfigParser()
config.read("bot_config.txt")

buy_from = config['ALT_ACCOUNT']['account_at']
oldschool_bot_id = config['DEFAULT']['oldschool_bot_id']  # the bot that my bot replies to, DON'T CHANGE
bot_speaking_channel_id = config['DEFAULT']['bot_speaking_channel_id']  # My server bot channel
client.run(config['MAIN_ACCOUNT']['client_id'], bot=False)
