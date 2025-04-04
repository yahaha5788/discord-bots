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
    result: str | NamedTuple
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

#------------------------OTHER-----------------------#

class UpcomingEventCheck(NamedTuple):
    last_events: UpcomingEvents
    current_events: UpcomingEvents

class OngoingEventCheck(NamedTuple):
    last_events: OngoingEvents
    current_event: OngoingEvents