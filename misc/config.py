from http.client import responses
from typing import Final, Optional, Any

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

FTC_LOGO: Final[str] =  "../bot/ftc.png"

AWARD_DESCRIPTIONS: Final[dict[str, str]] = {
    "inspire": "*The team that receives this award is a strong ambassador for FIRST programs and a role model FIRST team. This team is a top contender for many other judged awards and is a gracious competitor.*",
    "think": "*This judged award is given to the team that best reflects the journey the team took as they experienced their season. The content within the portfolio is the key reference for JUDGES to help identify the most deserving team. The team could share or provide additional detailed information that is helpful for the judges. *",
    "connect": "*This judged award is given to the team that connects with their local science, technology, engineering, and math community to learn and adopt new tools through effort and persistence. This team has a team plan and has identified steps to achieve their goals. A portfolio is not required for this award.*",
    "reach": "*This award celebrates a team that has introduced and recruited new people into FIRST. Through their efforts, they have sparked others to embrace the FIRST culture. A portfolio is not required for this award.*",
    "sustain": "*Sustainability and planning are essential for a FIRST team, because they ensure the program’s long-term success. This award celebrates the team that has considered their future team members and has worked to ensure that their team or program will continue to exist long after they have gone on to develop their careers.*",
    "innovate": "*The Innovate Award celebrates a team that thinks imaginatively and has the ingenuity, creativity, and inventiveness to make their designs come to life. This judged award is given to the team that has an innovative and creative ROBOT design solution to any specific COMPONENTS in the FIRST Tech Challenge game.*",
    "control": "*The Control Award celebrates a team that uses sensors and software to increase the robot’s functionality during gameplay. This award is given to the team that demonstrates innovative thinking and solutions to solve game challenges such as autonomous operation, improving mechanical systems with intelligent control, or using sensors to achieve better results.*",
    "design": "*The Design Award celebrates the team that demonstrates an understanding of industrial design principles by striking a balance between form, function, and aesthetics while meeting the needs of this season’s challenge. The design process used should result in a robot which is efficiently designed and effectively addresses the game challenge.*",
    "choice": "*During the competition, the judging panel may meet a team whose unique efforts, performance, or dynamics merit recognition, but does not fit into any of the other award categories. To recognize these unique teams, FIRST offers a Judges’ Choice Award. *"
}

# ---------------- UTILS -------------------#

def get_code_desc(code: int) -> str:
    desc: str = responses[code]
    return desc

def append_suffix(num: int) -> str:
    if num < 10 or num > 19: # 10 - 19 all end in 'th'
        number: list[str] = list(str(num))
        lastchar: str = number[len(number) - 1]
        match lastchar:
            case '1':
                suf = 'st'
            case '2':
                suf = 'nd'
            case '3':
                suf = 'rd'
            case _:
                suf = 'th'
    else: suf = 'th'

    appended = f'{num}{suf}'
    return appended

def set_footer(embed: discord.Embed) -> None:
    """
    Gives links to put at the bottom of an embed. Since links don't work in the footer field of an embed,
    this should be used after all embed fields are added.
    :param embed: The embed to add the links to.
    """
    embed.add_field(name="", value="-# [FTCScout](https://ftcscout.org/) | [API Link](https://api.ftcscout.org/graphql) | [Github Repository](https://github.com/yahaha5788/discord-bots)", inline=False)


# --------------- CATEGORIZED COMMANDS --------------------------#
def commandattrs(name: str, description: str, usage: str, brief: str, category: str, param_guide: Optional[dict[str, str]] = None, param_options: Optional[dict[str, list[dict[str, Any]]]] = None):
    """
    Associates given attributes with an app command. Some, like name and description are used by the app command while others are for the help menu (brief, category, usage)

    :param name: The name of the command
    :param description: A description to give the command
    :param usage: Specifies the way the command should be used
    :param brief: A shorter, condensed description to give the command when seen in the help menu.
    :param category: A category to give that command, shown in help menu and as a keyword for help
    :param param_guide: Descriptions for each parameter. Used in help, and also to give a description to parameters for the app command
    :param param_options: Used to assign predetermined choices to an app command's parameters.
    """
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
    """
    Gathers attributes given by @commandattrs to use in adding the app command

    :param cmd: The command whose attributes to gather
    :return: The command's attributes
    """
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

class CategorizedAppCommand:
    def __init__(self, command):
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
