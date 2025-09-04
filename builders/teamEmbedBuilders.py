import discord

from misc.datatemplates import TeamData
from misc.config import EMBED_COLOR, set_footer, append_suffix
from query_stuff import builderQueries

class EventTeamEmbed:
    def __init__(self, event_code: str):
        self.event_code = event_code

class TeamEmbed:
    def __init__(self, number: int):
        self.team: TeamData | None = builderQueries.query_team_data(number)

    def create(self) -> discord.Embed | None:
        if self.team is None:
            return None

        title = f"Team {self.team.number} {self.team.name}"

        desc = f"""
Located in {self.team.location.cityStateCountry}
Website: {self.team.website}
"""
        embed: discord.Embed = discord.Embed(title=title, description=desc, color=EMBED_COLOR)

        quickstats = self.team.quickstats

        qstats = f"""
Auto: {quickstats.auto.value}, ranked {append_suffix(quickstats.auto.rank)}
TeleOp: {quickstats.tele.value}, ranked {append_suffix(quickstats.tele.rank)}
Endgame: {quickstats.endgame.value}, ranked {append_suffix(quickstats.endgame.rank)}
Total: {quickstats.total.value}, ranked {append_suffix(quickstats.total.rank)}
        """

        embed.add_field(name='Quickstats', value=qstats)

        set_footer(embed)

        return embed