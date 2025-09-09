import discord

from util.data.templates import AwardCompilation, GenericAwardData
from util.cfg import AWARD_DESCRIPTIONS

from query_stuff.builderQueries import query_event_awards

class EventAwardsEmbed:
    def __init__(self, event_code: str, season: int):
        self.event_code = event_code
        self.season = season

        self.awards: AwardCompilation = query_event_awards(self.event_code, self.season)



    def create(self):
        pass

class AwardEmbed:
    def __init__(self, award: GenericAwardData):
        self.first = award.first_place_team
        self.second = award.second_place_team
        self.type = award.type
        self.desc = AWARD_DESCRIPTIONS[award.type.lower()] # raises KeyError if the award type isn't in the dict, used to weed out Winner and Finalist awards among some others

    def create(self) -> discord.Embed:
        title = f"{self.type} Award"

        embed = discord.Embed(title=title, description=self.desc)

        embed.add_field(name="Teams", value=f"1st Place: {self.first.number}, {self.first.name}\n2nd Place: {self.second.name}, {self.second.name}")

        return embed
