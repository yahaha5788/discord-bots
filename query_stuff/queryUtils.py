import json
import requests
from types import SimpleNamespace
import requests_cache

from misc.tupleTemplates import quickStats, LocationValues, EventData, EventStats, TeamInfo
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

def formatQStats(auto: SimpleNamespace, teleop: SimpleNamespace, endgame: SimpleNamespace, np: SimpleNamespace) -> quickStats:
    auto = f"{round(auto.opr, 2)} | {appendSuffix(auto.rank)}"

    teleOp = f"{round(teleop.opr, 2)} | {appendSuffix(teleop.rank)}"

    endGame = f"{round(endgame.opr, 2)} | {appendSuffix(endgame.rank)}"

    npData = f"{round(np.np, 2)} | {appendSuffix(np.rank)}"

    return quickStats(auto, teleOp, endGame, npData)

def formatTeamEventData(i: SimpleNamespace) -> EventData:
    event = i.event
    stats = i.stats

    name = event.name
    level = event.type
    time = event.start
    started = event.started

    csc = f"{event.location.city}, {event.location.state}, {event.location.country}."
    loc = LocationValues(csc, event.location.loc)

    if not stats:
        return EventData(name, level, time, started, loc)

    team_event_stats = EventStats(stats.rank, stats.w, stats.l, stats.t)

    return EventData(name, level, time, started, loc, team_event_stats)

def formatEventInfo(event: SimpleNamespace) -> EventData:
    event = event.event
    name = event.name
    level = event.type
    time = event.start

    csc = f"{event.location.city}, {event.location.state}, {event.location.country}."
    loc = LocationValues(csc, event.location.loc)
    return EventData(name, level, time, loc)

def formatTeamInfo(team: SimpleNamespace) -> TeamInfo:
    name = team.name
    number = team.number
    loc = team.location

    csc = f"{loc.city}, {loc.state}, {loc.country}."
    location = LocationValues(csc)

    return TeamInfo(name, number, location)