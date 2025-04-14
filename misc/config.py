import json
from http.client import responses
from typing import Final, Optional

import discord
from discord import app_commands
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

FTC_LOGO: Final[str] =  "../bots/ftc.png"

with open('../bots/guilds.json', 'r') as guilds_json:
    guilds: dict[str, int] = json.load(guilds_json)
    command_guilds: list[discord.Object] = []
    for guild in guilds.values():
        command_guilds.append(discord.Object(id=guild))

    VALID_GUILDS: Final[list[discord.Object]] = command_guilds

# ---------------- UTILS -------------------#

def getCodeDesc(code: int) -> str:
    desc: str = responses[code]
    return desc

def appendSuffix(num: int) -> str:
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

def setFooter(embed: discord.Embed) -> None:
    embed.add_field(name="Links", value="[FTCScout](https://ftcscout.org/) | [API Link](https://api.ftcscout.org/graphql) | [Github Repository](https://github.com/yahaha5788/discord-bots)", inline=False)


# --------------- CATEGORIZED COMMANDS --------------------------#
def commandAttrs(name: str, description: str, usage: str, brief: str, category: str, param_guide: Optional[dict[str, str]] = None):
    def decorator(cmd):
        cmd.name = name
        cmd.description = description
        cmd.usage = usage
        cmd.brief = brief
        cmd.category = category
        cmd.param_guide = param_guide

        return cmd
    return decorator

def gatherCommandAttrs(cmd) -> tuple[str, str, str, str, str, dict[str, str] | None]:
    name = getattr(cmd, "name")
    description = getattr(cmd, "description")
    category = getattr(cmd, "category")
    usage = getattr(cmd, "usage")
    brief = getattr(cmd, "brief")
    param_guide = getattr(cmd, "param_guide", None)

    return name, description, category, usage, brief, param_guide

def addAppCommand(
    bot: commands.Bot,
):
    def decorator(cmd):
        name, description, category, usage, brief, param_guide = gatherCommandAttrs(cmd)

        command = app_commands.command(name=name, description=description)(cmd)

        command.usage = usage
        command.brief = brief
        command.category = category
        command.param_guide = param_guide

        if VALID_GUILDS:
            for guild in VALID_GUILDS:
                bot.tree.add_command(command, guild=guild)
        else:
            bot.tree.add_command(command)

        return command
    return decorator

class CategorizedAppCommand: # basically just wraps every command when the help function is run
    def __init__(self, command): # TODO: OPTIMIZE- WRAP ALL COMMANDS ON START AND USE INSTEAD OF WRAPPING EVERY TIME /HELP IS RUN
        self.command = command
        self.name, self.description, self.category, self.usage, self.brief, self.param_guide = gatherCommandAttrs(command)

def gatherAppCommands(commands_to_filter: list[CategorizedAppCommand], keyword: str) -> tuple[list[CategorizedAppCommand], str, Optional[str]]:
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

def sortCategoryCommands(commands_to_sort: list[CategorizedAppCommand]) -> list[CategorizedAppCommand]:
    return sorted(commands_to_sort, key=lambda cmd: cmd.name.lower())

def sortAllCommands(commands_to_sort: list[CategorizedAppCommand]) -> dict[str, list[CategorizedAppCommand]]:
    sorted_commands = sorted(commands_to_sort, key=lambda cmd: cmd.category.lower())
    commands_dict: dict[str, list[CategorizedAppCommand]] = {}
    for command in sorted_commands:
        if command.category not in commands_dict.keys(): #creates list of category commands if it does not exist
            commands_dict[command.category] = []

        commands_dict[command.category].append(command)

    return commands_dict

