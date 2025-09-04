from typing import Optional

from discord.ext import commands
from discord import Interaction
import discord
from random import randint, choice
from misc.config import EMBED_COLOR, CHOICES, commandattrs, add_app_command, set_footer


class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self) -> None:
        add_app_command(self.bot)(self.dice)
        add_app_command(self.bot)(self.flip)
        add_app_command(self.bot)(self.eightball)

    @commandattrs(
        name='dice',
        description='Rolls a die with a given number of sides',
        usage="/dice <sides>",
        brief="Rolls a die with a given number of sides",
        category='Fun',
        param_guide={
            '<sides>': "The number of sides on the die."
        }
    )
    async def dice(self, interaction: Interaction, sides: Optional[int] = 6):
        roll = randint(1, int(sides))
        dice_embed = discord.Embed(title=":game_die:", description=f"You rolled a **{roll}** on a **{sides}** sided die.", color=EMBED_COLOR)
        set_footer(dice_embed)
        await interaction.response.send_message(embed=dice_embed)


    @commandattrs(
        name='flip',
        category='Fun',
        description='Flips a coin.',
        brief="Flips a coin.",
        usage="/flip",
    )
    async def flip(self, interaction: Interaction):
        result = 'heads' if randint(0, 1) == 1 else "tails"
        coin_embed = discord.Embed(title="Flipped a coin!", description=f"The :coin: landed on {result}.", color=EMBED_COLOR)
        set_footer(coin_embed)
        await interaction.response.send_message(embed=coin_embed)

    @commandattrs(
        name='eightball',
        category='Fun',
        description='Rolls an eightball.',
        brief='Rolls an eightball.',
        usage="/eightball"
    )
    async def eightball(self, interaction: Interaction):
        result = choice(CHOICES)
        eightball_embed = discord.Embed(title='The :8ball: says:', description=result, color=EMBED_COLOR)
        set_footer(eightball_embed)
        await interaction.response.send_message(embed=eightball_embed)