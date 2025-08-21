import discord
from discord import ButtonStyle, SelectOption

from query_stuff import builderQueries

class EventEmbed:
    def __init__(self, season: int, region: str):
        self.season = season
        self.region = region