from . import queryUtils
from misc.tupleTemplates import QueryResult, BestTeam, TeamQStats


def getBestTeam(region) -> QueryResult:
    query = """
{
    tepRecords(region: """+region+""", season: 2024, skip: 0, take: 1, sortDir: Desc, sortBy: "opr") {
        data {
            data {
                team {
                    number: number
                    name: name
                    location {
                        city
                        state
                        country
                    }
                    qStats: quickStats(season: 2024) {
                        Auto: auto {
                            rank: rank
                            opr: value
                        }
                        TeleOp: dc {
                            rank: rank
                            opr: value
                        }
                        Endgame: eg {
                            rank: rank
                            opr: value
                        }
                        TotalNP: tot {
                            rank: rank
                            np: value
                        }
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

    team = data.data.tepRecords.data[0].data.team #i may kill graphql
    team_info = queryUtils.formatTeamInfo(team)

    autoData = team.qStats.Auto
    teleOpData = team.qStats.TeleOp
    endGameData = team.qStats.Endgame
    npData = team.qStats.TotalNP
    qStats = queryUtils.formatQStats(autoData, teleOpData, endGameData, npData)

    events = team.events #this is a list, not namespace
    team_events = []
    team_events_dict = {}

    for event in events:
        ev = queryUtils.formatTeamEventData(event)
        team_events.append(ev)
        
        
    bt: BestTeam = BestTeam(team_info, qStats, team_events) #teehee type annotations
    
    return QueryResult(bt, success)
    
def teamQuickStats(number) -> QueryResult:
    query = """
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

    data = data.data.teamByNumber
    name = data.name
    number = data.number

    qstats = data.quickStats
    auto = qstats.auto
    tele = qstats.dc
    endgame = qstats.eg
    np = qstats.tot

    qStats = queryUtils.formatQStats(auto, tele, endgame, np)

    team_quickstats = TeamQStats(name, number, qStats)

    return QueryResult(team_quickstats, success)