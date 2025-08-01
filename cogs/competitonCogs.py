from datetime import datetime, timezone
from typing import Optional

import discord
from discord.ext import commands
from discord import VoiceChannel

from query_stuff import queries

from misc.config import EMBED_COLOR, FTC_LOGO, commandattrs, add_app_command
from misc.templates import EventDates, MajorQualifyingEvent, event_status


class CompetitionCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open(FTC_LOGO, 'rb') as logo:
            self.event_logo = logo.read()

    async def cog_load(self) -> None:
        add_app_command(self.bot)(self.worlds)

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

    @commandattrs(
        category='Competition',
        brief="testing",
        description="testing",
        usage=f"/worlds",
        name='worlds'
    )
    async def worlds(self, interaction: discord.Interaction, divison: Optional[str] = None):
        data, success = queries.worlds()
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)
            return

        finals, edison, jemison, franklin, ochoa = data

        if divison is None:
            finals: MajorQualifyingEvent
            finals_title = f"{finals.name}- {finals.dates.month} / {finals.dates.start_day} / {finals.dates.year} to {finals.dates.month} / {finals.dates.end_day} / {finals.dates.year}"
            finals_name = f"{event_status(finals.started, finals.ongoing)}"
            finals_value = f"There are {len(finals.teams)} teams in this event."
            finals_embed = discord.Embed(title=finals_title, color=EMBED_COLOR)
            finals_embed.add_field(name=finals_name, value=finals_value)
            await interaction.response.send_message(embed=finals_embed)
        else:
            match divison.lower():
                case 'edison':
                    edison: MajorQualifyingEvent
                    edison_teams = ''
                    for team in edison.teams:
                        name = team.name # save space
                        number = team.number
                        edison_teams += f"{number}\n"

                    edison_embed = discord.Embed(title=f"Edison Division", description=edison_teams)

                    await interaction.response.send_message(embed=edison_embed)

                case 'ochoa':
                    ochoa: MajorQualifyingEvent
                    ochoa_teams = ''
                    for team in ochoa.teams:
                        name = team.name
                        number = team.number
                        ochoa_teams += f"{number}\n"

                    ochoa_embed = discord.Embed(title="Edison Division", description=ochoa_teams)

                    await interaction.response.send_message(embed=ochoa_embed)

                case 'jemison':
                    jemison: MajorQualifyingEvent
                    jemison_teams = ''
                    for team in jemison.teams:
                        name = team.name
                        number = team.number
                        jemison_teams += f"{number}\n"

                    jemison_embed = discord.Embed(title="Edison Division", description=jemison_teams)

                    await interaction.response.send_message(embed=jemison_embed)

                case 'franklin':
                    franklin: MajorQualifyingEvent
                    franklin_teams = ''
                    for team in franklin.teams:
                        name = team.name
                        number = team.number
                        franklin_teams += f"{number}\n"

                    franklin_embed = discord.Embed(title="Edison Division", description=franklin_teams)

                    await interaction.response.send_message(embed=franklin_embed)

    @commandattrs(
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
