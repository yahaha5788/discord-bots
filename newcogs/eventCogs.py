import discord
from discord.ext import commands

from builders import eventEmbedBuilders

from misc.cmdutils import commandattrs, add_app_command
from misc.cfg import SEASON_OPTIONS, REGION_OPTIONS, EVENT_OPTIONS
from misc.utils import QueryFailException


class EventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self) -> None:
        add_app_command(self.bot)(self.event)

    @commandattrs(
        category="Events",
        usage="/event <keyword> <season> <region> <event_type>",
        brief="event",
        description="event",
        param_guide={
            "<keyword>": "A keyword to use in the event search.",
            "<season>": "The season to search in.",
            "<region>": "The region to search in.",
            "<event_type>": "The event type to search for."
        },
        param_options={
            "<season>": SEASON_OPTIONS,
            "<event_type>": EVENT_OPTIONS,
            "<region>": REGION_OPTIONS
        },
        name="event"
    )
    async def event(self, interaction: discord.Interaction, keyword: str, season: int, region: str, event_type: str):
        try:
            message_content: tuple[discord.Embed, discord.ui.View] = eventEmbedBuilders.build_embed(keyword, season, region, event_type)

            embed: discord.Embed = message_content[0]
            view: discord.ui.View = message_content[1]
            await interaction.response.send_message(embed=embed, view=view)
        except QueryFailException as e:
            await interaction.response.send_message(e)