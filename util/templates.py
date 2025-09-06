from typing import NamedTuple, Union
from util.config import append_suffix
import discord

# namedtuples go brrr

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

class EventDates(NamedTuple):
    year: str
    month: str #one event shouldn't take an entire year, let alone one month.
    start_day: str
    end_day: str

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

class MajorQualifyingEvent(NamedTuple):
    name: str
    dates: EventDates
    teams: list[Team]
    matches: list[Match]
    started: bool
    ongoing: bool
    finished: bool
    stream: str = None

class WorldsEvent(NamedTuple):
    FinalsDiv: MajorQualifyingEvent
    EdisonDiv: MajorQualifyingEvent
    JemisonDiv: MajorQualifyingEvent
    FranklinDiv: MajorQualifyingEvent
    OchoaDiv: MajorQualifyingEvent


#------------------------ TEMPLATES FOR FORMATTING -----------------------------------------#

def award_template(award: Award) -> str:
    return f"{append_suffix(award.placement)} place {award.type}\n"

def unplayed_event_template(event: Event) -> str:
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
        val = val + award_template(award)

    return name, val

def quickstats_template(auto, teleop, endgame, np) -> tuple[str, str]:
    name = "**Quick Stats:**"
    val = f"""
Auto: {auto}\nTeleOp: {teleop}\nEndgame: {endgame}\nNpTotal: {np}
"""
    return name, val

def match_scores_template(red: Alliance, blue: Alliance) -> str:
    return f"Red Alliance ({red.one} & {red.two}) - {red.scores.totalPoints} ({red.scores.totalPointsNP})\nBlue Alliance ({blue.one} & {blue.two}) - {blue.scores.totalPoints} ({blue.scores.totalPointsNP})"

def auto_scores(scores: MatchScores) -> str:
    return f"**{scores.autoPoints}**\n{scores.autoSample}\n{scores.autoSpecimen}\n{scores.autoPark}"

def dc_scores(scores: MatchScores) -> str: # dc is teleop period
    return f"**{scores.dcPoints}**\n{scores.dcSample}\n{scores.dcSpecimen}\n{scores.dcPark}"

def penalty_points(scores: MatchScores) -> str:
    return f"**{scores.penaltyPointsByOpp}**\n{scores.majorPenalties*15}\n{scores.minorPenalties*5}"

def add_match_scores(match: Match, embed: discord.Embed) -> None:
    red = match.red
    blue = match.blue

    table_values = f"**Total Points (NP)**\n\n**Auto**\nSample Points\nSpecimen Points\nParking Points\n\n**TeleOp**\nSample Points\nSpecimen Points\nParking Points\n\n**Penalties**\nMajors Points\nMinors Points"
    embed.add_field(name="Alliance\nNumber", value=table_values, inline=True)

    red_name = f"Red Alliance\n({red.one.number} & {red.two.number})"
    red_scores = f"{red.scores.totalPoints} ({red.scores.totalPointsNP})\n\n{auto_scores(red.scores)}\n\n{dc_scores(red.scores)}\n\n{penalty_points(red.scores)}"

    blue_name = f"Blue Alliance\n({blue.one.number} & {blue.two.number})"
    blue_scores = f"{blue.scores.totalPoints} ({blue.scores.totalPointsNP})\n\n{auto_scores(blue.scores)}\n\n{dc_scores(blue.scores)}\n\n{penalty_points(blue.scores)}"

    embed.add_field(name=red_name, value=red_scores, inline=True)
    embed.add_field(name=blue_name, value=blue_scores, inline=True)

def add_sponsors(sponsors: list[str], string: str) -> str:
    if not sponsors:
        return string + "None"

    for sponsor in sponsors:
        string = string + f"{sponsor}\n"

    return string

#------------------------------ HELP ----------------------------#
def format_usage(usage: str, parameters: dict[str, str]) -> tuple[str, str]:
    name = "Usage"
    value = f"`{usage}`\n"
    if parameters:
        for parameter, use in parameters.items():
            value = value + f"\n`{parameter}`: {use}"

    return name, value

def event_status(started: bool, ongoing: bool) -> str:
    if started:
        if ongoing:
            return "This event is ongoing."
        else:
            return "This event has finished."
    else:
        return "This event has not started."