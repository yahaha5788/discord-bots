import discord

from misc.datatemplates import GenericEventData
from misc.cfg import EMBED_COLOR, E
from misc.utils import set_footer, event_status
from query_stuff import builderQueries

def build_embed(keyword: str, season: int, region: str, event_type: str):
    """
    Creates an event embed, either multiple embeds if the query results in multiple events, or a single embed if the query returns only one event
    :return: A ``discord.Embed`` and a ``discord.ui.View``
    """
    events: list[GenericEventData] | None = builderQueries.query_event(keyword, season, region, event_type)

    if events is None:
        return None

    elif len(events) == 1:
        embed = EventEmbed(events[0]).create()

        return embed

    else:

        return MultiEventEmbed(events).create()


class EventEmbed:
    def __init__(self, event: GenericEventData | None):
        self.event: GenericEventData | None = event

    def create(self) -> discord.Embed | None:
        """
        Creates a ``discord.Embed`` for an event
        :return: a ``discord.Embed`` containing the event details
        """
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

    def create(self) -> E:
        """
        Creates an embed that has a dropdown to select an event from a list.

        :return: a ``tuple`` containing a list of ``discord.Embed`` and a ``discord.ui.View`` containing the dropdown for events.
        """
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

        return pages[0], select_view
