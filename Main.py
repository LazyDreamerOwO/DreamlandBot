import discord
import os
import random
from dotenv import load_dotenv
load_dotenv(".env")

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

client.run(os.environ.get("TOKEN"))
