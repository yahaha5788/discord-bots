import json
import requests
from types import SimpleNamespace

from misc.tupleTemplates import QuickStats, Location, Event, EventStats, Team, Award, MatchScores
from misc.utilMethods import getCodeDesc, appendSuffix

def parseQuery(query):
    response = requests.post(url="https://api.ftcscout.org/graphql", json={"query": query})
    if response.status_code == 200:
        success = True
        j = response.content
        data: SimpleNamespace = json.loads(j, object_hook=lambda d: SimpleNamespace(**d))
        return success, data

    else:
        success = False
        return success, f"Request did not return code 200, instead returned code {response.status_code}: {getCodeDesc(response.status_code)}"

def formatQStats(auto: SimpleNamespace, teleop: SimpleNamespace, endgame: SimpleNamespace, np: SimpleNamespace) -> QuickStats:
    auto = f"{round(auto.value, 2)} | {appendSuffix(auto.rank)}"

    teleOp = f"{round(teleop.value, 2)} | {appendSuffix(teleop.rank)}"

    endGame = f"{round(endgame.value, 2)} | {appendSuffix(endgame.rank)}"

    npData = f"{round(np.value, 2)} | {appendSuffix(np.rank)}"

    return QuickStats(auto, teleOp, endGame, npData)

def formatLocationData(loc: SimpleNamespace) -> Location:
    csc = f"{loc.city}, {loc.state}, {loc.country}."
    if not loc.venue:
        return Location(csc)

    return Location(csc, loc.venue)

def formatTeamEventData(i: SimpleNamespace, number: int) -> Event:
    event: SimpleNamespace = i.event
    stats: SimpleNamespace = i.stats

    name: str = event.name
    level: str = event.type
    time: str = event.start
    started: bool = event.started

    loc: Location = formatLocationData(event.location)

    if not stats:
        return Event(name, level, time, started, loc)

    awards: list[Award] = filterAwards(event.awards, number)

    team_event_stats = EventStats(stats.rank, stats.w, stats.l, stats.t, awards)

    return Event(name, level, time, started, loc, team_event_stats)

def formatEventInfo(event: SimpleNamespace) -> Event:
    name: str = event.name
    level: str = event.type
    time: str = event.start
    started: bool = event.started

    loc: Location = formatLocationData(event.location)

    return Event(name, level, time, started, loc)

def formatTeamInfo(team: SimpleNamespace) -> Team:
    name = team.name
    number = team.number

    loc = formatLocationData(team.location)

    return Team(
        name,
        number,
        loc
    )

def filterAwards(awards: list[Award], number) -> list[Award]:
    return [award for award in awards if award.teamNumber == number]

def formatMatchScores(alliance: SimpleNamespace) -> MatchScores:
    return MatchScores(
        alliance.autoPoints,
        alliance.autoSamplePoints,
        alliance.autoSpecimenPoints,
        alliance.autoParkPoints,
        alliance.dcPoints,
        alliance.dcSamplePoints,
        alliance.dcSpecimenPoints,
        alliance.dcParkPoints,
        alliance.penaltyPointsByOpp,
        alliance.minorsByOpp,
        alliance.majorsByOpp,
        alliance.totalPoints,
        alliance.totalPointsNp
    )