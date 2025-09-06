import discord
from discord.ext import commands
from discord import app_commands

from typing import Optional

from query_stuff import queries

from util.config import EMBED_COLOR, set_footer, commandattrs, add_app_command
from util.templates import quickstats_template, add_sponsors


class StatsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self) -> None:
        add_app_command(self.bot)(self.quickstats)
        # (addAppCommand(self.bot)(self.customstat)
        # (addAppCommand(self.bot)(self.recentmatches)
        # (addAppCommand(self.bot)(self.compareteams)

    @commandattrs(
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
        data, success = queries.team_quickstats(str(number))
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)
            return
        name, number, qstats = data
        title = f"Team {number}, {name}"

        auto, tele, endgame, np = qstats
        qstats_embed: discord.Embed = discord.Embed(title=title, color=EMBED_COLOR)

        name, val = quickstats_template(auto, tele, endgame, np)
        qstats_embed.add_field(name=name, value=val, inline=False)

        set_footer(qstats_embed)

        await interaction.response.send_message(embed=qstats_embed)

    @commandattrs(
        category='Stats',
        description='Gets a specific statistic for a team',
        brief="Gets a specific statistic for a team",
        usage="/stat <number> <stat> <value> <period>",
        param_guide={
            "<number>": "The number of the team to query for.",
            "<stat>": "The specific statistic to query for.",
            "<value>": "The value of the statistic.",
            "<period>": "The period of a match to search in."
        },
        param_options={
            "<stat>": [{"Sample": "sample"}, {"Specimen": "spec"}, {"Park / Hang": "park"}],
            "<value>": [{"Average": "avg"}, {"Maximum": "max"}, {"Minimum": "min"}],
            "<period>": [{"TeleOp": "dc"}, {"Autonomous": "auto"}],
        },
        name='stat'
    )
    async def stat(self, interaction: discord.Interaction, number: int, stat: app_commands.Choice[str], value: app_commands.Choice[str], period: app_commands.Choice[str]):
        await interaction.response.send_message("This command pulls from the alliance score as it is not possible to see the single team's score.")
        raise NotImplementedError() # TODO: IMPLEMENT
        # wow really? i couldn't tell that this needs to be implemented

    @commandattrs(
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

    @commandattrs(
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
        add_app_command(self.bot)(self.teaminfo)

    @commandattrs(
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
        data, success = queries.team_logistics(str(number))
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
        desc = add_sponsors(data.sponsors, desc)

        info_embed = discord.Embed(title=title, description=desc, color=EMBED_COLOR)
        set_footer(info_embed)

        await interaction.response.send_message(embed=info_embed)