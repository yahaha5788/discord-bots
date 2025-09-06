from typing import NamedTuple

class LocationData(NamedTuple):
    cityStateCountry: str
    venue: str = None


class QuickStat(NamedTuple):
    rank: int
    value: int

class QuickStats(NamedTuple):
    auto: QuickStat
    tele: QuickStat
    endgame: QuickStat
    total: QuickStat

class GenericEventData(NamedTuple):
    name: str
    event_type: str
    start: str
    end: str

    started: bool
    ongoing: bool

    team_quantity: int
    match_quantity: int

    event_code: str

    location: LocationData

class GenericAwardData(NamedTuple):
    placement: int
    team_name: str
    team_number: str
    type: str

class AwardCompilation(NamedTuple):
    awards: list[GenericAwardData]

    def sortByType(self) -> list[GenericAwardData]:
        return sorted(self.awards, key=lambda a: a.type.lower())

    def getTeamAwards(self, number: int) -> list[GenericAwardData]:
        return [award for award in self.awards if award.team_number == number]

class GenericTeamData(NamedTuple):
    name: str
    number: str
    website: str

    location: LocationData
    quickstats: QuickStats
