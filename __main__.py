import os, asyncio, importlib

from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv(".env")
bot = commands.Bot(command_prefix='/')

# todo: use discord_slash?

def load_cogs(bot):
    """load commands cogs from commands.py"""
    loaded = importlib.import_module(".", "commands")
    importlib.reload(loaded)
    for attr in loaded.__dict__:
        obj = getattr(loaded, attr)
        if issubclass(type(obj), commands.cog.CogMeta):
            print(f"-- {obj.__name__} cog was loaded")
            bot.add_cog(obj(bot))

async def reload_cogs(bot):
    cogs = bot.cogs.copy()
    for cog in cogs:
        bot.remove_cog(cog)
    load_cogs(bot)

@bot.event
async def on_ready():
    print(f"-- We have logged in as {bot.user}")

# todo: make that only developers could run it
@bot.command(hidden=True)
# @commands.is_owner()
async def reload(ctx):
    """Reload bot and all registered cogs"""
    await ctx.send("-- Reloading bot...")
    try:
        await reload_cogs(ctx.bot)
        await ctx.send(f"-- Reloaded successfully")
    except Exception as e:
        await ctx.send(f"-- Error on cogs reloading: {e.__str__()}")

@bot.event
async def on_message(message):
    username = message.author.name
    user_message = message.content
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == bot.user:
        return

    elif user_message == 'hello':
        await message.reply(f'Hello, {username}!', mention_author=True)
        return
    elif user_message == 'bye':
        await message.reply(f'Goodbye, {username}!', mention_author=True)
        return
    else:
        await bot.process_commands(message)

token = os.environ.get("DiscordBotToken")
if token is not None:
    load_cogs(bot)
    bot.run(os.environ.get("DiscordBotToken"))
else:
    raise Exception("No token available in environment")
