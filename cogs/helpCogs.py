import discord
from discord.ext import commands
from discord import ButtonStyle

from misc.config import EMBED_COLOR, CHARACTER_LIMIT, gatherAppCommands, addAppCommand, commandAttrs, CategorizedAppCommand
from misc.templates import formatUsage


class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.commands = [CategorizedAppCommand(command) for command in self.bot.tree.get_commands()]

    async def cog_load(self) -> None:
        self.bot.tree.add_command(addAppCommand(self.bot)(self.help))
        self.bot.tree.add_command(addAppCommand(self.bot)(self.intro))

    async def allHelp(self, interaction: discord.Interaction):
        current_page = discord.Embed(
            title="Help",
            description="List of available commands:",
            color=EMBED_COLOR,
        )

        pages = []
        current_length = 0

        for command in self.commands:
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

        async def previous_page(interact: discord.Interaction):
            nonlocal current_index
            if current_index > 0:
                current_index -= 1
            await interact.message.edit(embed=pages[current_index])
            await interact.response.defer()

        async def next_page(interact: discord.Interaction):
            nonlocal current_index
            if current_index < len(pages) - 1:
                current_index += 1
            await interact.message.edit(embed=pages[current_index])
            await interact.response.defer()

        backButton = discord.ui.Button(label="⬅️", style=ButtonStyle.grey)
        nextButton = discord.ui.Button(label="➡️", style=ButtonStyle.grey)
        backButton.callback = previous_page
        nextButton.callback = next_page

        help_view = discord.ui.View(timeout=30)
        help_view.add_item(backButton)
        help_view.add_item(nextButton)

        await interaction.response.send_message(embed=pages[current_index], view=help_view)

    async def commandHelp(self, interaction: discord.Interaction, command: CategorizedAppCommand):
        title = f"Help: {command.name}"
        help_embed = discord.Embed(title=title, color=EMBED_COLOR)

        help_embed.add_field(name='Category', value=command.category, inline=False)

        help_embed.description = command.description

        name, value = formatUsage(command.usage, command.param_guide)

        help_embed.add_field(name=name, value=value, inline=False)

        await interaction.response.send_message(embed=help_embed)

    async def categoryHelp(self, interaction: discord.Interaction, commands_in_category, category):
        current_page = discord.Embed(
            title=f"Help: {category}",
            description=f"Commands in `{category}`:",
            color=EMBED_COLOR,
        )

        pages: list[discord.Embed] = []
        current_length = 0

        for command in commands_in_category:
            cmd_name = f"`{command.name}`"
            cmd_desc = command.brief or "No description available."
            cmd_usage = command.usage or "Usage not specified."
            field_text = f"{cmd_desc}\n{cmd_usage}\n"

            if current_length + len(cmd_name) + len(field_text) > CHARACTER_LIMIT:
                pages.append(current_page)
                current_page = discord.Embed(title=f"Help: {category}", color=EMBED_COLOR)
                current_length = 0

            current_page.add_field(name=cmd_name, value=field_text, inline=False)
            current_length += len(cmd_name) + len(field_text)

        pages.append(current_page)

        current_index = 0

        async def previous_page(interact: discord.Interaction):
            nonlocal current_index
            if current_index > 0:
                current_index -= 1
            await interact.message.edit(embed=pages[current_index])
            await interact.response.defer()

        async def next_page(interact: discord.Interaction):
            nonlocal current_index
            if current_index < len(pages) - 1:
                current_index += 1
            await interact.message.edit(embed=pages[current_index])
            await interact.response.defer()

        backButton = discord.ui.Button(label="⬅️", style=ButtonStyle.grey)
        nextButton = discord.ui.Button(label="➡️", style=ButtonStyle.grey)
        backButton.callback = previous_page
        nextButton.callback = next_page

        help_view = discord.ui.View(timeout=30)
        help_view.add_item(backButton)
        help_view.add_item(nextButton)

        await interaction.response.send_message(embed=pages[current_index], view=help_view)

    @commandAttrs(
        name='help',
        description='Help command. Shows this command.',
        brief="Help command. Shows this command.",
        usage='/help <keyword>',
        param_guide={
            "<keyword>": "An option key word to filter by command or category."
        },
        category='Help'
    )
    async def help(self, interaction: discord.Interaction, keyword: str = None):
        if keyword:
            commands_to_show, help_type = gatherAppCommands(self.commands, keyword)
            if help_type == 'category':
                await self.categoryHelp(interaction, commands_to_show, keyword)
            elif help_type == 'command':
                await self.commandHelp(interaction, commands_to_show[0])
            else:
                await interaction.response.send_message("That is not a valid command or category name.")
        else:
            await self.allHelp(interaction)

    @commandAttrs(
        name='intro',
        description='Intro command for new users.',
        brief='Introduction command.',
        usage='/intro',
        category='help'
    )
    async def intro(self, interaction: discord.Interaction):
        title = f"Welcome, {interaction.user.display_name}!"
        description = f"Welcome, {interaction.user.display_name}, to team 14988, Royal ⍴-botics!\nTo get started, type `/quickstats 14988`! That's our team's stats for the season. You can type /help for more commands.\n\nWe're excited to have you on the team, and we hope you have a great time!"
        intro_embed = discord.Embed(title=title, description=description, color=EMBED_COLOR)
        await interaction.response.send_message(embed=intro_embed, ephemeral=True)

