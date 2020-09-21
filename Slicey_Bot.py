import asyncio
import discord
import random
import time
import configparser

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
    "Queen": "kq"
}

last_npc = "Zulrah"
asleep = False

currently_running_command = "+mine iron"


@client.event
async def on_connect():
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(bot_speaking_channel_id)
    await channel.send(currently_running_command)


@client.event
async def on_message(message):
    global last_npc, asleep, currently_running_command
    message_time = time.ctime(time.time())
    message_time = message_time.split(" ")
    message_time = list(filter(None, message_time))
    time_split = message_time[3].split(":")
    if asleep:
        if int(time_split[0]) >= 8:
            asleep = False
            channel = client.get_channel(bot_speaking_channel_id)
            await channel.send(currently_running_command)
    if message.channel.id == bot_speaking_channel_id:
        if message.author.id == oldschool_bot_id:
            content = message.content.replace(',', '').replace("'", '')
            message_to_send = ""
            clue = False
            monster = False
            quest = False
            prev_was_clue = False
            mining = False
            cooking = False
            chopping = False
            agility = False
            rc = False
            tier = ""
            if minion_name in content and "finished " in content:
                if "finished killing" in content:
                    monster = True
                elif "finished questing" in content:
                    quest = True
                elif "carefully places the reward casket in your bank." in content:
                    prev_was_clue = True
                elif "finished mining" in content:
                    print("Finished Mining")
                    mining = True
                elif "finished cooking" in content:
                    print("Finished cooking")
                    cooking = True
                elif "finished Woodcutting" in content:
                    print("Finished chopping")
                    chopping = True
                elif "finished crafting" in content and "rune" in content:
                    print("Finished rcing")
                    rc = True
                elif "finished" in content and "laps and fell" in content:
                    agility = True
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
                await asyncio.sleep(random_time)
                if prev_was_clue:
                    message_to_send = currently_running_command
                    await message.channel.send(message_to_send)
                elif clue:
                    message_to_send = "+m clue 1 {0}".format(tier)
                    await message.channel.send(message_to_send)
                else:
                    if random_time < 120:
                        message_to_send = message.content.split("Say `")[1][0]
                        await message.channel.send(message_to_send)
                    else:
                        if monster:
                            message_to_send = "+m kill {0}".format(monsters_to_kill[last_npc])
                        elif quest:
                            message_to_send = "+m quest"
                        elif mining:
                            print("mining iron")
                            message_to_send = "+mine iron"
                        elif cooking:
                            print("making jugs of wine")
                            message_to_send = "+cook jug of wine"
                        elif agility:
                            print("running laps")
                            message_to_send = "+laps ardougne"
                        elif chopping:
                            print("chopping")
                            message_to_send = "+chop sulliusceps"
                        elif rc:
                            print("rcing")
                            message_to_send = "+rc astral"
                        currently_running_command = message_to_send
                        await message.channel.send(message_to_send)
            return

config = configparser.ConfigParser()
config.read("bot_config.txt")

oldschool_bot_id = config['DEFAULT']['oldschool_bot_id']  # the bot that my bot replies to, DON'T CHANGE
bot_speaking_channel_id = config['DEFAULT']['bot_speaking_channel_id']  # My server bot channel
minion_name = config['MAIN_ACCOUNT']['minion_name']
client.run(config['MAIN_ACCOUNT']['client_id'], bot=False)
