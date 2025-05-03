import discord
from discord.ext import commands

from query_stuff import queries

from misc.config import EMBED_COLOR, setFooter, commandAttrs, addAppCommand
from misc.templates import qStatsTemplate, addSponsors


class StatsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self) -> None:
        addAppCommand(self.bot)(self.quickstats)
        # (addAppCommand(self.bot)(self.customstat)
        # (addAppCommand(self.bot)(self.recentmatches)
        # (addAppCommand(self.bot)(self.compareteams)

    @commandAttrs(
        category='Stats',
        usage=f"/quickstats <number>",
        brief="Gets the quickstats of a team.",
        description='Gets the quickstats of a given team by their number from ftcscout.org.',
        param_guide={
            "<number>": "The number of the team to query for."
        },
        name='quickstats'
    )
    async def quickstats(self, interaction: discord.Interaction, number: int):
        data, success = queries.teamQuickStats(str(number))
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)
            return
        name, number, qstats = data
        title = f"Team {number}, {name}"

        auto, tele, endgame, np = qstats
        qstats_embed: discord.Embed = discord.Embed(title=title, color=EMBED_COLOR)

        name, val = qStatsTemplate(auto, tele, endgame, np)
        qstats_embed.add_field(name=name, value=val, inline=False)

        setFooter(qstats_embed)

        await interaction.response.send_message(embed=qstats_embed)

    @commandAttrs(
        category='Stats',
        description='NOT IMPLEMENTED',
        brief="NOT IMPLEMENTED",
        usage=f"/customstat <number> <stat> <value> <period>",
        param_guide={
            "<number>": "The number of the team to query for.",
            "<stat>": "The specific statistic to query for. Options are: teleop, auto, np, sample, specimen, park",
            "<value>": "The value of statistic to query for. Options are: avg (default), max, min",
            "<period>": "The period of a match to search in. Options are: teleop (default), auto"
        },
        name='customstat'
    )
    async def customstat(self, interaction: discord.Interaction, number: int, stat: str, value: str = 'avg', period: str = 'teleop'):
        raise NotImplementedError() # TODO: IMPLEMENT
        # wow really? i couldn't tell that this needs to be implemented

    @commandAttrs(
        category='Stats',
        description='NOT IMPLEMENTED',
        brief="NOT IMPLEMENTED",
        usage=f"/compareteams <team_number_1> <team_number_2>",
        name='compareteams',
        param_guide={
            "<team_number_1>": "The number of the first team.",
            "<team_number_2>": "The number of the second team."
        }
    )
    async def compareteams(self, interaction: discord.Interaction, team_number_1: int, team_number_2: int):
        raise NotImplementedError() # TODO: IMPLEMENT

    @commandAttrs(
        category='Stats',
        description='NOT IMPLEMENTED',
        brief="NOT IMPLEMENTED",
        usage=f"/recentmatches <number>",
        name='recentmatches',
        param_guide={
            "<number>": "The number of the team to query for."
        }
    )
    async def recentmatches(self, interaction: discord.Interaction, number: int):
        raise NotImplementedError() # TODO: IMPLEMENT

class InfoCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self) -> None:
        addAppCommand(self.bot)(self.teaminfo)

    @commandAttrs(
        category='Info',
        usage=f"/teaminfo <number>",
        brief="Gets information on a team",
        description='Gets information on a team, like their rookie year or website link by their number from ftcscout.org',
        param_guide={
            "<number>": "The number of the team to query for."
        },
        name='teaminfo'
    )
    async def teaminfo(self, interaction: discord.Interaction, number: int):
        data, success = queries.teamLogistics(str(number))
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)
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

        await interaction.response.send_message(embed=info_embed)