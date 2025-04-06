import discord
from discord.ext import commands

from query_stuff import queries

from misc.templates import eventTemplate
from misc.config import EMBED_COLOR, COMMAND_PREFIX, checkValidNumber, setFooter, categorizedCommand
from query_stuff.queries import nameFromNumber


class EventCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def events(self, ctx):
        await ctx.send(f"This is the group of event commands. Type `{COMMAND_PREFIX}help events` for more info.")

    @categorizedCommand(
        category="events",
        aliases=['ev'],
        usage=f"{COMMAND_PREFIX}teamevents <number>",
        brief="Gets all events a team has had or will have.",
        description="Gets all events a team has had or will have, and their stats for events they've played."
    )
    async def teamevents(self, ctx, number):
        if not checkValidNumber(number):
            await ctx.send("Please enter a valid number.")
            return
        data, success = queries.teamEvents(number)
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await ctx.send(embed=embed)
            return
        info, events = data
        title = f"Team {info.number}, {info.name}"

        events_embed = discord.Embed(title=title, color=EMBED_COLOR)

        for event in events:
            name, val = eventTemplate(event)
            events_embed.add_field(name=name, value=val, inline=False)

        setFooter(events_embed)

        await ctx.send(embed=events_embed)

    @categorizedCommand(
        category='events',
        aliases=['calendar'],
        description='Gets any events that a team has not played yet, and shows their location. The command can also be told to create a discord event for each event',
        brief="Gets all the events a team has not played yet.",
        usage=f"{COMMAND_PREFIX}upcomingevents <number> <create_event>"
    )
    async def upcomingevents(self, ctx, number, create_event):
        raise NotImplementedError() # TODO: IMPLEMENT BASICS THEN CODE EVENT CREATION


class QualificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def qualification(self, ctx):
        await ctx.send(f"This is the group of qualification commands. Type `{COMMAND_PREFIX}help qualification` for more info")

    @categorizedCommand(
        category='qualification',
        aliases=['states', 'qualstates'],
        description='',
        brief='',
        usage=f'{COMMAND_PREFIX}qualifiedforstates <number>'
    )
    async def qualifiedstates(self, ctx, number):
        if not checkValidNumber(number):
            await ctx.send("Please enter a valid number.")
            return

        data, success = queries.qualifiedSTATES(number)
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await ctx.send(embed=embed)
            return

        if not data.hasQualified:
            desc = f"Team {data.team.number} {data.team.name} has not qualified for states."
            qual_embed = discord.Embed(title=desc, color=EMBED_COLOR)
            await ctx.send(embed=qual_embed)
            return

        title = f"Team {data.team.number} {nameFromNumber(data.team.number)} has qualified for states."

        name, val = eventTemplate(data.eventQualified)

        qual_embed = discord.Embed(title=title, color=EMBED_COLOR)
        qual_embed.add_field(name=name, value=val, inline=False)
        setFooter(qual_embed)

        await ctx.send(embed=qual_embed)

    @categorizedCommand(
        category='qualification',
        aliases=['worlds', 'qualworlds'],
        description="Checks if a team has qualified for worlds. If they have, gets the data and the team's stats for the event they qualified in.",
        brief='Checks if a team has qualified for worlds.',
        usage=f'{COMMAND_PREFIX}qualifiedforworlds <number>'
    )
    async def qualifiedforworlds(self, ctx, number):
        if not checkValidNumber(number):
            await ctx.send("Please enter a valid number.")
            return

        data, success = queries.qualifiedWORLDS(number)
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await ctx.send(embed=embed)
            return

        if not data.hasQualified:
            desc = f"Team {data.team.number} {data.team.name} has not qualified for worlds."
            qual_embed = discord.Embed(title=desc, color=EMBED_COLOR)
            await ctx.send(embed=qual_embed)
            return

        title = f"Team {data.team.number} {nameFromNumber(data.team.number)} has qualified for worlds."

        name, val = eventTemplate(data.eventQualified)

        qual_embed = discord.Embed(title=title, color=EMBED_COLOR)
        qual_embed.add_field(name=name, value=val, inline=False)
        setFooter(qual_embed)

        await ctx.send(embed=qual_embed)