from typing import NamedTuple



class quickStats(NamedTuple):
    autoData: str
    teleOpData: str
    endGameData: str
    NpData: str

class LocationValues(NamedTuple):
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

class EventData(NamedTuple):
    name: str
    event_type: str
    start: str
    started: bool

    location: LocationValues
    stats: EventStats = None

class TeamInfo(NamedTuple):
    name: str
    number: int
    loc: LocationValues = None

class TeamQStats(NamedTuple):
    name: str
    number: str

    qStats: quickStats

class BestTeam(NamedTuple):
    info: TeamInfo
    stats: quickStats
    events: list[EventData]

    
class QueryResult(NamedTuple):
    result: NamedTuple
    success: bool

class TeamLogistics(NamedTuple):
    name: str
    number: str

    loc: LocationValues

    rookie: str
    website: str = None
    sponsors: list = None

