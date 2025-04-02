import discord
from discord import ButtonStyle

import query_stuff.queries as queries
from discord.ext import commands
import discord.utils
from random import randint, choice

from misc.tupleTemplates import Alliance, MatchScores, Match
from misc.utilMethods import appendSuffix
from typing import Never, Optional, Final


command_prefix = '$'
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
activity = discord.Activity(type=discord.ActivityType.listening, name="the sounds of lifts skipping")
bot = commands.Bot(command_prefix=command_prefix, intents=intents, activity=activity, help_command=None)

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

CHARACTER_LIMIT: Final[int] = 200


def categorizedCommand(group: str = "Uncategorized", **kwargs): #i think making my own decorator is a sign i'm going down the rabbit hole
    def decorator(command_function):
        global bot
        new_command = bot.command(**kwargs)(command_function)
        new_command.group = group
        return new_command
    return decorator

def awardTemplate(award) -> str:
    return f"{appendSuffix(award.placement)} place {award.type}\n"

def eventTemplate(event) -> tuple[str, str]:
    if not event.stats:
        name = f"**{event.name} on {event.start}, at {event.location.venue} in {event.location.cityStateCountry}**"
        val = f"Type: {event.event_type}\nNo stats for the event."
        return name, val

    name = f"**{event.name} on {event.start}, at {event.location.venue} in {event.location.cityStateCountry}**"
    val = f"""
Type: {event.event_type}
Team's stats for the event:
Rank: {event.stats.event_rank}
Record: {event.stats.w} - {event.stats.l} - {event.stats.t}
Awards:"""

    if not event.stats.awards:
        return name, val + f" None\n"

    val = val + f"\n"
    for award in event.stats.awards:
        val = val + awardTemplate(award)

    return name, val

def qStatsTemplate(auto, teleop, endgame, np) -> tuple[str, str]:
    name = "**Quick Stats:**"
    val = f"""
Auto: {auto}\nTeleOp: {teleop}\nEndgame: {endgame}\nNpTotal: {np}
"""
    return name, val

def matchScoresTemplate(red: Alliance, blue: Alliance) -> str:
    return f"Red Alliance ({red.one} & {red.two}) - {red.scores.totalPoints} ({red.scores.totalPointsNP})\nBlue Alliance ({blue.one} & {blue.two}) - {blue.scores.totalPoints} ({blue.scores.totalPointsNP})"

def autoScores(scores: MatchScores) -> str:
    return f"**{scores.autoPoints}**\n{scores.autoSample}\n{scores.autoSpecimen}\n{scores.autoPark}"

def teleOpScores(scores: MatchScores) -> str:
    return f"**{scores.dcPoints}**\n{scores.dcSample}\n{scores.dcSpecimen}\n{scores.dcPark}"

def penaltyPoints(scores: MatchScores) -> str:
    return f"**{scores.penaltyPointsByOpp}**\n{scores.majorPenalties*15}\n{scores.minorPenalties*5}"

def addMatchScores(match: Match, embed: discord.Embed) -> None:
    red = match.red
    blue = match.blue

    table_values = f"**Total Points (NP)**\n\n**Auto**\nSample Points\nSpecimen Points\nParking Points\n\n**TeleOp**\nSample Points\nSpecimen Points\nParking Points\n\n**Penalties**\nMajors Points\nMinors Points"
    embed.add_field(name="Alliance\nNumber", value=table_values, inline=True)

    red_name = f"Red Alliance\n({red.one.number} & {red.two.number})"
    red_scores = f"{red.scores.totalPoints} ({red.scores.totalPointsNP})\n\n{autoScores(red.scores)}\n\n{teleOpScores(red.scores)}\n\n{penaltyPoints(red.scores)}"

    blue_name = f"Blue Alliance\n({blue.one.number} & {blue.two.number})"
    blue_scores = f"{blue.scores.totalPoints} ({blue.scores.totalPointsNP})\n\n{autoScores(blue.scores)}\n\n{teleOpScores(blue.scores)}\n\n{penaltyPoints(blue.scores)}"

    embed.add_field(name=red_name, value=red_scores, inline=True)
    embed.add_field(name=blue_name, value=blue_scores, inline=True)


def addSponsors(sponsors: list[str], string: str) -> str:
    if not sponsors:
        return string + "None"

    for sponsor in sponsors:
        string = string + f"{sponsor}\n"

    return string

def setFooter(embed: discord.Embed) -> None:
    embed.add_field(name="Links", value="[FTCScout](https://ftcscout.org/) | [API Link](https://api.ftcscout.org/graphql) | [Github Repository](https://github.com/yahaha5788/discord-bots)", inline=False)


@categorizedCommand(
    group='Help',
    aliases=['h'],
    brief='Help command'
)
async def help(ctx, keyword: Optional[str] = None) -> Never:
    """
    :param ctx: The context of the command. This value is automatically passed in when the command is used.

    :param keyword: the keyword to filter by. if the keyword matches a group name, the commands shown will be all the commands in that group.
    If it does not match a group name, the command will search by command name.

    :return: Never
    """
    current_page = discord.Embed(
        title="Help",
        description="List of available commands:",
        color=EMBED_COLOR,
    )

    pages = []
    current_length = 0
    commands_to_show: list = list(bot.commands)

    if keyword:
        commands_to_show = [command for command in bot.commands if getattr(command, 'group', 'Uncategorized') == keyword]
        if not commands_to_show:
            commands_to_show = [command for command in bot.commands if command.name == keyword]
            command_to_show = commands_to_show[0]
            #do all embed stuff here and return instead of doing multipage stuff because there is only one command
            #and this will give all info (not just brief)
    else:
        for command in commands_to_show:
            cmd_name = f"`{command.name}`"
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
        nonlocal current_page, current_index, message
        if current_index > 0:
            current_index -= 1
        await interaction.message.edit(embed=pages[current_index])
        await interaction.response.defer() #yeah this exists pycharm just is stupid ig

    async def next_page(interaction: discord.Interaction):
        nonlocal current_page, current_index, message
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

    message = await ctx.send(embed=pages[current_index], view=help_view)

@categorizedCommand(
    group="Records",
    aliases=['topteam', 'bt'],
    description='Queries the best team from ftcscout.org with an optional region modifier to search within a given region',
    brief="Gets the best team from ftcscout.org",
    usage="$bestteam <region>"
)
async def bestteam(ctx, region='All') -> Never:
    data, success = queries.bestTeam(region)
    if not success:
        embed = discord.Embed(description=data, color=EMBED_COLOR)
        await ctx.send(embed=embed)
        return
    team_info, team_qstats, team_events = data
    auto, tele, endgame, np = team_qstats
    location = team_info.loc.cityStateCountry
    title = f"Team {team_info.number}, {team_info.name}"
    desc = f"Located in {location}"

    embed = discord.Embed(title=title, description=desc, color=EMBED_COLOR)

    name, val = qStatsTemplate(auto, tele, endgame, np)
    embed.add_field(name=name, value=val, inline=False)

    for event in team_events:
        name, val = eventTemplate(event)

        embed.add_field(name=name, value=val, inline=False)

    setFooter(embed)

    await ctx.send(embed=embed)

@categorizedCommand(
    group="Stats",
    aliases=['qstats', 'qs'],
    usage="",
    brief="Gets the Quick Stats (Auto, Teleop, Endgame, NP) of a team.",
    description='Gets the Quick Stats (Auto, Teleop, Endgame, NP) of a given team by their number from ftcscout.org.'
)
async def quickstats(ctx, number) -> Never:
    data, success = queries.teamQuickStats(number)
    if not success:
        embed = discord.Embed(description=data, color=EMBED_COLOR)
        await ctx.send(embed=embed)
        return
    name, number, qstats = data
    title = f"Team {number}, {name}"

    auto, tele, endgame, np = qstats
    qStats_embed: discord.Embed = discord.Embed(title=title, color=EMBED_COLOR)

    name, val = qStatsTemplate(auto, tele, endgame, np)
    qStats_embed.add_field(name=name, value=val, inline=False)

    setFooter(qStats_embed)

    await ctx.send(embed=qStats_embed)

@categorizedCommand(
    group="Stats",
    aliases=['events', 'ev'],
    help="Command format: $teamevents <number>",
    brief="Gets all events a team has had or will have, and their stats.",
    description='Gets all events and event stats of given team by their number from ftcscout.org.'
)
async def teamevents(ctx, number) -> Never:
    data, success = queries.teamEvents(number)
    if not success:
        embed = discord.Embed(description=data, color=EMBED_COLOR)
        await ctx.send(embed=embed)
        return
    info, events = data
    title = f"Team {info.number}, {info.name}"


    events_embed = discord.Embed(title=title, color=EMBED_COLOR)

    for event in events:
        name, val = eventTemplate(event)
        events_embed.add_field(name=name, value=val, inline=False)

    setFooter(events_embed)

    await ctx.send(embed=events_embed)

@categorizedCommand(
    group="Info",
    aliases=['info', 'ti'],
    help="Command format: $teaminfo <number>",
    brief = "Gets information on a team",
    description = 'Gets information on a team, like their rookie year or website link by their number from ftcscout.org'
)
async def teaminfo(ctx, number) -> Never:
    data, success = queries.teamLogistics(number)
    if not success:
        embed = discord.Embed(description=data, color=EMBED_COLOR)
        await ctx.send(embed=embed)
        return

    title = f"Team {data.number}, {data.name}"

    desc = f"""
Located in {data.loc.cityStateCountry}
Rookie Year: {data.rookie}
School: {data.school}

Website: {data.website}
Sponsors:
"""
    desc = addSponsors(data.sponsors, desc)

    info_embed = discord.Embed(title=title, description=desc, color=EMBED_COLOR)
    setFooter(info_embed)

    await ctx.send(embed=info_embed)

@categorizedCommand(
    group='Records',
)
async def bestmatch(ctx, region='All'):
    data, success = queries.bestMatch(region)
    if not success:
        embed = discord.Embed(description=data, color=EMBED_COLOR)
        await ctx.send(embed=embed)
        return

    event, match = data


    title = f"Best match was played at {event.name} on {event.start}\n{event.location.cityStateCountry} ({event.event_type})"
    scores_embed = discord.Embed(title=title, description="═══════════════════════════════", color=EMBED_COLOR)

    addMatchScores(match, scores_embed)

    setFooter(scores_embed)

    await ctx.send(embed=scores_embed)

@categorizedCommand(
    group='Fun',
)
async def eightball(ctx) -> Never:
    result = choice(CHOICES)
    eightball_embed = discord.Embed(title='The :8ball: says:', description=result, color=EMBED_COLOR)
    await ctx.send(embed=eightball_embed)

@categorizedCommand(
    group='Fun'
)
async def dice(ctx, sides=6) -> Never:
    roll = randint(0, sides)
    dice_embed=discord.Embed(title=":game_die:", description=f"You rolled a **{roll}** on a **{sides}** sided die.", color=EMBED_COLOR)
    await ctx.send(embed=dice_embed)

@categorizedCommand(
    group='Fun'
)
async def flip(ctx):
    result = 'heads' if randint(0, 1) == 1 else "tails"
    coin_embed = discord.Embed(title="Flipped a coin!", description=f"The :coin: landed on {result}.", color=EMBED_COLOR)
    await ctx.send(embed=coin_embed)