import discord
from discord import ButtonStyle, SelectOption

from misc.utils import GenericEventData, event_status, AwardCompilation, AwardData
from misc.config import EMBED_COLOR, set_footer, AWARD_DESCRIPTIONS
from query_stuff.builderQueries import query_event_awards

class EventAwardsEmbed:
    def __init__(self, event_code: str, season: int):
        self.event_code = event_code
        self.season = season

        self.awards: AwardCompilation | None = query_event_awards(self.event_code, self.season)

    def create(self):


class AwardEmbed:
    def __init__(self, award: AwardData):
        self.name = award.teamName
        self.number = award.teamNumber
        self.placement = award.placement
        self.type = award.type
        self.desc = AWARD_DESCRIPTIONS[award.type] # raises  if the award type isn't in the dict, used to weed out Winner and Finalist awards among some others

    def create(self) -> discord.Embed:
        