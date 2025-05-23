from discord.ext import commands
from discord import Interaction
import discord
from random import randint, choice
from misc.config import EMBED_COLOR, CHOICES, commandAttrs, addAppCommand, setFooter


class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self) -> None:
        addAppCommand(self.bot)(self.dice)
        addAppCommand(self.bot)(self.flip)
        addAppCommand(self.bot)(self.eightball)
        addAppCommand(self.bot)(self.trivia)

    @commandAttrs(
        name='dice',
        description='Rolls a die with a given number of sides',
        usage=f"/dice <sides>",
        brief="Rolls a die with a given number of sides",
        category='Fun',
        param_guide={
            '<sides>': "The number of sides on the die."
        }
    )
    async def dice(self, interaction: Interaction, sides: int = 6):
        roll = randint(1, int(sides))
        dice_embed = discord.Embed(title=":game_die:", description=f"You rolled a **{roll}** on a **{sides}** sided die.", color=EMBED_COLOR)
        setFooter(dice_embed)
        await interaction.response.send_message(embed=dice_embed)


    @commandAttrs(
        name='flip',
        category='Fun',
        description='Flips a coin.',
        brief="Flips a coin.",
        usage=f"/flip",
    )
    async def flip(self, interaction: Interaction):
        result = 'heads' if randint(0, 1) == 1 else "tails"
        coin_embed = discord.Embed(title="Flipped a coin!", description=f"The :coin: landed on {result}.", color=EMBED_COLOR)
        setFooter(coin_embed)
        await interaction.response.send_message(embed=coin_embed)

    @commandAttrs(
        name='eightball',
        category='Fun',
        description='Rolls an eightball.',
        brief='Rolls an eightball.',
        usage=f"/eightball"
    )
    async def eightball(self, interaction: Interaction):
        result = choice(CHOICES)
        eightball_embed = discord.Embed(title='The :8ball: says:', description=result, color=EMBED_COLOR)
        setFooter(eightball_embed)
        await interaction.response.send_message(embed=eightball_embed)

    @commandAttrs(
        name='trivia',
        category='Fun',
        description='Play trivia about FIRST.',
        brief="Play trivia about FIRST.",
        usage=f"/trivia <number_of_questions>",
        param_guide={
            '<number_of_questions>': 'The number of questions the bot will ask'
        }
    )
    async def trivia(self, interaction: Interaction, number_of_questions: int = 1):
        # if number_of_questions < 1 or number_of_questions > 10:
        #     await interaction.response.send_message("Please enter a number between 1 and 10.")
        raise NotImplementedError() # TODO: IMPLEMENT