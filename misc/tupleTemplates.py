from typing import NamedTuple



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

    minorPenalties: int
    majorPenalties: int

    totalPoints: int
    totalPointsNP: int

class Alliance(NamedTuple):
    one: Team
    two: Team
    scores: MatchScores

class Match(NamedTuple):
    red: Alliance
    blue: Alliance

########################## QUERY RESULT CLASSES ########################

class QueryResult(NamedTuple):
    result: NamedTuple
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
