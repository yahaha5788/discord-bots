from datetime import datetime, timezone
import discord
from discord.ext import commands
from discord import VoiceChannel

from query_stuff import queries

from misc.config import EMBED_COLOR, FTC_LOGO, commandAttrs, addAppCommand
from misc.templates import EventDates, MajorQualifyingEvent


class CompetitionCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open(FTC_LOGO, 'rb') as logo:
            self.event_logo = logo.read()

    # async def cog_load(self) -> None:
    #     self.bot.tree.add_command(addAppCommand(self.bot)(self.setworlds))
    #     self.bot.tree.add_command(addAppCommand(self.bot)(self.setstates))

    async def createEvent(self, guild: discord.Guild, name: str, day: EventDates, vc: VoiceChannel, links: str) -> discord.ScheduledEvent:
        start_time = datetime(int(day.year), int(day.month), int(day.start_day), 12, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(int(day.year), int(day.month), int(day.end_day), 21, 0, 0)


        event = await guild.create_scheduled_event(
            name=name,
            start_time=start_time,
            end_time=end_time,
            image=self.event_logo,
            channel=vc,
            description=links
        )
        return event

    @commandAttrs(
        category='Competition',
        param_guide={
            "<vc>": 'The voice channel location of the server event. Type "#!" to mention the voice channel just as you would use "#" to mention a normal channel'
        },
        brief="",
        description="",
        usage=f"/setworlds <vc>",
        name='setworlds'
    )
    async def setworlds(self, interaction: discord.Interaction, vc: discord.VoiceChannel):
        data, success = queries.worlds()
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)
            return

        finals, edison, jemison, franklin, ochoa = data

        #FINALS
        finals: MajorQualifyingEvent
        title = f"{finals.name}- {finals.dates.month} / {finals.dates.start_day} / {finals.dates.year} to {finals.dates.month} / {finals.dates.end_day} / {finals.dates.year}"
        



    @commandAttrs(
        category='Competition',
        param_guide={
            "<name>": "The name of the states event.",
            "<vc>": 'The voice channel location of the server event. Type "#!" to mention the voice channel just as you would use "#" to mention a normal channel'
        },
        brief="NOT IMPLEMENTED",
        description="NOT IMPLEMENTED",
        usage=f"/setstates <name> <vc>",
        name='setstates'
    )
    async def setstates(self, interaction: discord.Interaction, name: str, vc: discord.VoiceChannel):
        raise NotImplementedError("no") # TODO: IMPLEMENT
        # data, success = queries.worlds(name)
        # if not success:
        #     embed = discord.Embed(description=data, color=EMBED_COLOR)
        #     await ctx.send(embed=embed)
        #     return
