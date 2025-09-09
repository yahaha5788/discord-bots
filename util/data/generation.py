from types import SimpleNamespace

from util.data.templates import GenericEventData, GenericAwardData, GenericTeamData, LocationData, QuickStats, QuickStat


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

def generate_award_data(award) -> GenericAwardData:
    """

    :param award:
    :return:
    """
    return GenericAwardData(
        award.placement,
        award.team.name,
        award.team.number,
    )

def generate_team_data(team) -> GenericTeamData:
    return GenericTeamData(
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