import discord
from discord.ext import commands
from query_stuff import queries
from misc.templates import *
from misc.config import set_footer, EMBED_COLOR, commandattrs, add_app_command


class RecordCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self) -> None:
        add_app_command(self.bot)(self.worldrecord)
        add_app_command(self.bot)(self.bestteam)

    @commandattrs(
        category="Records",
        description='Gets the best team within a optional given region.',
        brief="Gets the best team from ftcscout.org",
        usage=f"/bestteam <region>",
        param_guide={
            "<region>": "An optional argument for the region to search in. Defaults to All."
        },
        name='bestteam'
    )
    async def bestteam(self, interaction: discord.Interaction, region: str ='All'):
        data, success = queries.best_team(region)
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)
            return
        team_info, team_qstats, team_events = data
        auto, tele, endgame, np = team_qstats
        location = team_info.loc.cityStateCountry
        title = f"Team {team_info.number}, {team_info.name}"
        desc = f"Located in {location}"

        embed = discord.Embed(title=title, description=desc, color=EMBED_COLOR)

        name, val = quickstats_template(auto, tele, endgame, np)
        embed.add_field(name=name, value=val, inline=False)

        for event in team_events:
            if event.started:
                name, val = eventTemplate(event)

                embed.add_field(name=name, value=val, inline=False)

        set_footer(embed)

        await interaction.response.send_message(embed=embed)

    @commandattrs(
        category='Records',
        description='Gets the best match within a optional given region.',
        brief="Gets the best match from ftcscout.org.",
        usage=f"/worldrecord <region>",
        param_guide={
            "<region>": "An optional argument for the region to search in. Defaults to All."
        },
        name='worldrecord'
    )
    async def worldrecord(self, interaction: discord.Interaction, region: str ='All'):
        await interaction.response.defer()
        data, success = queries.best_match(region)
        if not success:
            embed = discord.Embed(description=data, color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)
            return

        event, match = data


        title = f"Best match was played at {event.name} on {event.start}\n{event.location.cityStateCountry} ({event.event_type})"
        scores_embed = discord.Embed(title=title, description="═══════════════════════════════", color=EMBED_COLOR)

        add_match_scores(match, scores_embed)

        set_footer(scores_embed)

        await interaction.followup.send(embed=scores_embed)

