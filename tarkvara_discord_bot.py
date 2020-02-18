import time

import discord

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


tarkvaratehnika_id = 671097134145339422


@client.event
async def on_message(message):
    try:
        if message.guild.id == tarkvaratehnika_id:
            message_time = time.ctime(time.time())
            message_to_write_part_1 = "{0} - {1} - {2}({3})".format(message_time, message.channel, message.author,
                                                                    message.author.id)
            message_to_write_part_2 = message.content
            write_to_file(message.channel, [message_to_write_part_1, message_to_write_part_2])
    except AttributeError:
        pass


write = "_tarkvaratehnika.log"


def write_to_file(channel_name, message):
    with open("logs/" + str(channel_name) + write, "a") as o:
        o.write(message[0] + "\n")
        o.write(message[1] + "\n")


client.run("NDYzNjQwMzU4MDE5MDA2NDY0.XjSv5g.2XACnLL50uR0JnSm90JVUaIIRCI", bot=False)
