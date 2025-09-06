import discord
from discord.ext import commands

from builders import teamEmbedBuilders

from util.cmdutils import commandattrs, add_app_command
from util.utils import QueryFailException

class TeamCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    async def cog_load(self) -> None:
        add_app_command(self.bot)(self.team)

    @commandattrs(
        category="Team",
        usage="/team <number>",
        brief="team",
        description="team",
        param_guide={
            "<number>": "The number of the team to search for."
        },
        name="team"
    )
    async def team(self, interaction: discord.Interaction, number: int):
        try:
            embed: discord.Embed = teamEmbedBuilders.TeamEmbed(number).create()

            await interaction.response.send_message(embed=embed)
        except QueryFailException as e:
            await interaction.response.send_message(e)