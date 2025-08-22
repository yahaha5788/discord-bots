import discord
from discord import ButtonStyle, SelectOption

from misc.utils import GenericEventData, event_status
from misc.config import EMBED_COLOR, set_footer
from query_stuff import builderQueries

import matchEmbedBuilders, teamEmbedBuilders, awardEmbedBuilders

class EventEmbed:
    def __init__(self, keyword: str, season: int, region: str, event_type: str):
        self.keyword = keyword
        self.season = season
        self.region = region
        self.event_type = event_type

        self.event: GenericEventData | None = builderQueries.query_event(self.keyword, self.season, self.region, self.event_type)

    def create(self) -> discord.Embed | None:
        if self.event is None:
            return None

        title = f"**{self.event.name}, at {self.event.location.venue} in {self.event.location.cityStateCountry}**"

        desc = f"""
From {self.event.start} to {self.event.end}
{event_status(self.event.started, self.event.ongoing)}
This event has {self.event.team_quantity} teams, and {self.event.match_quantity} matches.tc
"""
        embed = discord.Embed(title=title, description=desc, color=EMBED_COLOR)
        set_footer(embed)

        return embed

