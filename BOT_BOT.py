import asyncio
import discord
import pandas as pd
import random
import time

client = discord.Client()

allowed = False
minus_trivia_enabled = True
trivia_answers = []
bot_commands = {
    "enable trivia": "Enable -trivia",
    "disable trivia": "Disable -trivia",
    "start": "Bot will start asking osrsbot for +trivia",
    "stop": "Bot will stop asking osrsbot for +trivia",
    "daily": "Bot will ask osrsbot for it's +daily",
    "commands": "Show all bot commands",
    "send": "send=YOUR MESSAGE HERE(Currently only in gangshit osrs-bot channel"
}
ignored_messages = [
    "nobody answered correctly",
    "had the right answer",
    "and received...",
    "ou can claim your next daily",
    "is currently killing",
    "you cannot use this command",
    "finished killing",
    "pat",
    "do clue scrolls"
    "is currently doing nothing"
    "you can assign",
    "- ",
    "<:"
]
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
    "Shaman": "shaman"
}
commands = ""
for key, value in bot_commands.items():
    commands += "Command: \"" + key + "\" " + "Explanation: \"" + value + "\".\n"


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def check_pm_commmands(message):
    global allowed, minus_trivia_enabled, commands
    gang_shit_bot_channel = client.get_channel(bot_speaking_channel_id)
    if message.author.id == bot_controller_id:
        message_to_send = ""
        message_content = message.content.lower()
        if "enable trivia" == message_content:
            minus_trivia_enabled = True
            message_to_send = "Enabled -trivia"
            await message.channel.send("Enabled -trivia")
        if "disable trivia" == message_content:
            message_to_send = "Disabled -trivia"
            minus_trivia_enabled = False
            await message.channel.send("Disabled -trivia")
        if "start" == message_content:
            allowed = True
            message_to_send = "Bot is gonna ask for trivia."
            await message.channel.send("Bot is gonna ask for trivia.")
            await gang_shit_bot_channel.send('+trivia')
        if "daily" == message_content:
            message_to_send = "Bot is gonna ask for a daily."
            await message.channel.send(message_to_send)
            await gang_shit_bot_channel.send('+daily')
        if "stop" == message_content:
            allowed = False
            message_to_send = "Bot has stopped asking."
            await message.channel.send(message_to_send)
        if "commands" == message_content:
            await message.channel.send(commands)
            return
        if "send=" in message_content:
            split_message = message.content.split("=")
            if len(split_message) > 2:
                message_to_send = split_message[1] + "=" + split_message[2]
            else:
                message_to_send = split_message[1]
            await gang_shit_bot_channel.send(message_to_send)
        if "quest" in message_content:
            message_to_send = "+m quest"
            await gang_shit_bot_channel.send(message_to_send)
        if "stats" in message_content:
            message_to_send = "+m stats"
            await gang_shit_bot_channel.send(message_to_send)
        for value in monsters_to_kill.values():
            if value == message_content:
                message_to_send = "+m kill {0}".format(value.rstrip())
                await gang_shit_bot_channel.send(message_to_send)
        if message_to_send == "":
            return
        return


@client.event
async def answer_message(message):
    global allowed, ignored_messages
    if message.channel.id == bot_speaking_channel_id:
        if message.author.id == oldschool_bot_id:
            content = message.content.replace(',', '').replace("'", '')
            message_time = time.ctime(time.time())
            message_time = message_time.split(" ")
            message_time = list(filter(None, message_time))
            message_to_send = ""
            clue = False
            monster = False
            quest = False
            tier = ""
            time_split = message_time[3].split(":")
            if "Diango asks" in content:
                content = content.split("...** ")[1]
            if minion_name in content and ("finished killing" in content or "finished questing" in content):
                if "finished killing" in content:
                    monster = True
                elif "finished questing" in content:
                    quest = True
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
                if 23 <= int(time_split[0]) < 24 or 0 <= int(time_split[0]) <= 8:
                    return
                weighted = [320, 320, 320, 320, 320, 720, 720, 720, 1440, 2222]
                random_time = random.randrange(10, weighted[random.randrange(0, 10)])
                print("Waiting for {0} seconds".format(random_time))
                split_message = content.split(" ")
                boss = split_message[-1].replace(".", " ").rstrip()
                await asyncio.sleep(random_time)
                if clue:
                    message_to_send = "+m clue 1 {0}".format(tier)
                    await message.channel.send(message_to_send)
                else:
                    if random_time < 120:
                        message_to_send = "yes"
                        await message.channel.send(message_to_send)
                    else:
                        if monster:
                            message_to_send = "+m kill {0}".format(monsters_to_kill[boss])
                        elif quest:
                            message_to_send = "+m quest"
                        await message.channel.send(message_to_send)
                return
            for ignored in ignored_messages:
                if ignored in content.lower():
                    return
            if content in dictionary:
                await asyncio.sleep(1)
                await message.channel.send(dictionary[content])
                print(content, dictionary[content])
            return


active = True


@client.event
async def on_message(message):
    if message.channel.id == controller_bot_dm_channel_id:
        await check_pm_commmands(message)
        return
    if active:
        await answer_message(message)
    return


dictionary = dict()
questions = []
answers = []


def read_file_with_answers():
    read = "trivia.csv"
    reader = pd.read_csv(read)
    for message in reader.values:
        question = message[0].replace(',', '')
        question = question.replace("'", '')
        question = question
        answer = message[1].lower()
        dictionary[question] = answer


oldschool_bot_id = 303730326692429825  # the bot that my bot replies to, DON'T CHANGE
bot_speaking_channel_id = 612985926993575936
bot_controller_id = 0
controller_bot_dm_channel_id = 0
minion_name=""
read_file_with_answers()
client.run("", bot=False)