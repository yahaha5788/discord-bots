import discord
from anyio import value

import query_stuff.queries as queries
from discord.ext import commands
import discord.utils
from random import randint, choice
from misc.utilMethods import appendSuffix
from typing import Never

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
activity = discord.Activity(type=discord.ActivityType.listening, name="the sounds of lifts skipping")
bot = commands.Bot(command_prefix="$", intents=intents, activity=activity)

gold = 'BBA53D'
embed_color = int(gold, 16)

choices = [
    'Yes.',
    'No.',
    'Maybe.',
    'Unlikely.',
    'Likely.',
    'You forgot to reset encoders.',
    'Go code autonomous.',
    'Tell Ty he can solo drive for the next comp.'
]


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

def addSponsors(sponsors: list[str], string: str) -> str:
    if not sponsors:
        return string + "None"

    for sponsor in sponsors:
        string = string + f"{sponsor}\n"

    return string

def setFooter(embed: discord.Embed):
    embed.add_field(name="Links", value="[FTCScout](https://ftcscout.org/) | [API Link](https://api.ftcscout.org/graphql) | [Github Repository](https://github.com/yahaha5788/discord-bots)", inline=False)


@bot.command(pass_context=True,
             aliases=['topteam', 'bt'],
             help='Command format: $bestTeam <region>. If <region> is left blank, the default region is All.',
             description='Queries the best team from ftcscout.org with an optional region modifier to search within a given region',
             brief="Gets the best team from ftcscout.org"
             )
async def bestteam(ctx, region='All') -> Never:
    data, success = queries.bestTeam(region)
    if not success:
        embed = discord.Embed(description=data, color=embed_color)
        await ctx.send(embed=embed)
        return
    team_info, team_qstats, team_events = data
    auto, tele, endgame, np = team_qstats
    location = team_info.loc.cityStateCountry
    title = f"Team {team_info.number}, {team_info.name}"
    desc = f"Located in {location}"

    embed = discord.Embed(title=title, description=desc, color=embed_color)

    name, val = qStatsTemplate(auto, tele, endgame, np)
    embed.add_field(name=name, value=val)

    for event in team_events:
        name, val = eventTemplate(event)

        embed.add_field(name=name, value=val)

    setFooter(embed)

    await ctx.send(embed=embed)

@bot.command(pass_context=True,
             aliases=['qstats', 'qs'],
             help="Command format: $quickstats <number>",
             brief="Gets the Quick Stats (Auto, Teleop, Endgame, NP) of a team.",
             description='Gets the Quick Stats (Auto, Teleop, Endgame, NP) of a given team by their number from ftcscout.org.'
             )
async def quickstats(ctx, number) -> Never:
    data, success = queries.teamQuickStats(number)
    if not success:
        embed = discord.Embed(description=data, color=embed_color)
        await ctx.send(embed=embed)
        return
    name, number, qstats = data
    title = f"Team {number}, {name}"

    auto, tele, endgame, np = qstats
    qStats_embed: discord.Embed = discord.Embed(title=title, color=embed_color)

    name, val = qStatsTemplate(auto, tele, endgame, np)
    qStats_embed.add_field(name=name, value=val)

    setFooter(qStats_embed)

    await ctx.send(embed=qStats_embed)

@bot.command(pass_context=True,
             aliases=['events', 'ev'],
             help="Command format: $teamevents <number>",
             brief="Gets all events a team has had or will have, and their stats.",
             description='Gets all events and event stats of given team by their number from ftcscout.org.'
             )
async def teamevents(ctx, number) -> Never:
    data, success = queries.teamEvents(number)
    if not success:
        embed = discord.Embed(description=data, color=embed_color)
        await ctx.send(embed=embed)
        return
    info, events = data
    title = f"Team {info.number}, {info.name}"


    events_embed = discord.Embed(title=title, color=embed_color)

    for event in events:
        name, val = eventTemplate(event)
        events_embed.add_field(name=name, value=value)

    setFooter(events_embed)

    await ctx.send(embed=events_embed)

@bot.command(pass_context=True,
             aliases=['info', 'ti'],
             help="Command format: $teaminfo <number>",
             brief = "Gets information on a team",
             description = 'Gets information on a team, like their rookie year or website link by their number from ftcscout.org'
             )
async def teaminfo(ctx, number) -> Never:
    data, success = queries.teamLogistics(number)
    if not success:
        embed = discord.Embed(description=data, color=embed_color)
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

    info_embed = discord.Embed(title=title, description=desc, color=embed_color)
    setFooter(info_embed)

    await ctx.send(embed=info_embed)

@bot.command(pass_context=True)
async def bestmatch(ctx, region='All'):
    data, success = queries.bestMatch(region)
    if not success:
        embed = discord.Embed(description=data, color=embed_color)
        await ctx.send(embed=embed)
        return


@bot.command(pass_context=True, aliases=['8'])
async def eightball(ctx) -> Never:
    result = choice(choices)
    eightball_embed = discord.Embed(title='The :8ball: says:', description=result, color=embed_color)
    await ctx.send(embed=eightball_embed)

@bot.command(pass_context=True)
async def dice(ctx, sides=6) -> Never:
    roll = randint(0, sides)
    diceembed=discord.Embed(title=":game_die:", description=f"You rolled a **{roll}** on a **{sides}** sided die.", color=embed_color)
    await ctx.send(embed=diceembed)

@bot.command(pass_context=True)
async def flip(ctx):
    result = 'heads' if randint(0, 1) == 1 else "tails"
    coin_embed = discord.Embed(title="Flipped a coin!", description=f"The :coin: landed on {result}.", color=embed_color)
    await ctx.send(embed=coin_embed)
