import discord
from discord.ext import tasks, commands
from misc.config import EMBED_COLOR, COMMAND_PREFIX, categorizedCommand

class CompetitionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @categorizedCommand(
        category="Competition"
    )
    async def setStates(self, ctx, name, ftcscout_url):
