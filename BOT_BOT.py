import asyncio
import discord
import random
import time
import configparser
import re
import pandas as pd
import sys
from enum import Enum

try:
    ACCOUNT = sys.argv[1]
except IndexError:
    raise Exception("No argument for account type was present, available values are: ['MAIN', 'ALT]")


class EventEndMessageEnum(Enum):
    NIGHTMARE = "died in all their attempts to kill the nightmare"
    MONSTER = "finished killing"
    QUEST = "finished questing"
    PREV_WAS_CLUE = "carefully places the reward casket in your bank"
    MINING = "finished mining"
    COOKING = "finished cooking"
    WOODCUTTING = "finished woodcutting"
    SMITHING = "finished smelting"
    RC = "finished crafting rune"
    AGILITY = "finished laps and fell"
    CLUE = "you got clue scrolls in your loot"
    FISHING = "finished fishing"
    HALLOWEEN = "finished trick or treating!"
    HALLOWED = "finished doing the hallowed sepulchre"
    TRAWLER = "finished completing trawler"
    DIANGO = "diango asks"
    CRAFTING = "finished crafting"


client = discord.Client()
dictionary = dict()
asleep = False


@client.event
async def on_connect():
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(bot_speaking_channel_id)
    await channel.send(config[ACCOUNT]['currentCommand'])


async def can_send_messages(time_split) -> bool:
    global asleep
    # Should go to sleep:
    if 0 <= int(time_split[0]) < 8 and not asleep:
        print(time_split[0])
        asleep = True
        return False
    # Check if asleep and needs to wake up.
    if asleep:
        if int(time_split[0]) >= 8:
            asleep = False
            await asyncio.sleep(determine_wait_time())
            channel = client.get_channel(bot_speaking_channel_id)
            await channel.send(config[ACCOUNT]['currentCommand'])
        return False
    return True


def author_and_channel_match(message) -> bool:
    if message.channel.id == bot_speaking_channel_id:
        if message.author.id == oldschool_bot_id:
            return True
    return False


def is_dm_message(message) -> bool:
    if message.channel.id == dm_channel_id:
        if message.author.id == dm_channel_controller_id:
            return True
    return False


def determine_event(content):
    for name, member in EventEndMessageEnum.__members__.items():
        enum_value_list = member.value.split()
        content_list = content.split()
        result = all(elem in content_list for elem in enum_value_list)
        if result:
            return member
    return None


def determine_command(message):
    split_message = message.split()
    for item in config['MONSTERS'].items():
        values = item[1].split(",")
        for word in split_message:
            for value in values:
                if word.lower() in value.lower():
                    return values[0]
    return ""


def determine_message_to_send(event, content, time_to_await) -> str:
    message_to_send = ""
    events_that_can_not_be_repeated_by_char = [
        EventEndMessageEnum.NIGHTMARE,
        EventEndMessageEnum.CLUE,
        EventEndMessageEnum.PREV_WAS_CLUE,
        EventEndMessageEnum.DIANGO
    ]
    try:
        if event is None:
            print(content)
            return ""
        overwrite_prev_command = True

        if EventEndMessageEnum.DIANGO == event:
            content = content.split("...** ")[1]
            if content in dictionary:
                message_to_send = dictionary[content]
                overwrite_prev_command = False
        if time_to_await < 115 and event not in events_that_can_not_be_repeated_by_char:
            overwrite_prev_command = False
            message_to_send = re.search("(?<=say `)(.*)(?=` to repeat this trip)", content).group(1)
        elif EventEndMessageEnum.MONSTER == event:
            npc_in_message = re.search("(?<=your )(.*)(?= kc)", content).group(1)
            try:
                message_to_send = config['MONSTERS'][npc_in_message].split(",")[0]
                print("Killing {}.".format(npc_in_message))
            except KeyError:
                print("{} was not found in {} config.".format(npc_in_message, "MONSTERS"))
                defaulting_to = config[ACCOUNT]['defaultNPC'].lower()
                message_to_send = config['MONSTERS'][defaulting_to].split(",")[0]
                print("Defaulting to {}.".format(defaulting_to))
        elif EventEndMessageEnum.NIGHTMARE == event:
            print("Killing nightmare.")
            message_to_send = "+nightmare solo"
        elif EventEndMessageEnum.FISHING == event:
            # Example:
            # fish_with_amount = 280 salmon
            # fish = salmon
            fish_with_amount = re.search("(?<=finished fishing )(.*)(?= you also received)", content).group(1)
            fish = fish_with_amount.split()[1]
            message_to_send = "+fish {}".format(fish)
        elif EventEndMessageEnum.AGILITY == event:
            # Example:
            # course_with_amount = 40 canifis Rooftop Course
            # course = canifis
            course_with_amount = re.search("(?<=finished )(.*)(?= laps and fell on)", content).group(1)
            course = course_with_amount.split()[1]
            if course == "al":
                course = "al kharid"
            message_to_send = "+laps {}".format(course)
        elif EventEndMessageEnum.WOODCUTTING == event:
            # Example:
            # log_with_amount = 60 yew log
            # log = yew
            log_with_amount = re.search("(?<=finished woodcutting )(.*)(?= you also received)", content).group(1)
            log = log_with_amount.split()[1]
            message_to_send = "+chop {}".format(log)
        elif EventEndMessageEnum.MINING == event:
            # Example:
            # ore_with_amount = 512 iron ore
            # ore = iron
            ore_with_amount = re.search("(?<=finished mining )(.*)(?= you also received)", content).group(1)
            ore = ore_with_amount.split()[1]
            message_to_send = "+mine {}".format(ore)
        elif EventEndMessageEnum.COOKING == event:
            # Example:
            # food_with_amount = 60 shark
            # food = shark
            food_with_amount = re.search("(?<=finished cooking )(.*)(?= you also received)", content).group(1)
            food = food_with_amount.split()[1]
            if food == "jug":
                food = "wine"
            message_to_send = "+cook {}".format(food)
        elif EventEndMessageEnum.RC == event:
            # Example:
            # rune_with_amount = 3996 astral
            # rune = astral
            rune_with_amount = re.search("(?<=finished crafting )(.*)(?= rune you also received)", content).group(1)
            rune = rune_with_amount.split()[1]
            message_to_send = "+rc {}".format(rune)
        elif EventEndMessageEnum.SMITHING == event:
            # Example:
            # bar_with_amount = 20x gold bar
            # bar = gold
            bar_with_amount = re.search("(?<=smelting )(.*)(?= you also received)", content).group(1)
            bar = bar_with_amount.split()[1].lower()
            message_to_send = "+smelt {}".format(bar)
        elif EventEndMessageEnum.CRAFTING == event:
            material_with_amount = re.search("(?<=crafting )(.*)(?= you also received)", content).group(1)
            material_list = material_with_amount.split()
            material = material_list[1:]
            message_to_send = "+craft {}".format(" ".join(material))
        elif EventEndMessageEnum.QUEST == event:
            print("Questing.")
            message_to_send = "+m quest"
        elif EventEndMessageEnum.PREV_WAS_CLUE == event:
            print("Repeating last event after completing a clue.")
            overwrite_prev_command = False
            message_to_send = config[ACCOUNT]['currentCommand']
            pass
        elif EventEndMessageEnum.CLUE == event:
            overwrite_prev_command = False
            tier_in_message = re.search("(?<=you got clue scrolls in your loot \\()(.*)(?=\\)\\.)", content).group(1)
            message_to_send = "+m clue 1 {}".format(tier_in_message)
            print("Completing {} clue".format(tier_in_message))
        elif EventEndMessageEnum.HALLOWEEN == event:
            message_to_send = "+trickortreat"
        elif EventEndMessageEnum.HALLOWED == event:
            message_to_send = "+sepulchre"
        elif EventEndMessageEnum.TRAWLER == event:
            message_to_send = "+trawler"
        if overwrite_prev_command:
            config.wr
            config[ACCOUNT]['currentCommand'] = message_to_send
            with open('bot_config.cfg', 'w') as configfile:
                config.write(configfile)
        return message_to_send
    except AttributeError:
        print("----------------ERROR------------------")
        print(event)
        print(content)
        print(time_to_await)
        print("----------------ERROR------------------")
        return ""


def determine_wait_time():
    weighted = [320, 320, 320, 320, 320, 720, 720, 720, 1440, 2222]
    random_time = random.randrange(10, weighted[random.randrange(0, 10)])
    return random_time


def bot_should_reply(content):
    content = content.lower()
    if minion_name in content and 'currently killing' not in content and 'now killing' not in content:
        return True
    if client.user.name.lower() in content and 'diango asks' in content:
        return True
    return False


@client.event
async def on_message(message):
    message_time = time.ctime(time.time()).split(" ")
    message_time = list(filter(None, message_time))
    time_split = message_time[3].split(":")
    if await can_send_messages(time_split):
        if author_and_channel_match(message):
            content = message.content.replace(',', '').replace("'", '').lower()
            if bot_should_reply(content):
                event = determine_event(content)
                time_to_await = 3
                if event != EventEndMessageEnum.DIANGO:
                    time_to_await = determine_wait_time()
                message_to_send = determine_message_to_send(event, content, time_to_await)
                if message_to_send:
                    print("Waiting for {0} seconds".format(time_to_await))
                    await asyncio.sleep(time_to_await)
                    print(message_to_send)
                    await message.channel.send(message_to_send)
        if ACCOUNT == "ALT":
            if is_dm_message(message):
                channel = client.get_channel(bot_speaking_channel_id)
                message_content = message.content.lower()
                message_to_send = ""
                if "send=" in message_content:
                    split_message = message.content.split("=")
                    if len(split_message) > 2:
                        message_to_send = split_message[1] + "=" + split_message[2]
                    else:
                        message_to_send = split_message[1]
                elif "daily" == message_content:
                    message_to_send = "+daily"
                elif "quest" in message_content:
                    message_to_send = "+m quest"
                elif "stats" in message_content:
                    message_to_send = "+m stats"
                if message_to_send == "":
                    message_to_send = determine_command(message.content)
                if message_to_send == "":
                    return
                await channel.send(message_to_send)


def read_file_with_answers():
    read = "trivia.csv"
    reader = pd.read_csv(read)
    for message in reader.values:
        question = message[0].replace(',', '')
        question = question.replace("'", '')
        question = question.lower()
        answer = message[1].lower()
        dictionary[question] = answer


read_file_with_answers()

config = configparser.ConfigParser()
config.read("bot_config.cfg")

if ACCOUNT == "ALT":
    dm_channel_controller_id = int(
        config['DEFAULT']['bot_controller_id'])
    dm_channel_id = int(
        config['DEFAULT']['controller_bot_dm_channel_id'])
oldschool_bot_id = int(config['DEFAULT']['oldschool_bot_id'])  # the bot that my bot replies to, DON'T CHANGE
bot_speaking_channel_id = int(config['DEFAULT']['bot_speaking_channel_id'])  # My server bot channel
minion_name = config[ACCOUNT]['minion_name']
client.run(config[ACCOUNT]['client_id'], bot=False)
