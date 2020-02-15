import discord

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    pass


indova_guild_id = 369813150113071105
gang_shit_guild_id = 612690766086537235
slicey_id = 463640358019006464
mut_id = 141961876790575105


@client.event
async def on_message(message):
    if message.author.name == "Shaun":
        print(message.author.id)
    if message.author.id == mut_id:
        user = client.get_user(mut_id)
        await message.channel.send("ANNOYING MUT DO NOT BE ALARMED {0}!".format(user.mention))
        print("Typed in " + str(message.channel))
    try:
        return
    except AttributeError:
        return


client.run("NDYzNjQwMzU4MDE5MDA2NDY0.XjSv5g.2XACnLL50uR0JnSm90JVUaIIRCI", bot=False)
