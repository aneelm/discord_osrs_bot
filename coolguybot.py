import discord, asyncio, random, pandas as pd

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


allowed = False
minus_trivia_enabled = True
prev_message = ""
trivia_answers = []
bot_commands = {
    "enable trivia": "Enable -trivia",
    "disable trivia": "Disable -trivia",
    "start": "Bot will start asking osrsbot for +trivia",
    "stop": "Bot will stop asking osrsbot for +trivia",
    "daily": "Bot will ask osrsbot for it's +daily",
    "commands": "Show all bot commands",
    "send message": "send message=YOUR MESSAGE HERE(Currently only in gangshit osrs-bot channel"
}
commands = ""
for key, value in bot_commands.items():
    commands += "Command: \"" + key + "\" " + "Explanation: \"" + value + "\".\n"
osrs_bot_channel_id = 612985926993575936
oldschool_bot_id = 303730326692429825
slicey_id = 463640358019006464
slicey_dm_channel_id = 677077227292065802


@client.event
async def check_pm_commmands(message):
    global allowed, minus_trivia_enabled, commands
    gang_shit_bot_channel = client.get_channel(osrs_bot_channel_id)
    if message.author.id == slicey_id:
        if "enable trivia" == message.content:
            minus_trivia_enabled = True
            await message.channel.send("Enabled -trivia")
        if "disable trivia" == message.content:
            minus_trivia_enabled = False
            await message.channel.send("Disabled -trivia")
        if "start" == message.content:
            allowed = True
            await message.channel.send("Bot is gonna ask for trivia.")
            await gang_shit_bot_channel.send('+trivia')
        if "daily" == message.content:
            await message.channel.send("Bot is gonna ask for a daily.")
            await gang_shit_bot_channel.send('+daily')
        if "stop" == message.content:
            allowed = False
            await message.channel.send("Bot has stopped asking.")
        if "commands" == message.content:
            await message.channel.send(commands)
        if "send message" in message.content and "=" in message.content:
            split_message = message.content.split("=")
            await gang_shit_bot_channel.send(split_message[1])
        return


@client.event
async def answer_trivia(message):
    global prev_message, allowed
    if message.guild.id == 342983479501389826:
        if message.channel.id == 346304390858145792:
            if message.author.id == oldschool_bot_id:
                content = message.content.replace(',', '')
                content = content.replace("'", '')
                if content[:17] == "**Daily Trivia:**":
                    content = content[18:]
                if "Nobody answered correctly" in content or "had the right answer" in content or \
                        "and received..." in content or "ou can claim your next daily" in content or \
                        "is currently killing" in content or "You cannot use this command" in content or \
                        "finished killing" in content or "pat" in content.lower() or \
                        "Do clue scrolls" in content or "is currently doing nothing" in content or \
                        "You can assign" in content or "- " in content or "<:" in content:
                    return
                if content in dictionary:
                    await asyncio.sleep(1)
                    await message.channel.send(dictionary[content])
                    print(content + " : " + dictionary[content])
                return


@client.event
async def on_message(message):
    if message.channel.id == slicey_dm_channel_id:
        await check_pm_commmands(message)
    await answer_trivia(message)
    return


unanswered_trivia = []
dictionary = dict()
questions = []
answers = []


@client.event
async def send_message(message):
    await message.channel.send('+trivia')


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


def read_unanswered():
    read = "unanswered_trivia.csv"
    reader = pd.read_csv(read)
    for message in reader.values:
        unanswered_trivia.append(message)


read_file_with_answers()
read_unanswered()
# client.run("Njc2ODEyMTU3NjA1OTA0Mzg0.XkLIgg.PvwZosZ0eWfB42MuyyVHr0Y9HXU")  # test bot
# client.run("Mjc5NjQ5NDQ3OTEzMzI0NTQ0.XkFMpA.gsKZfh-NWUIuBPErrglP8gM41gU", bot=False)  # Eelma kasutaja
client.run("Njc3MTU5NjcwMjg4MzUxMjMz.XkQNUQ.gnkNF7GZCW4gsWO-q5QwpjFobe4", bot=False)  # CooolGuy22#7096 kasutaja
print("x")
