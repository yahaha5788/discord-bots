import discord
from discord import ButtonStyle, WebhookMessage

from util.data.templates import GenericEventData
from util.cfg import EMBED_COLOR
from util.utils import set_footer, event_status
from query_stuff import builderQueries

def build_embed(keyword: str, season: int, region: str, event_type: str) -> tuple[discord.Embed, discord.ui.View]:
    """
    Creates an event embed, either multiple embeds if the query results in multiple events, or a single embed if the query returns only one event
    :return: A ``discord.Embed`` and a ``discord.ui.View``
    """
    events: list[GenericEventData] = builderQueries.query_event(keyword, season, region, event_type)

    return MultiEventEmbed(events).create()


class EventEmbed:
    def __init__(self, event: GenericEventData):
        self.event: GenericEventData = event

    def create_embed(self) -> discord.Embed:
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
    def __init__(self, events: list[GenericEventData]):
        self.events: list[GenericEventData] = events

    def create(self) -> tuple[discord.Embed, discord.ui.View]:
        """
        Creates an embed that has a dropdown to select an event from a list.

        :return: a ``tuple`` containing a list of ``discord.Embed`` and a ``discord.ui.View`` containing the dropdown for events.
        """

        pages: list[discord.Embed] = [
            EventEmbed(event).create_embed() for event in self.events
        ]
        page_events: list[GenericEventData] = self.events
        current_index = 0
        current_event = page_events[current_index]
        awards_shown = False
        teams_shown = False
        matches_shown = False
        award_message: WebhookMessage
        team_message: WebhookMessage
        match_message: WebhookMessage

        # ---------------------- BUTTON ---------------------------- #

        async def awards_callback(interaction: discord.Interaction):
            nonlocal current_event, awards_shown, award_message

            await interaction.response.defer()

            if not awards_shown:
                query_awards_button.style = ButtonStyle.grey
                award_message = await interaction.followup.send(f"awards {current_event.name}", wait=True)
            else:
                query_awards_button.style = ButtonStyle.green
                await award_message.delete()

            awards_shown = not awards_shown
            await interaction.response.defer()


        async def teams_callback(interaction: discord.Interaction):
            nonlocal current_event, teams_shown, team_message

            await interaction.response.defer()

            if not teams_shown:
                query_teams_button.style = ButtonStyle.grey
                team_message = await interaction.followup.send(f"teams {current_event.name}", wait=True)
            else:
                query_teams_button.style = ButtonStyle.green
                await team_message.delete()

            teams_shown = not teams_shown
            await interaction.response.defer()


        async def matches_callback(interaction: discord.Interaction):
            nonlocal current_event, matches_shown, match_message

            await interaction.response.defer()

            if not matches_shown:
                query_matches_button.style = ButtonStyle.grey
                match_message = await interaction.followup.send(f"matches {current_event.name}", wait=True)
            else:
                query_matches_button.style = ButtonStyle.green
                await match_message.delete()

            matches_shown = not matches_shown
            await interaction.response.defer()

        query_awards_button = discord.ui.Button(label="Awards", style=ButtonStyle.green)
        query_teams_button = discord.ui.Button(label="Teams", style=ButtonStyle.green)
        query_matches_button = discord.ui.Button(label="Matches", style=ButtonStyle.green)

        query_awards_button.callback = awards_callback
        query_teams_button.callback = teams_callback
        query_matches_button.callback = matches_callback

        # -------------------- SELECT -------------------------------- #

        event_select = discord.ui.Select()
        event_select.placeholder = "Select an event"

        async def select(interaction: discord.Interaction):
            nonlocal current_index, current_event, awards_shown, award_message, teams_shown, team_message, matches_shown, match_message

            current_index = int(event_select.values[0])
            current_event = page_events[current_index]

            await interaction.message.edit(embed=pages[int(event_select.values[0])])

            if awards_shown:
                await award_message.edit(content=f"awards {current_event.name}")
            if teams_shown:
                await team_message.edit(content=f"teams {current_event.name}")
            if matches_shown:
                await match_message.edit(content=f"matches {current_event.name}")

            await interaction.response.defer()

        def shorten_evname(name: str) -> str:
            index = name.find(", at ")
            if index != -1:
                return name[:index]
            else:
                return name

        event_select.callback = select
        event_select.options = [discord.SelectOption(label=shorten_evname(embed.title.strip("**")), value=str(pages.index(embed))) for embed in pages]

        event_view = discord.ui.View(timeout=60)

        event_view.add_item(query_teams_button)
        event_view.add_item(query_awards_button)
        event_view.add_item(query_matches_button)

        event_view.add_item(event_select)

        return pages[0], event_view
