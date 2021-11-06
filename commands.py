import random, subprocess

import discord
from discord.ext import commands

termite_help = """```
Termite is a small stack-based programming language
It operates on interpreting input sequence directly without processing it in any way
Basic structural element of every program is token, there's 3 kinds of them:
    . Hexadecimals : Byte, consists of 2 characters, letters are capital, - example: 00, 32, FA, 4D
    . Literals : Any single ASCII compliment character that doesn't correspond to any operator or hex, - example: a b c
    . Operators : Special symbols that change state of stack or cursor, example -  / @ [

Available operators:
    < Output    : Pop value and output it to STDOUT
    . Drop      : Deletes last value from the stack
    @ Duplicate : Clones last value on the stack
    ^ Swap      : Swaps two last values
    ~ Not       : Toggles least significant bit
    = Equal     : Pops two values, pushes 01 if values are equal or 00 if not
    ? Compare   : Pops two values, pushes 10 if last values was bigger, 00 otherwise
    + Add       : Pops two values, pushes result of addition
    - Subtract  : Pops two values, pushes result of subtraction
    * Multiply  : Pops two values, pushes result of multiplication
    / Divide    : Pops two values, pushes result of division
    # Conveyor  : Moves last value into beginning of stack
    ] Seek      : Pops N value, seeks N tokens forward
    [ Rewind    : Pops N value, rewinds N tokens back

Restrictions:
    . Only 1000 characters could be outputted by discord bot
    . Stack limit is 66560
    . Input limit is 66560, but discord will truncate it

Switches:
Usage: /termite A[-d ...] a <
    -d  : Debug mode
    -s  : Turn on stack step printing
    -ns : Turn off stack step printing
    -l  : Experimental -- Capture state of rewind and terminate program if stack is identical each time i.e. leads to infinite recursion
    -h  : Output everything as hex
```"""

def strip_discord_formatting(s: str) -> str:
    result = s.strip()
    if result.startswith("```") and result.endswith("```"):
        l = 0
        for ch in result:
            if ch.isspace():
                break
            l += 1
        result = result[l:-3]
    elif result.startswith("`") and result.endswith("`"):
        result = result[1:-1]
    return result


class TermiteCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def termite(self, ctx, *args: str):
        # todo: ability to satisfy '>'
        code = " ".join(args)
        code = strip_discord_formatting(code)
        args = []
        if code.startswith("A"):
            list_open = code.find("[")
            list_close = code.find("]")
            if list_open != -1 and list_close != -1 and list_open < list_close:
                args = code[list_open+1:list_close].split()
                code = code[list_close+1:]
                code = strip_discord_formatting(code)
            else:
                await ctx.send(f"```diff\ninvalid argument clause```")
                return
        try:
            output = subprocess.run(["termite.exe", *args], timeout=5.0,input=code, capture_output=True, text=True)
            output_msg = str(output.stdout)
            if len(output_msg) > 1000:
                output_msg = output_msg[0:1000] + "<...truncated>"
            if output.returncode == 0:
                if len(output_msg) == 0:
                    await ctx.send(f"```\nno output```")
                else:
                    await ctx.send(f"```\n{output_msg}```")
            elif output.returncode == 1:
                await ctx.send(f"```diff\n{output_msg}```")
            else:
                await ctx.send(f"```diff\n!!! termite crashed, tochka, fix !!!```")
        except subprocess.TimeoutExpired:
            await ctx.send(f"```how dare you create infinite loops```")

    # todo: make it "/termite help" 
    @commands.command(name="termite-help")
    async def termite_help(self, ctx):
        await ctx.send(termite_help)


class PythonCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def eval(self, ctx, *args: str):
        code = " ".join(args)
        try:
            await ctx.send(f"`{eval(code, {}, {})}`")
        except Exception as e:
            await ctx.send(f"`{e}`")


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
        chance = random.randrange(101)
        msg = " ".join(args)
        if "tochka" in msg.lower():
            await ctx.send(f"`i won't answer this`")
        elif ctx.author.name == "OwlMan":
            if chance < 30:
                await ctx.send(f"`-{chance}% chance that {msg}`")
            else:
                chance = max(75, chance + 50)
                await ctx.send(f"`{chance}% chance that {msg}`")
        elif chance == 13:
            await ctx.send(f"`i have no interest in talking about conspiracy theories`")
        elif chance == 99:
            await ctx.send(f"`...you said WHAT???`")
        elif chance == 69:
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

    @commands.command()
    async def when(self, ctx, *args: str):
        answers = [
            "when lobster whistles on top of a mountain",
            "never ever",
            "after the rain on thursday",
            "when lazy will not be lazy",
        ]
        await ctx.send(f"`{random.choice(answers)}`")
