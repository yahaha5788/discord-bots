from datetime import datetime, timezone
import discord
from discord.ext import commands
from discord import VoiceChannel

from query_stuff import queries

from misc.config import EMBED_COLOR, COMMAND_PREFIX, categorizedCommand, FTC_LOGO
from misc.templates import EventDates, MajorQualifyingEvent


class CompetitionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(FTC_LOGO, 'rb') as logo:
            self.event_logo = logo.read()

    async def createEvent(self, guild: discord.Guild, name: str, day: EventDates, vc: VoiceChannel) -> discord.ScheduledEvent:
        start_time = datetime(int(day.year), int(day.month), int(day.start_day), 12, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(int(day.year), int(day.month), int(day.end_day), 21, 0, 0)


        event = await guild.create_scheduled_event(
            name=name,
            start_time=start_time,
            end_time=end_time,
            image=self.event_logo,
            channel=vc
        )
        return event

    @categorizedCommand(
        category='Competition',
        parameters={
            "<vc>": 'The voice channel location of the server event. Type "#!" to mention the voice channel just as you would use "#" to mention a normal channel'
        },
        aliases=["WORLDS"],
        brief="",
        desription="",
        usage=f"{COMMAND_PREFIX}setworlds <vc>"
    )
    async def setworlds(self, ctx, vc: discord.VoiceChannel):
        data, success = queries.worlds()
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await ctx.send(embed=embed)
            return

        finals, edison, jemison, franklin, ochoa = data

        #FINALS
        finals: MajorQualifyingEvent

        title = finals.name
        date_range = f"{finals.dates.month} / {finals.dates.start_day} / {finals.dates.year} to {finals.dates.month} / {finals.dates.end_day} / {finals.dates.year}"



    @categorizedCommand(
        category='Competition',
        parameters={
            "<name>": "The name of the states event.",
            "<vc>": 'The voice channel location of the server event. Type "#!" to mention the voice channel just as you would use "#" to mention a normal channel'
        },
        aliases=["STATES"],
        brief="NOT IMPLEMENTED",
        desription="NOT IMPLEMENTED",
        usage=f"{COMMAND_PREFIX}setstates <name> <vc>"
    )
    async def setstates(self, ctx, name, vc: discord.VoiceChannel):
        raise NotImplementedError("no")
        # data, success = queries.worlds(name)
        # if not success:
        #     embed = discord.Embed(description=data, color=EMBED_COLOR)
        #     await ctx.send(embed=embed)
        #     return
