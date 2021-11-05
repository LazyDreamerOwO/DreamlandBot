import random

import discord
from discord.ext import commands

class UserCommands(commands.Cog):
    """Decoupled cog of commands suitable for hot reloading"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Roll a single dice with N sides")
    async def dice(self, ctx, sides: int = 6):
        """Roll single dice with N sides"""
        sides = max(sides, 2)
        await ctx.send(f"`You rolled {random.randint(1, sides)} of {sides}!`")

    @commands.command(description="Say me, how probable is nonsense that i wrote")
    async def info(self, ctx, *args: str):
        """Specifies probability of given event in message"""
        # idea: make that random nonsense would be placed in message if no message is given
        chance = random.choice(range(101))
        msg = " ".join(args)
        if chance == 69:
            await ctx.send(f"`over 9000% chance that {msg}!!!`")
        else:
            await ctx.send(f"`{chance}% chance that {msg}`")

    # todo: make it reply based
    @commands.command(description="Bonk!")
    async def bonk(self, ctx, *args):
        """Bonk!!!"""
        if len(ctx.message.mentions) != 0:
            targets = ", ".join(a.name for a in ctx.message.mentions)
            await ctx.send(f"`{ctx.author.name} bonked {targets}!`")
