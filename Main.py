import os, random
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv(".env")

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def dice(ctx, sides: int = 6):
    """Roll single dice with N sides"""
    sides = max(sides, 2)
    await ctx.send(f"You rolled a {random.randint(1, sides)} on a {sides} sided dice!")

# todo make global registry of such commands to mimic @bot.command interface
async def info(message):
    """Specifies probability of given event in message"""
    # idea: make that random nonsense would be placed in message if no message is given
    chance = random.choice(range(101))
    if chance == 69:
        await message.channel.send(f"9000% chance that {message.content}")
    else:
        await message.channel.send(f"{chance}% chance that {message.content}")

async def process_text_command(message):
    """Bypass parsing of args by Bot.command
    Return true if message was consumed, otherwise false"""
    if message.content.startswith("!info"):
        info()
        return True

    return False

async def process_user_mention_command(message, user: discord.User):
    """Process message with mention of single user"""
    if message.content.startswith("!bonk"):
        author = str(message.author).split('#')[0]
        await message.channel.send(f"{author} bonked {user.name}!")

@bot.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = message.content
    channel = str(message.channel.name)
    print(f'{username}: {user_message}: ({channel})')

    if message.author == bot.user:
        return

    text_command_consumed = await process_text_command(message)
    if text_command_consumed:
        return

    elif message.mentions is discord.User:
        await process_user_mention_command(message, message.mentions)

    elif user_message == 'hello':
        await message.reply(f'Hello {username}!', mention_author=True)
        return
    elif user_message == 'bye':
        await message.reply(f'Goodbye {username}!', mention_author=True)
        return
    else:
        await bot.process_commands(message)

bot.run(os.environ.get("DiscordBotToken"))
