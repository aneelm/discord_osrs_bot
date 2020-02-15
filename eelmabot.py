import time, discord, asyncio, random, pandas as pd

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
    "Beast": "corp"
}
commands = ""
for key, value in bot_commands.items():
    commands += "Command: \"" + key + "\" " + "Explanation: \"" + value + "\".\n"
osrs_bot_channel_id = 612985926993575936
oldschool_bot_id = 303730326692429825
slicey_id = 463640358019006464
slicey_dm_channel_id = 547056996676009986
mut_id = 141961876790575105


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def check_pm_commmands(message):
    global allowed, minus_trivia_enabled, commands
    gang_shit_bot_channel = client.get_channel(osrs_bot_channel_id)
    if message.author.id == slicey_id:
        message_to_send = ""
        message_time = time.time()
        message_time = time.ctime(message_time)
        log_message_time = message_time.split(" ")
        log_file_name = log_message_time[1] + "_" + log_message_time[2] + "_" + log_message_time[4] + ".log"
        if "enable trivia" == message.content:
            minus_trivia_enabled = True
            message_to_send = "Enabled -trivia"
            await message.channel.send("Enabled -trivia")
        if "disable trivia" == message.content:
            message_to_send = "Disabled -trivia"
            minus_trivia_enabled = False
            await message.channel.send("Disabled -trivia")
        if "start" == message.content:
            allowed = True
            message_to_send = "Bot is gonna ask for trivia."
            await message.channel.send("Bot is gonna ask for trivia.")
            await gang_shit_bot_channel.send('+trivia')
        if "daily" == message.content:
            message_to_send = "Bot is gonna ask for a daily."
            await message.channel.send(message_to_send)
            await gang_shit_bot_channel.send('+daily')
        if "stop" == message.content:
            allowed = False
            message_to_send = "Bot has stopped asking."
            await message.channel.send(message_to_send)
        if "commands" == message.content:
            message_to_send = commands
            await message.channel.send(commands)
            message_to_write_to_file = log_message_time[3] + " - " + message_to_send + "~"
            write_to_log(message_to_write_to_file, log_file_name)
            return
        if "send=" in message.content:
            split_message = message.content.split("=")
            message_to_send = split_message[1]
            await gang_shit_bot_channel.send(split_message[1])
        for value in monsters_to_kill.values():
            if value == message.content:
                message_to_send = "+m kill {0}".format(value.rstrip())
                await gang_shit_bot_channel.send(message_to_send)
        if message_to_send == "":
            return
        message_to_write_to_file = log_message_time[3] + " - " + message_to_send + "~\n"
        write_to_log(message_to_write_to_file, log_file_name)
        return


def write_to_log(message, write):
    if message == "":
        return
    lines = []
    try:
        with open(write, "r") as o:
            lines = o.readlines()
    except IOError:
        print("Creating new log file.")
    with open(write, "w") as o:
        lines = filter(lambda x: x.strip(), lines)
        o.write("".join(lines))
        o.write(message + "\n")


@client.event
async def answer_message(message):
    global allowed, ignored_messages
    if message.channel.id == osrs_bot_channel_id:
        if message.author.id == oldschool_bot_id:
            content = message.content.replace(',', '').replace("'", '')
            message_time = time.ctime(time.time())
            log_message_time = message_time.split(" ")
            log_file_name = log_message_time[1] + "_" + log_message_time[2] + "_" + log_message_time[4] + ".log"
            message_to_send = ""
            if "Diango asks..." in content:
                content = content.split("Diango asks...** ")[1]
            if "**beepboop**" in content and "finished killing" in content:
                time_split = log_message_time[3].split(":")
                if 23 < int(time_split[0]) < 24 or 0 < int(time_split[0]) < 8:
                    return
                weighted = [320, 320, 320, 320, 320, 720, 720, 720, 1440, 2222]
                random_time = random.randrange(10, weighted[random.randrange(0, 10)])
                print("Waiting for {0} seconds".format(random_time))
                split_message = content.split(" ")
                boss = split_message[-1].replace(".", " ").rstrip()
                await asyncio.sleep(random_time)
                if random_time < 120:
                    message_to_send = "yes"
                    await message.channel.send(message_to_send)
                    message_to_write_to_file = log_message_time[3] + " - " + message_to_send + "~\n"
                    write_to_log(message_to_write_to_file, log_file_name)
                else:
                    message_to_send = "+m kill {0}".format(monsters_to_kill[boss])
                    await message.channel.send(message_to_send)
                    message_to_write_to_file = log_message_time[3] + " - " + message_to_send + "~\n"
                    write_to_log(message_to_write_to_file, log_file_name)
                return
            for ignored in ignored_messages:
                if ignored in content.lower():
                    return
            if content in dictionary:
                await asyncio.sleep(1)
                await message.channel.send(dictionary[content])
                message_to_write_to_file = log_message_time[3] + " - " + content + " : " + dictionary[content] + "~\n"
                write_to_log(message_to_write_to_file, log_file_name)
            else:
                message_to_write_to_file = log_message_time[3] + " - " + message_to_send + "~\n"
                write_to_log(message_to_write_to_file, log_file_name)
            return


active = True


@client.event
async def on_message(message):
    if message.channel.id == slicey_dm_channel_id:
        await check_pm_commmands(message)
        return
    if active:
        await answer_message(message)
    return


dictionary = dict()
questions = []
answers = []


def write_to_file(message, write):
    with open(write, "a") as o:
        o.write(message + "\n")


def read_file_with_answers():
    read = "trivia.csv"
    reader = pd.read_csv(read)
    for message in reader.values:
        question = message[0].replace(',', '')
        question = question.replace("'", '')
        question = question
        answer = message[1].lower()
        dictionary[question] = answer


read_file_with_answers()
client.run("Mjc5NjQ5NDQ3OTEzMzI0NTQ0.XkFMpA.gsKZfh-NWUIuBPErrglP8gM41gU", bot=False)  # Eelma kasutaja
