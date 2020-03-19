Bot that I made which replies to another bot in discord
Usage:
Install https://discordpy.readthedocs.io/en/latest/

In order for the bot to work, you need atleast 2 accounts. 
One which is the bot, and a second one which sends commands to the BOT and controls it.
"BOT USER ID HERE" on line 250 requires the bot account token.
bot=False if the "bot" account is not an official discord bot, bot=True if it is an official discord bot account.
You also need to change the following id's to be correct.
bot_speaking_channel_id = 0
bot_controller_id = 0
controller_bot_dm_channel_id = 0

The bot can answer all trivia questions (around 400) as of 19/03/2020. And can solve clues and kill minions on it's own.
