import asyncio
import discord
import random
import time
import configparser
import re
from enum import Enum


class EventEndMessageEnum(Enum):
    NIGHTMARE = "died in all their attempts to kill the nightmare"
    MONSTER = "finished killing"
    QUEST = "finished questing"
    PREV_WAS_CLUE = "carefully places the reward casket in your bank"
    MINING = "finished mining"
    COOKING = "finished cooking"
    WOODCUTTING = "finished woodcutting"
    RC = "finished crafting rune"
    AGILITY = "finished laps and fell"
    CLUE = "you got clue scrolls in your loot"


client = discord.Client()

asleep = False


@client.event
async def on_connect():
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(bot_speaking_channel_id)
    await channel.send(config['MAIN_ACCOUNT']['currentCommand'])


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
            channel = client.get_channel(bot_speaking_channel_id)
            await channel.send(config['MAIN_ACCOUNT']['currentCommand'])
    return True


def author_and_channel_match(message) -> bool:
    if message.channel.id == bot_speaking_channel_id:
        if message.author.id == oldschool_bot_id:
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


def determine_message_to_send(event, content, time_to_await) -> str:
    message_to_send = ""
    events_that_can_not_be_repeated_by_char = [
        EventEndMessageEnum.NIGHTMARE,
        EventEndMessageEnum.CLUE,
        EventEndMessageEnum.PREV_WAS_CLUE
    ]
    overwrite_prev_command = True
    if time_to_await < 115 and event not in events_that_can_not_be_repeated_by_char:
        overwrite_prev_command = False
        message_to_send = re.search("(?<=say `)(.*)(?=` to repeat this trip)", content).group(1)
    elif EventEndMessageEnum.MONSTER == event:
        npc_in_message = re.search("(?<=your )(.*)(?= kc)", content).group(1)
        try:
            npc_to_say = config['MONSTERS'][npc_in_message]
            print("Killing {}.".format(npc_to_say))
        except KeyError:
            print("{} was not found in {} config.".format(npc_in_message, "MONSTERS"))
            npc_to_say = config['MAIN_ACCOUNT']['defaultNPC']
            print("Defaulting to {}.".format(npc_to_say))
        if npc_in_message == "nightmare":
            message_to_send = "+nightmare solo"
        else:
            message_to_send = "+m kill {}".format(npc_to_say)
    elif EventEndMessageEnum.NIGHTMARE == event:
        print("Killing nightmare.")
        message_to_send = "+nightmare solo"
    elif EventEndMessageEnum.AGILITY == event:
        # TODO:
        pass
    elif EventEndMessageEnum.WOODCUTTING == event:
        # TODO:
        pass
    elif EventEndMessageEnum.MINING == event:
        # TODO:
        pass
    elif EventEndMessageEnum.COOKING == event:
        # TODO:
        pass
    elif EventEndMessageEnum.RC == event:
        # TODO:
        pass
    elif EventEndMessageEnum.QUEST == event:
        print("Questing.")
        message_to_send = "+m quest"
    elif EventEndMessageEnum.PREV_WAS_CLUE == event:
        print("Repeating last event after completing a clue.")
        overwrite_prev_command = False
        message_to_send = config['MAIN_ACCOUNT']['currentCommand']
        pass
    elif EventEndMessageEnum.CLUE == event:
        overwrite_prev_command = False
        tier_in_message = re.search("(?<=you got clue scrolls in your loot \\()(.*)(?=\\)\\.)", content).group(1)
        message_to_send = "+m clue 1 {}".format(tier_in_message)
        print("Completing {} clue".format(tier_in_message))
    if overwrite_prev_command:
        config['MAIN_ACCOUNT']['currentCommand'] = message_to_send
        with open('example.cfg', 'w') as configfile:
            config.write(configfile)
    return message_to_send


def determine_wait_time():
    weighted = [320, 320, 320, 320, 320, 720, 720, 720, 1440, 2222]
    random_time = random.randrange(10, weighted[random.randrange(0, 10)])
    return random_time


def bot_should_reply(content):
    if minion_name in content and 'currently killing' not in content and 'now killing' not in content:
        return True
    return False


@client.event
async def on_message(message):
    if author_and_channel_match(message):
        message_time = time.ctime(time.time()).split(" ")
        message_time = list(filter(None, message_time))
        time_split = message_time[3].split(":")
        if await can_send_messages(time_split):
            content = message.content.replace(',', '').replace("'", '').lower()
            if bot_should_reply(content):
                event = determine_event(content)
                time_to_await = determine_wait_time()
                message_to_send = determine_message_to_send(event, content, time_to_await)
                if message_to_send:
                    print("Waiting for {0} seconds".format(time_to_await))
                    await asyncio.sleep(time_to_await)
                    await message.channel.send(message_to_send)


config = configparser.ConfigParser()
config.read("bot_config.cfg")

oldschool_bot_id = int(config['DEFAULT']['oldschool_bot_id'])  # the bot that my bot replies to, DON'T CHANGE
bot_speaking_channel_id = int(config['DEFAULT']['bot_speaking_channel_id'])  # My server bot channel
minion_name = config['MAIN_ACCOUNT']['minion_name']
client.run(config['MAIN_ACCOUNT']['client_id'], bot=False)
