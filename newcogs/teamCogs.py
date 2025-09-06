import discord
from discord.ext import commands

from builders import eventEmbedBuilders

from misc.cmdutils import commandattrs, add_app_command
from misc.cfg import SEASON_OPTIONS, REGION_OPTIONS, EVENT_OPTIONS
from misc.utils import QueryFailException

class TeamCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot