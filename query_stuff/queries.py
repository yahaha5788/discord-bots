from . import queryUtils
from misc.tupleTemplates import *
from types import SimpleNamespace


def bestTeam(region: str) -> QueryResult:
    query: str = """
{
    tepRecords(region: """+region+""", season: 2024, skip: 0, take: 1, sortDir: Desc, sortBy: "opr") { #gets the best team
        data {
            data {
                team {
                    number
                    name
                    location {
                        city
                        state
                        country
                    }
                    quickStats(season: 2024) {
                        auto {
                            rank
                            value
                        }
                        dc {
                            rank
                            value
                        }
                        eg {
                            rank
                            value
                        }
                        tot {
                            rank
                            value
                        }
                    }
                    events(season: 2024) {
                        event {
                            name
                            type
                            location {
                                venue
                                city
                                state
                                country
                            }
                            start
                            started
                            awards {
                                type
                                teamNumber
                                placement
                            }
                        }
                        stats {
                            ... on TeamEventStats2024 {
                                rank
                                w: wins
                                l: losses
                                t: ties
                            }
                        }
                    }
                }
            }
        }
    }
}
    """

    success, data = queryUtils.parseQuery(query)
    if not success:
        return QueryResult(data, success)

    team: SimpleNamespace = data.data.tepRecords.data[0].data.team #i may kill graphql
    team_info: Team = queryUtils.formatTeamInfo(team)

    autoData: SimpleNamespace = team.qStats.auto
    teleOpData: SimpleNamespace = team.qStats.TeledcOp
    endGameData: SimpleNamespace = team.qStats.eg
    npData: SimpleNamespace = team.qStats.np
    qStats: QuickStats = queryUtils.formatQStats(autoData, teleOpData, endGameData, npData)

    events: list[SimpleNamespace] = team.events #this is a list, not namespace
    team_events: list[Event] = []


    for event in events:
        ev: Event = queryUtils.formatTeamEventData(event, team.number)
        team_events.append(ev)
        
        
    result: BestTeam = BestTeam(team_info, qStats, team_events) #teehee type annotations
    
    return QueryResult(result, success)
    
def teamQuickStats(number) -> QueryResult:
    query: str = """
{
    teamByNumber(number: """+number+""") {
        name
        number
        quickStats(season: 2024) {
            auto {
                rank
                opr: value
            }
            dc {
                rank
                opr: value
            }
            eg {
                rank
                opr: value
            }
            tot {
                rank
                np: value
            }
        }
    }
}
    """
    
    success, data = queryUtils.parseQuery(query)
    if not success:
        return QueryResult(data, success)

    team: SimpleNamespace = data.data.teamByNumber
    name: str = team.name
    number: str = team.number

    qstats: SimpleNamespace = team.quickStats
    auto: SimpleNamespace = qstats.auto
    tele: SimpleNamespace = qstats.dc
    endgame: SimpleNamespace = qstats.eg
    np: SimpleNamespace = qstats.tot

    qStats: QuickStats = queryUtils.formatQStats(auto, tele, endgame, np)

    result: TeamQStats = TeamQStats(name, number, qStats)

    return QueryResult(result, success)

def teamEvents(number) -> QueryResult:
    query: str = """
{
    teamByNumber(number: """+number+""") {
        name
        number
        location {
            city
            state
            country
            venue
        }
        events(season: 2024) {
            event {
                name
                type
                location {
                    loc: venue
                    city
                    state
                    country
                }
                start
                started
                awards {
                    type
                    teamNumber
                    placement
                }
            }
            stats {
                ... on TeamEventStats2024 {
                    rank
                    w: wins
                    l: losses
                    t: ties
                }
            }
        }
    }
}
"""

    success, data = queryUtils.parseQuery(query)
    if not success:
        return QueryResult(data, success)

    team: SimpleNamespace = data.data.teamByNumber

    team_info: Team = queryUtils.formatTeamInfo(team)

    team_events: list[Event] = []

    for event in team.events:
        ev: Event = queryUtils.formatTeamEventData(event, team.number)
        team_events.append(ev)

    result: TeamEvents = TeamEvents(team_info, team_events)

    return QueryResult(result, success)

def teamLogistics(number) -> QueryResult:
    query: str = """
{
    teamByNumber(number: """+number+""") {
        name
        number
        rookieYear
        sponsors
        schoolName
        website
        location {
            country
            state
            city
            venue
        }
    }
}
"""
    success, data = queryUtils.parseQuery(query)
    if not success:
        return data

    team = data.data.teamByNumber
    name: str = team.name
    number: str = team.number

    location: Location = queryUtils.formatLocationData(team.location)

    school_name: str = team.schoolName

    website: str = team.website
    sponsors: list[str] = team.sponsors

    rookie_year = team.rookieYear

    result = TeamLogistics(name, number, location, school_name, rookie_year, website, sponsors)

    return QueryResult(result, success)