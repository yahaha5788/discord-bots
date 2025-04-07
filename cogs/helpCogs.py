import discord
from discord.ext import commands
from discord import ButtonStyle

from misc.config import EMBED_COLOR, CHARACTER_LIMIT, gatherCommands, CategorizedCommand
from misc.templates import formatUsage


class HelpCMD(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        current_page = discord.Embed(
            title="Help",
            description="List of available commands:",
            color=EMBED_COLOR,
        )

        pages = []
        current_length = 0
        commands_to_show = [command for command in self.context.bot.commands if isinstance(command, CategorizedCommand)]

        for command in commands_to_show:
            cmd_name = f"`{command.name}: {command.category}`"
            cmd_desc = command.brief or "No description available"
            field_text = f"{cmd_desc}\n"

            if current_length + len(cmd_name) + len(field_text) > CHARACTER_LIMIT:
                pages.append(current_page)
                current_page = discord.Embed(title="Help Menu", color=EMBED_COLOR)
                current_length = 0

            current_page.add_field(name=cmd_name, value=field_text, inline=False)
            current_length += len(cmd_name) + len(field_text)

        pages.append(current_page)

        current_index = 0

        async def previous_page(interaction: discord.Interaction):
            nonlocal current_index
            if current_index > 0:
                current_index -= 1
            await interaction.message.edit(embed=pages[current_index])
            await interaction.response.defer()

        async def next_page(interaction: discord.Interaction):
            nonlocal current_index
            if current_index < len(pages) - 1:
                current_index += 1
            await interaction.message.edit(embed=pages[current_index])
            await interaction.response.defer()

        backButton = discord.ui.Button(label="⬅️", style=ButtonStyle.grey)
        nextButton = discord.ui.Button(label="➡️", style=ButtonStyle.grey)
        backButton.callback = previous_page
        nextButton.callback = next_page

        help_view = discord.ui.View(timeout=30)
        help_view.add_item(backButton)
        help_view.add_item(nextButton)

        await self.context.send(embed=pages[current_index], view=help_view)

    async def send_command_help(self, command: CategorizedCommand):
        title = f"Help: {command.name}"
        help_embed = discord.Embed(title=title, color=EMBED_COLOR)

        help_embed.add_field(name='Category', value=command.category, inline=False)

        help_embed.description = command.description

        name, value = formatUsage(command.usage, command.aliases, command.parameters)

        help_embed.add_field(name=name, value=value, inline=False)

        await self.context.send(embed=help_embed)

    async def send_group_help(self, category):

        category = str(category)

        current_page = discord.Embed(
            title=f"Help: {category}",
            description=f"Commands in `{category}`:",
            color=EMBED_COLOR,
        )

        pages: list[discord.Embed] = []
        current_length = 0

        commands_to_show = gatherCommands([command for command in self.context.bot.commands if isinstance(command, CategorizedCommand)], category)

        for command in commands_to_show:
            cmd_name = f"`{command.name}`"
            cmd_desc = command.description or "No description available"
            field_text = f"{cmd_desc}\n"

            if current_length + len(cmd_name) + len(field_text) > CHARACTER_LIMIT:
                pages.append(current_page)
                current_page = discord.Embed(title=f"Help: {category}", color=EMBED_COLOR)
                current_length = 0

            current_page.add_field(name=cmd_name, value=field_text, inline=False)
            current_length += len(cmd_name) + len(field_text)

        pages.append(current_page)

        current_index = 0

        async def previous_page(interaction: discord.Interaction):
            nonlocal current_index
            if current_index > 0:
                current_index -= 1
            await interaction.message.edit(embed=pages[current_index])
            await interaction.response.defer()

        async def next_page(interaction: discord.Interaction):
            nonlocal current_index
            if current_index < len(pages) - 1:
                current_index += 1
            await interaction.message.edit(embed=pages[current_index])
            await interaction.response.defer()

        backButton = discord.ui.Button(label="⬅️", style=ButtonStyle.grey)
        nextButton = discord.ui.Button(label="➡️", style=ButtonStyle.grey)
        backButton.callback = previous_page
        nextButton.callback = next_page

        help_view = discord.ui.View(timeout=30)
        help_view.add_item(backButton)
        help_view.add_item(nextButton)

        await self.context.send(embed=pages[current_index], view=help_view)