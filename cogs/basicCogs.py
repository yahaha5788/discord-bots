from discord.ext import commands
import discord
from random import randint, choice
from misc.config import EMBED_COLOR, CHOICES, COMMAND_PREFIX, categorizedCommand

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def fun(self, ctx):
        await ctx.send(f"This the group of fun commands. Type `{COMMAND_PREFIX}help fun` for more info")

    @categorizedCommand(
        category='fun',
        aliases=['roll'],
        description='Rolls a die with a given number of sides',
        brief="Rolls a die with a given number of sides",
        usage=f"{COMMAND_PREFIX}dice <sides>"
    )
    async def dice(self, ctx, sides=6):
        roll = randint(0, sides)
        dice_embed = discord.Embed(title=":game_die:", description=f"You rolled a **{roll}** on a **{sides}** sided die.", color=EMBED_COLOR)
        await ctx.send(embed=dice_embed)

    @categorizedCommand(
        category='fun',
        aliases=['coin'],
        description='Flips a coin.',
        brief="Flips a coin.",
        usage=f"{COMMAND_PREFIX}flip"
    )
    async def flip(self, ctx):
        result = 'heads' if randint(0, 1) == 1 else "tails"
        coin_embed = discord.Embed(title="Flipped a coin!", description=f"The :coin: landed on {result}.", color=EMBED_COLOR)
        await ctx.send(embed=coin_embed)

    @categorizedCommand(
        category='fun',
        aliases=['eight'],
        description='Rolls an eightball.',
        brief='Rolls an eightball.',
        usage=f"{COMMAND_PREFIX}eightball"
    )
    async def eightball(self, ctx):
        result = choice(CHOICES)
        eightball_embed = discord.Embed(title='The :8ball: says:', description=result, color=EMBED_COLOR)
        await ctx.send(embed=eightball_embed)

    @categorizedCommand(
        category='fun',
        aliases=['questions', 'quiz'],
        description='Play trivia about FIRST.',
        brief="lay trivia about FIRST.",
        usage=f"{COMMAND_PREFIX}trivia <number_of_questions>"
    )
    async def trivia(ctx, number_of_questions=1):
        raise NotImplementedError() # TODO: IMPLEMENT