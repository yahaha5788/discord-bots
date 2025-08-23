import discord
from discord import app_commands
from discord.ext import commands

from builders import eventEmbedBuilders
from query_stuff import queries
from query_stuff.queries import name_from_number

from misc.templates import eventTemplate
from misc.config import EMBED_COLOR, set_footer, commandattrs, add_app_command


class EventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self) -> None:
        add_app_command(self.bot)(self.teamevents)
        add_app_command(self.bot)(self.event)
        # addAppCommand(self.bot)(self.upcomingevents)

    @commandattrs(
        category="Events",
        usage="/event <keyword> <season> <region> <event_type>",
        brief="event",
        description="event",
        param_guide={
            "<keyword>": "A keyword to use in the event search.",
            "<season>": "The season to search in.",
            "<region>": "The region to search in.",
            "<event_type>": "The event type to search for."
        },
        param_options={  # dict hell
            "<season>": [{"Into The Deep": 2024}, {"Centerstage": 2023}, {"Power Play": 2022}, {"Freight Frenzy": 2021},
                         {"Ultimate Goal": 2020}, {"Skystone": 2019}],
            "<event_type>": [{"All": "All"}, {"Qualifier": "Qualifier"}, {"League Meet": "LeagueMeet"}, {"League Tournament": "LeagueTournament"},
                         {"FIRST Championship": "FIRSTChampionship"}, {"Championship": "Championship"},
                         {"Demo Exhibition": "DemoExhibition"}, {"Innovation Challenge": "InnovationChallenge"}, {"Kickoff": "Kickoff"},
                         {"Non-Competition": "NonCompetition"}, {"Off Season": "OffSeason"}, {"Official": "Official"},
                         {"Other": "Other"}, {"Practice": "PracticeDay"}, {"Premier Event": "Premier"}, {"Scrimmage": "Scrimmage"},
                         {"Super Qualifier": "SuperQualifier"}, {"Volunteer Signup": "VolunteerSignup"},
                         {"Workshop": "Workshop"}],
            "<region>": [{"All": "All"}, {"International": "International"}, {"United States": "UnitedStates"}, {"Ohio": "USOH"},
                         {"Australia": "AU"}, {"Brazil": "BR"}, {"Alberta": "CAAB"},
                         {"British Columbia": "CABC"}, {"Ontario": "CAON"}, {"Québec": "CAQC"}, {"China": "CN"}, {"Cyprus": "CY"},
                         {"Germany": "DE"}, {"Egypt": "EG"}, {"Spain": "ES"}, {"France": "FR"}, {"Great Britain": "GB"},
                         {"Israel": "IL"}, {"India": "IN"}, {"Jamaica": "JM"},
                         {"Libya": "LY"}, {"Mexico": "MX"}, {"Netherlands": "NL"}, {"Romania": "RO"}]
        },
        name="event"
    )
    async def event(self, interaction: discord.Interaction, keyword: str, season: int, region: str, event_type: str):
        try:
            event_embeds: discord.Embed | tuple[list[discord.Embed], discord.ui.View] | None = eventEmbedBuilders.EventEmbedBuilder(keyword, season, region, event_type).build()
            if event_embeds is None:
                await interaction.response.send_message("FTCScout did not respond, check your query parameters to ", ephemeral=True)

            elif type(event_embeds) == discord.Embed:
                await interaction.response.send_message(embed=event_embeds)

            else:
                event_embeds: tuple[list[discord.Embed], discord.ui.View]
                embeds: list[discord.Embed] = event_embeds[0]
                view: discord.ui.View = event_embeds[1]
                await interaction.response.send_message(embed=embeds[0], view=view)
        except IndexError:
            await interaction.response.send_message("No events found, check your query parameters.")



    @commandattrs(
        category="Events",
        usage=f"/teamevents <number>",
        brief="Gets all events a team has had or will have.",
        description="Gets all events a team has had or will have, and their stats for events they've played.",
        param_guide={
            '<number>': 'The number of the team to query for.'
        },
        name='teamevents'
    )
    @app_commands.describe(number="The number of the team to query for.")
    async def teamevents(self, interaction: discord.Interaction, number: int):
        data, success = queries.team_events(str(number))
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)
            return
        info, events = data
        title = f"Events for Team {info.number}, {info.name}"

        events_embed = discord.Embed(title=title, color=EMBED_COLOR)

        for event in events:
            name, val = eventTemplate(event)
            events_embed.add_field(name=name, value=val, inline=False)

        set_footer(events_embed)

        await interaction.response.send_message(embed=events_embed)

    @commandattrs(
        category='Events',
        description='Gets any events that a team has not played yet, and shows their location. The command can also be told to create a discord event for each event',
        brief="Gets all the events a team has not played yet.",
        usage=f"/upcomingevents <number> <create_event>",
        param_guide={
            '<number>': 'The number of the team.',
            '<create_event>': 'Enter "Yes" to create events based on the upcoming events of the team.'
        },
        name='upcomingevents'
    )
    async def upcomingevents(self, interaction: discord.Interaction, number: int):
        raise NotImplementedError() # TODO: IMPLEMENT BASICS THEN CODE EVENT CREATION


class QualificationCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self) -> None:
        add_app_command(self.bot)(self.qualifiedstates)
        add_app_command(self.bot)(self.qualifiedworlds)

    @commandattrs(
        category='Qualification',
        description="If a team has qualified for states, will send the team's stats for the event they qualified in.",
        brief='Checks if a team has qualified for states.',
        usage=f'/qualifiedstates <number>',
        param_guide={
            '<number>': 'The number of the team to query for.'
        },
        name='qualifiedstates'
    )
    async def qualifiedstates(self, interaction: discord.Interaction, number: int):
        data, success = queries.qual_states(str(number))
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)
            return

        if not data.hasQualified:
            desc = f"Team {data.team.number} {data.team.name} has not qualified for states."
            qual_embed = discord.Embed(title=desc, color=EMBED_COLOR)
            await interaction.response.send_message(embed=qual_embed)
            return

        title = f"Team {data.team.number} {name_from_number(data.team.number)} has qualified for states."

        name, val = eventTemplate(data.eventQualified)

        qual_embed = discord.Embed(title=title, color=EMBED_COLOR)
        qual_embed.add_field(name=name, value=val, inline=False)

        set_footer(qual_embed)

        await interaction.response.send_message(embed=qual_embed)

    @commandattrs(
        category='Qualification',
        description="If a team has qualified for worlds, will send the team's stats for the event they qualified in.",
        brief='Checks if a team has qualified for worlds.',
        usage=f'/qualifiedworlds <number>',
        param_guide={
            '<number>': 'The number of the team to query for.'
        },
        name='qualifiedworlds'
    )
    async def qualifiedworlds(self, interaction: discord.Interaction, number: int):
        data, success = queries.qual_worlds(str(number))
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)
            return

        if not data.hasQualified:
            desc = f"Team {data.team.number} {data.team.name} has not qualified for worlds."
            qual_embed = discord.Embed(title=desc, color=EMBED_COLOR)
            await interaction.response.send_message(embed=qual_embed)
            return

        title = f"Team {data.team.number} {name_from_number(data.team.number)} has qualified for worlds."

        name, val = eventTemplate(data.eventQualified)

        qual_embed = discord.Embed(title=title, color=EMBED_COLOR)
        qual_embed.add_field(name=name, value=val, inline=False)
        set_footer(qual_embed)

        await interaction.response.send_message(embed=qual_embed)