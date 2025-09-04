from typing import NamedTuple
from types import SimpleNamespace

# -------------------------- NAMEDTUPLE --------------------------------- #
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

class AwardData(NamedTuple):
    placement: int
    team_name: str
    team_number: str
    type: str

class AwardCompilation(NamedTuple):
    awards: list[AwardData]

    def sortByType(self) -> list[AwardData]:
        return sorted(self.awards, key=lambda a: a.type.lower())

    def getTeamAwards(self, number: int) -> list[AwardData]:
        return [award for award in self.awards if award.team_number == number]

class TeamData(NamedTuple):
    name: str
    number: str
    website: str

    location: LocationData
    quickstats: QuickStats

# -------------------------------- FORMATTING -------------------------------- #
def generate_event_data(event) -> list[GenericEventData]:
    """

    :param event:
    :return:
    """
    gen_events: list[GenericEventData] = []
    for ev in event:
        loc: LocationData = _format_location(ev.location)

        gen_events.append(
            GenericEventData(
                ev.name,
                ev.type,
                ev.start,
                ev.end,
                ev.started,
                ev.ongoing,
                len(ev.teams),
                len(ev.matches),
                ev.code,
                loc
            )
        )

    return gen_events

def generate_award_data(award) -> AwardData:
    """

    :param award:
    :return:
    """
    return AwardData(
        award.placement,
        award.team.name,
        award.team.number,
        award.type
    )

def generate_team_data(team) -> TeamData:
    return TeamData(
        team.name,
        team.number,
        team.website,
        _format_location(team.location),
        _format_qstats(team.quickStats)
    )

def _format_location(loc: SimpleNamespace) -> LocationData:
    csc = f"{loc.city}, {loc.state}, {loc.country}."
    if getattr(loc, 'venue', None) is None:
        return LocationData(csc)

    return LocationData(csc, loc.venue)

def _format_qstats(quickstats: SimpleNamespace) -> QuickStats:
    auto_ns = quickstats.auto
    tele_ns = quickstats.tele
    endgame_ns = quickstats.endgame
    total_ns = quickstats.tot

    return QuickStats(
        QuickStat(auto_ns.rank, auto_ns.value),
        QuickStat(tele_ns.rank, tele_ns.value),
        QuickStat(endgame_ns.rank, endgame_ns.value),
        QuickStat(total_ns.rank, total_ns.value)
    ) # the stats are quite quick indeed

def event_status(started: bool, ongoing: bool) -> str:
    if started:
        if ongoing:
            return "This event is ongoing."
        else:
            return "This event has finished."
    else:
        return "This event has not started."

