from typing import Optional, Any

from discord import app_commands
from discord.ext import commands

class CategorizedAppCommand:
    def __init__(self, command):
        self.command = command
        self.name, self.description, self.category, self.usage, self.brief, self.param_guide, self.param_options = gather_command_attrs(command)

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

def gather_app_commands(to_filter: list[CategorizedAppCommand], keyword: str) -> tuple[list[CategorizedAppCommand], str, str | None]:
    result = []

    for command in to_filter:
        if command.category.lower() == keyword.lower():
            result.append(command)

        if command.name.lower() == keyword.lower():
            result.append(command)

            return result, 'command', None

    if not result:
        return result, 'all', None

    return result, 'category', result[0].category

def sort_category_commands(to_sort: list[CategorizedAppCommand]) -> list[CategorizedAppCommand]:
    return sorted(to_sort, key=lambda cmd: cmd.name.lower())

def sort_all_commands(to_sort: list[CategorizedAppCommand]) -> dict[str, list[CategorizedAppCommand]]:
    sorted_commands = sorted(to_sort, key=lambda cmd: cmd.category.lower())

    commands_dict: dict[str, list[CategorizedAppCommand]] = {}

    for command in sorted_commands:
        if command.category not in commands_dict.keys(): #creates list of category commands if it does not exist
            commands_dict[command.category] = []

        commands_dict[command.category].append(command)

    return commands_dict
