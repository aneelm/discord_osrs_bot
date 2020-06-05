import asyncio
import discord
import pandas as pd
import random
import time

print("test")

client = discord.Client()
monsters_to_kill = {
    "Barrows": "barrows",
    "Prime": "prime",
    "Rex": "rex",
    "Supreme": "supreme",
    "Cerberus": "cerb",
    "Mole": "mole",
    "Vorkath": "vork",
    "Zulrah": "zulrah",
    "Graardor": "bandos",
    "Zilyana": "sara",
    "Kreearra": "arma",
    "Tsutsaroth": "zammy",
    "Man": "man",
    "Guard": "guard",
    "Woman": "woman",
    "Goblin": "goblin",
    "Callisto": "callisto",
    "Vetion": "vetion",
    "Venenatis": "venenatis",
    "Elemental": "chaos ele",
    "Fanatic": "chaos fanatic",
    "Archaeologist": "crazy arch",
    "Dragon": "kbd",
    "Scorpia": "scorpia",
    "Beast": "corp",
    "Shaman": "shaman",
    "Queen" : "kq"
}

last_npc = "Zulrah"
asleep = False



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global last_npc, asleep
    message_time = time.ctime(time.time())
    message_time = message_time.split(" ")
    message_time = list(filter(None, message_time))
    time_split = message_time[3].split(":")
    if asleep:
        if int(time_split[0]) >= 8:
            asleep = False
            channel = client.get_channel(bot_speaking_channel_id)
            await channel.send("+m kill {0}".format(monsters_to_kill[last_npc]))
    if message.channel.id == bot_speaking_channel_id:
        if message.author.id == oldschool_bot_id:
            content = message.content.replace(',', '').replace("'", '')
            message_to_send = ""
            clue = False
            monster = False
            quest = False
            monster_reboot = False
            mining = False
            cooking = False
            tier = ""
            if minion_name in content and "finished " in content:
                if "finished killing" in content:
                    monster = True
                elif "finished questing" in content:
                    quest = True
                elif "finished completing" in content:
                    monster_reboot = True
                elif "finished mining" in content:
                    print("Finished Mining")
                    mining = True
                elif "finished cooking" in content:
                    print("Finished cooking")
                    cooking = True
                if "ou got clue scrolls in your loot " in content:
                    clue = True
                    if "Elite" in content:
                        tier = "elite"
                    if "Hard" in content:
                        tier = "hard"
                    if "Medium" in content:
                        tier = "medium"
                    if "Easy" in content:
                        tier = "easy"
                if 0 <= int(time_split[0]) < 8:
                    asleep = True
                    return
                weighted = [320, 320, 320, 320, 320, 720, 720, 720, 1440, 2222]
                random_time = random.randrange(10, weighted[random.randrange(0, 10)])
                print("Waiting for {0} seconds".format(random_time))
                split_message = content.split(" ")
                if not monster_reboot:
                    boss = split_message[-1].replace(".", " ").rstrip()
                    last_npc = boss
                await asyncio.sleep(random_time)
                if clue:
                    message_to_send = "+m clue 1 {0}".format(tier)
                    await message.channel.send(message_to_send)
                else:
                    if random_time < 120:
                        message_to_send = random.choice(["yes", "y"])
                        await message.channel.send(message_to_send)
                    else:
                        if monster or monster_reboot:
                            message_to_send = "+m kill {0}".format(monsters_to_kill[last_npc])
                        elif quest:
                            message_to_send = "+m quest"
                        elif mining:
                            print("mining gold")
                            message_to_send = "+mine gold"
                        elif cooking:
                            print("making jugs of wine")
                            message_to_send = "+cook jug of wine"
                        await message.channel.send(message_to_send)
            return


oldschool_bot_id = 303730326692429825  # the bot that my bot replies to, DON'T CHANGE
bot_speaking_channel_id = 0
minion_name = ""
client.run("", bot=False)


print("test")