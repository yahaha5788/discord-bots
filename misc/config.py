import json
from http.client import responses
from typing import Final, Optional, NoReturn, Any

import discord
from discord import app_commands, ButtonStyle
from discord.ext import commands

# ------------------ FINALS ----------------------#
GOLD: Final[str] = 'BBA53D'
EMBED_COLOR: Final[int] = int(GOLD, 16)

CHOICES: Final[list] = [
    'Yes.',
    'No.',
    'Maybe.',
    'Unlikely.',
    'Likely.',
    'You forgot to reset encoders.',
    'Go code autonomous.',
    'Tell Ty he can solo drive for the next comp.'
]

CHARACTER_LIMIT: Final[int] = 500

ACTIVITY: Final[discord.Activity] = discord.Activity(type=discord.ActivityType.listening, name='to lifts skipping')

STARTING: Final[discord.CustomActivity] = discord.CustomActivity(name="STARTING")

FTC_LOGO: Final[str] =  "../bot/ftc.png"

# ---------------- UTILS -------------------#

def get_code_desc(code: int) -> str:
    desc: str = responses[code]
    return desc

def append_suffix(num: int) -> str:
    number = str(num)
    number = list("".join(number))[len(list("".join(number))) - 1] # muahahaha
    if num < 10 or num > 19: #10 - 19 all end in 'th'
        match number:
            case '1':
                suf = 'st'
            case '2':
                suf = 'nd'
            case '3':
                suf = 'rd'
            case _:
                suf = 'th'
    else: suf = 'th'

    fin = f'{num}{suf}'
    return fin

def set_footer(embed: discord.Embed) -> None:
    """
    Gives links to put at the bottom of an embed. Since links don't work in the footer field of an embed,
    this should be used after all embed fields are added.
    :param embed: The embed to add the links to.
    """
    embed.add_field(name="", value="-# [FTCScout](https://ftcscout.org/) | [API Link](https://api.ftcscout.org/graphql) | [Github Repository](https://github.com/yahaha5788/discord-bots)", inline=False)


# --------------- CATEGORIZED COMMANDS --------------------------#
def commandattrs(name: str, description: str, usage: str, brief: str, category: str, param_guide: Optional[dict[str, str]] = None, param_options: Optional[dict[str, list[dict[str, Any]]]] = None):
    def decorator(cmd):
        cmd.name = name
        cmd.description = description
        cmd.usage = usage
        cmd.brief = brief
        cmd.category = category
        cmd.param_guide = param_guide
        cmd.param_options = param_options

        return cmd
    return decorator

def gather_command_attrs(cmd) -> tuple[str, str, str, str, str, dict[str, str] | None, dict[str, list[dict[str, str]]] | None]:
    name = getattr(cmd, "name")
    description = getattr(cmd, "description")
    category = getattr(cmd, "category")
    usage = getattr(cmd, "usage")
    brief = getattr(cmd, "brief")
    param_guide = getattr(cmd, "param_guide", None)
    param_options = getattr(cmd, "param_options", None)

    return name, description, category, usage, brief, param_guide, param_options

def add_app_command(
    bot: commands.Bot,
):
    def decorator(cmd):
        name, description, category, usage, brief, param_guide, param_options = gather_command_attrs(cmd)

        command = app_commands.command(name=name, description=description)(cmd)

        command.usage = usage
        command.brief = brief
        command.category = category
        command.param_guide = param_guide
        command.param_options = param_options


        # apply descriptions
        if param_guide:
            for param, desc in param_guide.items():
                command = app_commands.describe(**{param.strip("<>"): desc})(command)

        # apply choices
        if param_options:
            for param, options in param_options.items():
                choices = [app_commands.Choice(name=list(n.keys())[0], value=list(n.values())[0]) for n in options]
                command = app_commands.choices(**{param.strip("<>"): choices})(command)

        if bot.guilds:
            for guild in bot.guilds:
                bot.tree.add_command(command, guild=guild)
        else:
            bot.tree.add_command(command)

        return command
    return decorator

class CategorizedAppCommand: # basically just wraps every command when the help function is run
    def __init__(self, command): # TODO: OPTIMIZE- WRAP ALL COMMANDS ON START AND USE INSTEAD OF WRAPPING EVERY TIME /HELP IS RUN
        self.command = command
        self.name, self.description, self.category, self.usage, self.brief, self.param_guide, self.param_options = gather_command_attrs(command)

def gather_app_commands(commands_to_filter: list[CategorizedAppCommand], keyword: str) -> tuple[list[CategorizedAppCommand], str, str | None]:
    result = []

    for command in commands_to_filter:
        if command.category.lower() == keyword.lower():
            result.append(command)

        if command.name.lower() == keyword.lower():
            result.append(command)

            return result, 'command', None

    if not result:
        return result, 'all', None

    return result, 'category', result[0].category

def sort_category_commands(commands_to_sort: list[CategorizedAppCommand]) -> list[CategorizedAppCommand]:
    return sorted(commands_to_sort, key=lambda cmd: cmd.name.lower())

def sort_all_commands(commands_to_sort: list[CategorizedAppCommand]) -> dict[str, list[CategorizedAppCommand]]:
    sorted_commands = sorted(commands_to_sort, key=lambda cmd: cmd.category.lower())

    commands_dict: dict[str, list[CategorizedAppCommand]] = {}

    for command in sorted_commands:
        if command.category not in commands_dict.keys(): #creates list of category commands if it does not exist
            commands_dict[command.category] = []

        commands_dict[command.category].append(command)

    return commands_dict

# --------------------------------------------- PAGES ------------------------------------- #

class MultiPageEmbed:
    def __init__(self, title: str, page_content: list[str]):
        self.title = title
        self.page_content = page_content
        # create embed with title and content for each piece in page_content, for example an embed with one event
        # not used for help command, as that goes off of character limit to determine when more pages are generated
        self.pages: list[discord.Embed] = [discord.Embed(title=title, description=content, color=EMBED_COLOR) for content in page_content]
        for page in self.pages:
            set_footer(page)

        self.current_index = 0


        async def previous_page(interact: discord.Interaction):
            if self.current_index > 0:
                self.current_index -= 1

                await interact.message.edit(embed=self.pages[self.current_index])

            await interact.response.defer()

        async def next_page(interact: discord.Interaction):
            if self.current_index < len(self.pages) - 1:
                self.current_index += 1
                
                await interact.message.edit(embed=self.pages[self.current_index])

            await interact.response.defer()

        backButton = discord.ui.Button(label="⬅️", style=ButtonStyle.grey)
        nextButton = discord.ui.Button(label="➡️", style=ButtonStyle.grey)

        backButton.callback = previous_page
        nextButton.callback = next_page

        self.help_view = discord.ui.View(timeout=30)

        self.help_view.add_item(backButton)
        self.help_view.add_item(nextButton)

    def send(self, interaction: discord.Interaction):
        interaction.response.send_message(embed=self.pages[0], view=self.help_view)

