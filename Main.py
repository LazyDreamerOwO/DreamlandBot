import discord
import os
import random
from dotenv import load_dotenv
load_dotenv(".env")

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message}: ({channel})')

    if message.author == client.user:
        return
    
    if message.channel.name == 'bot-test':
        if user_message == 'hello':
            await message.channel.send(f'Hello {username}!')
            return
        elif user_message == 'bye':
            await message.channel.send(f'Goodbye {username}!')
            return

client.run(os.environ.get("DiscordBotToken"))
