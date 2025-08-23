from typing import NamedTuple
from types import SimpleNamespace

# -------------------------- NAMEDTUPLE --------------------------------- #
class LocationData(NamedTuple):
    cityStateCountry: str
    venue: str = None

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
    teamName: str
    teamNumber: str
    type: str

class AwardCompilation(NamedTuple):
    awards: list[AwardData]

    def sortByType(self) -> list[AwardData]:
        return sorted(self.awards, key=lambda a: a.type.lower())

    def getTeamAwards(self, number: int) -> list[AwardData]:
        return [award for award in self.awards if award.teamNumber == number]

# -------------------------------- FORMATTING -------------------------------- #
def generate_event_data(event) -> list[GenericEventData]:
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

def _format_location(loc: SimpleNamespace) -> LocationData:
    csc = f"{loc.city}, {loc.state}, {loc.country}."
    if getattr(loc, 'venue', None) is None:
        return LocationData(csc)

    return LocationData(csc, loc.venue)

def event_status(started: bool, ongoing: bool) -> str:
    if started:
        if ongoing:
            return "This event is ongoing."
        else:
            return "This event has finished."
    else:
        return "This event has not started."

