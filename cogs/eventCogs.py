import discord
from discord.ext import commands

from query_stuff import queries
from query_stuff.queries import nameFromNumber


from misc.templates import eventTemplate
from misc.config import EMBED_COLOR, setFooter, commandAttrs, addAppCommand


class EventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self) -> None:
        self.bot.tree.add_command(addAppCommand(self.bot)(self.teamevents))
        # self.bot.tree.add_command(addAppCommand(self.bot)(self.upcomingevents))

    @commandAttrs(
        category="events",
        usage=f"/teamevents <number>",
        brief="Gets all events a team has had or will have.",
        description="Gets all events a team has had or will have, and their stats for events they've played.",
        param_guide={
            '<number>': 'The number of the team to query for.'
        },
        name='teamevents'
    )
    async def teamevents(self, interaction: discord.Interaction, number: int):
        data, success = queries.teamEvents(str(number))
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)
            return
        info, events = data
        title = f"Team {info.number}, {info.name}"

        events_embed = discord.Embed(title=title, color=EMBED_COLOR)

        for event in events:
            name, val = eventTemplate(event)
            events_embed.add_field(name=name, value=val, inline=False)

        setFooter(events_embed)

        await interaction.response.send_message(embed=events_embed)

    @commandAttrs(
        category='events',
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
        self.bot.tree.add_command(addAppCommand(self.bot)(self.qualifiedstates))
        self.bot.tree.add_command(addAppCommand(self.bot)(self.qualifiedworlds))

    @commandAttrs(
        category='qualification',
        description="If a team has qualified for states, will send the team's stats for the event they qualified in.",
        brief='Checks if a team has qualified for states.',
        usage=f'/qualifiedstates <number>',
        param_guide={
            '<number>': 'The number of the team to query for.'
        },
        name='qualifiedstates'
    )
    async def qualifiedstates(self, interaction: discord.Interaction, number: int):
        data, success = queries.qualifiedSTATES(str(number))
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)
            return

        if not data.hasQualified:
            desc = f"Team {data.team.number} {data.team.name} has not qualified for states."
            qual_embed = discord.Embed(title=desc, color=EMBED_COLOR)
            await interaction.response.send_message(embed=qual_embed)
            return

        title = f"Team {data.team.number} {nameFromNumber(data.team.number)} has qualified for states."

        name, val = eventTemplate(data.eventQualified)

        qual_embed = discord.Embed(title=title, color=EMBED_COLOR)
        qual_embed.add_field(name=name, value=val, inline=False)
        setFooter(qual_embed)

        await interaction.response.send_message(embed=qual_embed)

    @commandAttrs(
        category='qualification',
        description="If a team has qualified for worlds, will send the team's stats for the event they qualified in.",
        brief='Checks if a team has qualified for worlds.',
        usage=f'/qualifiedworlds <number>',
        param_guide={
            '<number>': 'The number of the team to query for.'
        },
        name='qualifiedworlds'
    )
    async def qualifiedworlds(self, interaction: discord.Interaction, number: int):
        data, success = queries.qualifiedWORLDS(str(number))
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)
            return

        if not data.hasQualified:
            desc = f"Team {data.team.number} {data.team.name} has not qualified for worlds."
            qual_embed = discord.Embed(title=desc, color=EMBED_COLOR)
            await interaction.response.send_message(embed=qual_embed)
            return

        title = f"Team {data.team.number} {nameFromNumber(data.team.number)} has qualified for worlds."

        name, val = eventTemplate(data.eventQualified)

        qual_embed = discord.Embed(title=title, color=EMBED_COLOR)
        qual_embed.add_field(name=name, value=val, inline=False)
        setFooter(qual_embed)

        await interaction.response.send_message(embed=qual_embed)