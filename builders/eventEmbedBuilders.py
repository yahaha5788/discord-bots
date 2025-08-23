import discord
from discord import ButtonStyle, SelectOption

from misc.utils import GenericEventData, event_status
from misc.config import EMBED_COLOR, set_footer
from query_stuff import builderQueries

class EventEmbedBuilder:
    def __init__(self, keyword: str, season: int, region: str, event_type: str):
        self.keyword = keyword
        self.season = season
        self.region = region
        self.event_type = event_type

        self.events: list[GenericEventData] | None = builderQueries.query_event(self.keyword, self.season, self.region, self.event_type)

    def build(self) -> discord.Embed | tuple[list[discord.Embed], discord.ui.View] | None: # type hint go brrr
        if self.events is None:
            return None

        elif len(self.events) == 1:
            embed = EventEmbed(self.events[0]).create()

            return embed

        else:

            return MultiEventEmbed(self.events).create()

class EventEmbed:
    def __init__(self, event: GenericEventData | None):
        self.event: GenericEventData | None = event

    def create(self) -> discord.Embed | None:
        if self.event is None:
            return None

        title = f"**{self.event.name}, at {self.event.location.venue} in {self.event.location.cityStateCountry}**"

        desc = f"""
From {self.event.start} to {self.event.end}
{event_status(self.event.started, self.event.ongoing)}
This event has {self.event.team_quantity} teams, and {self.event.match_quantity} matches.
"""
        embed = discord.Embed(title=title, description=desc, color=EMBED_COLOR)
        set_footer(embed)

        return embed

class MultiEventEmbed:
    def __init__(self, events: list[GenericEventData] | None):
        self.events: list[GenericEventData] | None = events

    def create(self) -> tuple[list[discord.Embed], discord.ui.View] | None:
        if self.events is None:
            return None

        pages: list[discord.Embed] = [
            EventEmbed(event).create() for event in self.events
        ]

        event_select = discord.ui.Select()
        event_select.placeholder = "Select an event"
        async def select(interaction: discord.Interaction):
            await interaction.message.edit(embed=pages[int(event_select.values[0])])
            await interaction.response.defer()

        def shorten_evname(name: str) -> str:
            index = name.find(", at ")
            if index != -1:
                return name[:index]
            else:
                return name

        event_select.callback = select
        event_select.options = [discord.SelectOption(label=shorten_evname(embed.title.strip("**")), value=str(pages.index(embed))) for embed in pages]

        select_view = discord.ui.View(timeout=60)
        select_view.add_item(event_select)

        return pages, select_view
