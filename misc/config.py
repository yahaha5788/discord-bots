from http.client import responses

import discord
from typing import Final, Optional

from discord.ext import commands


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

def checkValidNumber(number) -> bool:
    try:
        int(number)
        return True
    except ValueError:
        return False

class CategorizedCommand(commands.Command):
    def __init__(self, func, category: str, parameters: Optional[dict[str, str]] = None, **kwargs):
        super().__init__(func, **kwargs)
        self.category = category
        self.parameters = parameters

def categorizedCommand(category: str, parameters: Optional[dict[str, str]] = None, **kwargs): #i think making my own decorator is a sign i'm going down the rabbit hole
    def decorator(command_function):
        return CategorizedCommand(command_function, category=category, parameters=parameters,**kwargs)
    return decorator

def gatherCommands(commands_to_sort: list[CategorizedCommand], category: str) -> list[CategorizedCommand]:
    result = []
    for command in commands_to_sort:
        if command.category == category:
            result.append(command)

    return result


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

COMMAND_PREFIX: Final[str] = '$'

ACTIVITY: Final[discord.Activity] = discord.Activity(type=discord.ActivityType.listening, name="lifts skipping")

STARTING: Final[discord.CustomActivity] = discord.CustomActivity(name="STARTING")