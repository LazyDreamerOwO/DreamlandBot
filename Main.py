import os, random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv(".env")

intents = discord.Intents.default()
intent.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message}: ({channel})')

    if message.author == bot.user:
        return

    if message.channel.name == 'bot-test':
        if user_message == 'hello':
            await message.channel.send(f'Hello {username}!')
            return
        elif user_message == 'bye':
            await message.channel.send(f'Goodbye {username}!')
            return

@bot.command(name="dice")
async def dice(ctx, sides: int):
    """Roll single dice with N sides"""
    await ctx.send(f"You rolled a {random.randint(1, sides)} on a {sides} sided dice!")

bot.run(os.environ.get("DiscordBotToken"))
