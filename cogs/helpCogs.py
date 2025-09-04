import discord
from discord.ext import commands
from discord import ButtonStyle, app_commands

from misc.config import EMBED_COLOR, CHARACTER_LIMIT, gather_app_commands, add_app_command, commandattrs, \
    CategorizedAppCommand, sort_category_commands, sort_all_commands, set_footer
from misc.templates import format_usage
from query_stuff import builderQueries


class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.commands = []

    async def cog_load(self) -> None:
        add_app_command(self.bot)(self.help)
        add_app_command(self.bot)(self.intro)
        add_app_command(self.bot)(self.pingscout)

    def wrap_all_commands(self):
        self.commands = [CategorizedAppCommand(command) for command in self.bot.tree.get_commands()]

    async def all_help(self, interaction: discord.Interaction):
        current_page = discord.Embed(
            title="Harold's Commands",
            description="Type `/help <category>` for help on a specific category!\nType `/help <command>` for help on a specific command!\n",
            color=EMBED_COLOR,
        )

        pages = []
        current_length = 0

        cmd_dict = sort_all_commands(self.commands)

        for category, command_list in cmd_dict.items():
            category_commands: str = ''
            for command in command_list:
                cmd_name = f"`{command.name}`"
                cmd_desc = command.brief or "No description available"
                category_commands = category_commands + f"{cmd_name}: {cmd_desc}\n"

            if current_length + len(category) + len(category_commands) > CHARACTER_LIMIT:
                set_footer(current_page)
                pages.append(current_page)
                current_page = discord.Embed(
                    title="Help Menu",
                    description="Type /help <category> for help on a specific category!\nType /help <command> for help on a specific command!\n",
                    color=EMBED_COLOR
                )
                current_length = 0

            current_page.add_field(name=category, value=category_commands, inline=False)
            current_length += len(category) + len(category_commands)

        set_footer(current_page)
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

        await interaction.response.send_message(embed=pages[0], view=help_view)

    async def command_help(self, interaction: discord.Interaction, command: CategorizedAppCommand):
        title = f"/{command.name}"
        help_embed = discord.Embed(title=title, color=EMBED_COLOR)

        help_embed.description = command.description

        name, value = format_usage(command.usage, command.param_guide)

        help_embed.add_field(name=name, value=value, inline=False)

        set_footer(help_embed)

        await interaction.response.send_message(embed=help_embed)

    async def category_help(self, interaction: discord.Interaction, commands_in_category, category):
        current_page = discord.Embed(
            title=f"{category} Commands",
            description=f"Type `/help <command>` for help on a specific command.",
            color=EMBED_COLOR,
        )

        pages: list[discord.Embed] = []
        current_length = 0

        for command in commands_in_category:
            cmd_name = f"/{command.name}"
            cmd_desc = command.brief or "No description available."
            cmd_usage = command.usage or "Usage not specified."
            field_text = f"{cmd_desc}\n{cmd_usage}\n"

            if current_length + len(cmd_name) + len(field_text) > CHARACTER_LIMIT:
                set_footer(current_page)
                pages.append(current_page)
                current_page = discord.Embed(title=f"Help: {category}", color=EMBED_COLOR)
                current_length = 0

            current_page.add_field(name=cmd_name, value=field_text, inline=False)
            current_length += len(cmd_name) + len(field_text)

        set_footer(current_page)
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

    @commandattrs(
        name='help',
        description='Help command. Shows this command.',
        brief="Help command. Shows this command.",
        usage='/help <keyword>',
        param_guide={
            "<keyword>": "An optional key word to filter by command or category."
        },
        category='Help'
    )
    async def help(self, interaction: discord.Interaction, keyword: str = None):
        if keyword:
            commands_to_show, help_type, category = gather_app_commands(self.commands, keyword)
            if help_type == 'category':
                commands_to_show = sort_category_commands(commands_to_show)
                await self.category_help(interaction, commands_to_show, category)
            elif help_type == 'command':
                await self.command_help(interaction, commands_to_show[0])
            else:
                await interaction.response.send_message("That is not a valid command or category name.")
        else:
            await self.all_help(interaction)

    @commandattrs(
        name='intro',
        description='Intro command for new users.',
        brief='Introduction command.',
        usage='/intro',
        category='Help'
    )
    async def intro(self, interaction: discord.Interaction):
        title = f"Welcome, {interaction.user.display_name}!"
        description = f"Welcome, {interaction.user.display_name}, to team 14988, Royal ⍴-botics!\nTo get started, type `/quickstats 14988`! That's our team's stats for the season. You can type /help for more commands.\n\nWe're excited to have you on the team, and we hope you have a great time!"
        intro_embed = discord.Embed(title=title, description=description, color=EMBED_COLOR)
        await interaction.response.send_message(embed=intro_embed, ephemeral=True)

    @commandattrs(
        name='pingscout',
        description='Command to check if FTCScout is online.',
        brief='Command to check if FTCScout is online.',
        usage='/pingscout',
        category='Help'
    )
    async def pingscout(self, interaction: discord.Interaction):
        pinged: bool = builderQueries.ping_query()
        if pinged:
            await interaction.response.send_message("FTCScout is online.")
        else:
            await interaction.response.send_message("FTCScout did not respond.")

