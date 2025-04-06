import discord
from discord.ext import commands

from query_stuff import queries

from misc.config import EMBED_COLOR, COMMAND_PREFIX, setFooter, checkValidNumber, categorizedCommand
from misc.templates import qStatsTemplate, addSponsors


class StatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def stats(self, ctx):
        await ctx.send(f"This is the group of stats commands. Type `{COMMAND_PREFIX}help stats` for more info.")

    @categorizedCommand(
        category='stats',
        aliases=['qstats', 'qs'],
        usage=f"{COMMAND_PREFIX}quickstats <number>",
        brief="Gets the quickstats of a team.",
        description='Gets the quickstats of a given team by their number from ftcscout.org.'
    )
    async def quickstats(self, ctx, number):
        if not checkValidNumber(number):
            await ctx.send("Please enter a valid number.")
            return

        data, success = queries.teamQuickStats(number)
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await ctx.send(embed=embed)
            return
        name, number, qstats = data
        title = f"Team {number}, {name}"

        auto, tele, endgame, np = qstats
        qstats_embed: discord.Embed = discord.Embed(title=title, color=EMBED_COLOR)

        name, val = qStatsTemplate(auto, tele, endgame, np)
        qstats_embed.add_field(name=name, value=val, inline=False)

        setFooter(qstats_embed)

        await ctx.send(embed=qstats_embed)

    @categorizedCommand(
        category='stats',
        aliases=['stat'],
        description='',
        brief="",
        usage=f"{COMMAND_PREFIX}customstat <number> <stat>"
    )
    async def customstat(self, ctx, number, stat):
        raise NotImplementedError() # TODO: IMPLEMENT

    @categorizedCommand(
        category='stats',
        aliases=['betterteam', 'compare'],
        description='',
        brief="",
        usage=f"{COMMAND_PREFIX}compareteams <team_number_1> <team_number_2>"
    )
    async def compareteams(self, ctx, team_number_1, team_number_2):
        raise NotImplementedError() # TODO: IMPLEMENT

    @categorizedCommand(
        category='stats',
        aliases=['recentscores', 'recent'],
        description='',
        brief="",
        usage=f"{COMMAND_PREFIX}recentmatches <number>"
    )
    async def recentmatches(self, ctx, number):
        raise NotImplementedError() # TODO: IMPLEMENT

class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def info(self, ctx):
        await ctx.send(f"This is the group of info commands. Type `{COMMAND_PREFIX}help info` for more info.")

    @categorizedCommand(
        category='info',
        aliases=['ti'],
        usage=f"{COMMAND_PREFIX}teaminfo <number>",
        brief="Gets information on a team",
        description='Gets information on a team, like their rookie year or website link by their number from ftcscout.org'
    )
    async def teaminfo(self, ctx, number):
        if not checkValidNumber(number):
            await ctx.send("Please enter a valid number.")
            return

        data, success = queries.teamLogistics(number)
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await ctx.send(embed=embed)
            return

        title = f"Team {data.number}, {data.name}"

        desc = f"""
    Located in {data.loc.cityStateCountry}
    Rookie Year: {data.rookie}
    School: {data.school}

    Website: {data.website}
    Sponsors:
    """
        desc = addSponsors(data.sponsors, desc)

        info_embed = discord.Embed(title=title, description=desc, color=EMBED_COLOR)
        setFooter(info_embed)

        await ctx.send(embed=info_embed)