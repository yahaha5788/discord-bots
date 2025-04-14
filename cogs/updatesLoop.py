import json
import discord
from discord.ext import commands, tasks

from misc.templates import unplayedEventTemplate, UpcomingEvents, OngoingEvents, Event
from query_stuff import queries

from misc.config import COMMAND_PREFIX, EMBED_COLOR, setFooter, checkValidNumber, categorizedCommand

class Updates(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.ticker = 0
        self.monitorCog = None
        self.competitionCog = None

    def retrieveCogs(self):
        self.monitorCog = self.bot.get_cog("MonitorCog")
        self.competitionCog = self.bot.get_cog("CompetitionCog")

    def checkHour(self) -> bool: #i only want monitor updates to run every hour but worlds and states updates run every 5 min
        if self.ticker == 60:
            self.ticker = 0
            return True
        else:
            return False

    @tasks.loop(minutes=5)
    async def updatesAll(self):
        raise NotImplementedError
        # competition loop code
        # check hour
        # if check hour then run monitor loop code
        # check hour += 5