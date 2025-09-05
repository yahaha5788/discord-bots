import discord

from http.client import responses


def get_code_desc(code: int) -> str:
    """
    Gets the description of an HTTP code.
    :param code: The code to get the description of.
    :return: The description of the code.
    """
    desc: str = responses[code]
    return desc

def append_suffix(num: int) -> str:
    """
    Append the corresponding suffix ("th", "st", "rd", or "nd") to a given number.
    e.g. 45 -> 45th, 3 -> 3rd, 91 -> 91st, 72 -> 72nd.
    :param num: The number to append to.
    :return: The number and its appended suffix.
    """
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

def event_status(started: bool, ongoing: bool) -> str:
    """
    Determines the status of an event.
    :param started: If the event has started.
    :param ongoing: If the event is currently ongoing.
    :return: A string describing the event's current status.
    """
    if started:
        if ongoing:
            return "This event is ongoing."
        else:
            return "This event has finished."
    else:
        return "This event has not started."

class QueryFailException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
