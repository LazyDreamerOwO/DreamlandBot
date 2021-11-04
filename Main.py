import os, random
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv(".env")

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = message.content
    channel = str(message.channel.name)
    print(f'{username}: {user_message}: ({channel})')

    if message.author == bot.user:
        return

    elif message.mentions is discord.User:
        process_user_mention(message, message.mentions)

    elif user_message == 'hello':
        await message.reply(f'Hello {username}!', mention_author=True)
        return
    elif user_message == 'bye':
        await message.reply(f'Goodbye {username}!', mention_author=True)
        return
    else:
        await bot.process_commands(message)

async def process_user_mention(message, user: discord.User):
    """Process message with mention of single user"""
    if message.content.startswith("!bonk"):
        author = str(message.author).split('#')[0]
        await message.channel.send(f"{author} bonked {user.name}!")

@bot.command()
async def dice(ctx, sides: int = 6):
    """Roll single dice with N sides"""
    sides = max(sides, 2)
    await ctx.send(f"You rolled a {random.randint(1, sides)} on a {sides} sided dice!")

@bot.command()
async def info(ctx, *words):
    """Specifies probability of given event in message"""
    # idea: make that random nonsense would be placed in message if no message is given
    chance = random.choice(range(101))
    msg = " ".join(words)
    await ctx.send(f"{chance}% chance that {msg}")

bot.run(os.environ.get("DiscordBotToken"))
