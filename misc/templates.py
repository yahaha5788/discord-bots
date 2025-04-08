from typing import NamedTuple, Union
from misc.config import appendSuffix
import discord

class QuickStats(NamedTuple):
    autoData: str
    teleOpData: str
    endGameData: str
    NpData: str

class Location(NamedTuple):
    cityStateCountry: str
    venue: str = None

class Award(NamedTuple):
    type: str
    placement: int
    teamNumber: int

class EventStats(NamedTuple):
    event_rank: int
    w: int
    l: int
    t: int
    awards: list[Award]

class Event(NamedTuple):
    name: str
    event_type: str
    start: str
    started: bool

    location: Location
    stats: EventStats = None

class Team(NamedTuple):
    name: str
    number: int
    loc: Location = None

class MatchScores(NamedTuple):
    autoPoints: int
    autoSample: int
    autoSpecimen: int
    autoPark: int

    dcPoints: int
    dcSample: int
    dcSpecimen: int
    dcPark: int

    penaltyPointsByOpp: int
    minorPenalties: int
    majorPenalties: int

    totalPoints: int
    totalPointsNP: int

class Alliance(NamedTuple):
    one: Team
    two: Team
    color: str
    scores: MatchScores

class Match(NamedTuple):
    red: Alliance
    blue: Alliance

########################## QUERY RESULT CLASSES ########################

class QueryResult(NamedTuple):
    result: Union[str, NamedTuple]
    success: bool

class BestTeam(NamedTuple):
    info: Team
    stats: QuickStats
    events: list[Event]

class TeamQStats(NamedTuple):
    name: str
    number: str

    qStats: QuickStats

class TeamLogistics(NamedTuple):
    name: str
    number: str

    loc: Location
    school: str

    rookie: str
    website: str = None
    sponsors: list[str] = None

class TeamEvents(NamedTuple):
    info: Team
    events: list[Event]

class BestMatch(NamedTuple):
    event: Event
    match: Match

class UpcomingEvents(NamedTuple):
    team: Team
    events: list[Event]

class OngoingEvents(NamedTuple):
    team: Team
    events: list[Event]

class TeamQualified(NamedTuple):
    team: Team
    hasQualified: bool
    eventQualified: Event = None

#------------------------ TEMPLATES -----------------------------------------#

def awardTemplate(award: Award) -> str:
    return f"{appendSuffix(award.placement)} place {award.type}\n"

def unplayedEventTemplate(event: Event) -> str:
    return f"**{event.name} on {event.start}, at {event.location.venue} in {event.location.cityStateCountry}**\nType: {event.event_type}"

def eventTemplate(event: Event) -> tuple[str, str]:
    if not event.location.venue:
        name = f"**{event.name} on {event.start}, in {event.location.cityStateCountry}**"
    else:
        name = f"**{event.name} on {event.start}, at {event.location.venue} in {event.location.cityStateCountry}**"

    if not event.stats:
        val = f"Type: {event.event_type}\nNo stats for the event."
        return name, val

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

#------------------------------ HELP ----------------------------#
def formatUsage(usage: str, aliases: list[str], parameters: dict[str, str]) -> tuple[str, str]:
    name = "Usage"
    value = f"`{usage}`\nOther names: {[f'`{alias}`' for alias in aliases]}"
    if parameters:
        for parameter, use in parameters.items():
            value = value + f"\n`{parameter}`: {use}"

    return name, value