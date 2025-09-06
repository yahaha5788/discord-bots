from query_stuff import queryUtils
from util.templates import *
from types import SimpleNamespace

#from .queryUtils import formatEventInfo, formatTeamEventData


def name_from_number(number) -> str:
    query: str = """
{
    teamByNumber(number: """+str(number)+""") {
        name
    }
}
"""
    success, data = queryUtils.parseQuery(query)
    if not success:
        return ''

    return data.data.teamByNumber.name

def best_team(region: str) -> QueryResult:
    query: str = """
{
    tepRecords(region: """+region+""", season: 2024, skip: 0, take: 1, sortDir: Desc, sortBy: "opr") { #gets the best team
        data {
            data {
                team {
                    number
                    name
                    location {
                        venue
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

    autoData: SimpleNamespace = team.quickStats.auto
    teleOpData: SimpleNamespace = team.quickStats.dc
    endGameData: SimpleNamespace = team.quickStats.eg
    npData: SimpleNamespace = team.quickStats.tot
    qStats: QuickStats = queryUtils.formatQStats(autoData, teleOpData, endGameData, npData)

    events: list[SimpleNamespace] = team.events #this is a list, not namespace
    team_events: list[Event] = []


    for event in events:
        ev: Event = queryUtils.formatTeamEventData(event, team.number)
        team_events.append(ev)
        
        
    result: BestTeam = BestTeam(team_info, qStats, team_events) #teehee type annotations
    
    return QueryResult(result, success)
    
def team_quickstats(number) -> QueryResult:
    query: str = """
{
    teamByNumber(number: """+number+""") {
        name
        number
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

def team_events(number) -> QueryResult:
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

def team_logistics(number) -> QueryResult:
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

def best_match(region) -> QueryResult:
    query: str = """
{
    matchRecords(season: 2024, region: """+region+""", skip: 0, take: 1, sortDir: Desc) {
        data {
            data {
                match {
                    teams {
                        number: teamNumber
                        alliance
                    }
                    scores {
                        ... on MatchScores2024 {
                            red {
                                autoPoints
                                autoSamplePoints
                                autoSpecimenPoints
                                autoParkPoints
                                dcPoints
                                dcSamplePoints
                                dcSpecimenPoints
                                dcParkPoints
                                penaltyPointsByOpp
                                minorsByOpp
                                majorsByOpp
                                totalPoints
                                totalPointsNp
                            }
                            blue {
                                autoPoints
                                autoParkPoints
                                autoSamplePoints
                                autoSpecimenPoints
                                dcPoints
                                dcParkPoints
                                dcSamplePoints
                                dcSpecimenPoints
                                penaltyPointsByOpp
                                minorsByOpp
                                majorsByOpp
                                totalPoints
                                totalPointsNp
                            }
                        }
                    }
                    event {
                        name
                        type
                        start
                        started
                        location {
                            venue
                            city
                            state
                            country
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

    match = data.data.matchRecords.data[0].data.match

    red: Alliance = Alliance(match.teams[0], match.teams[1], match.teams[0].alliance, queryUtils.formatMatchScores(match.scores.red))
    blue: Alliance = Alliance(match.teams[2], match.teams[3], match.teams[2].alliance, queryUtils.formatMatchScores(match.scores.blue))

    event: Event = queryUtils.formatEventInfo(match.event)

    result = BestMatch(event, Match(red, blue))

    return QueryResult(result, success)

def upcoming_events(number) -> QueryResult:
    query: str = """
{
    teamByNumber(number: """+number+""") {
        name
        number
        events(season: 2024) {
            event {
                name
                type
                start
                started
                location {
                    venue
                    city
                    state
                    country
                }
            }
        }
    }
}
    """

    success, data = queryUtils.parseQuery(query)
    if not success:
        return QueryResult(data, success)

    team = data.data.teamByNumber

    events = team.events

    unplayed_events = [event for event in events if not event.event.started]

    ev: list[Event] = []

    for event in unplayed_events:
        ev.append(queryUtils.formatEventInfo(event.event))

    t = Team(team.name, team.number)

    result = UpcomingEvents(t, ev)

    return QueryResult(result, success)


def ongoing_events(number) -> QueryResult:
    query: str = """
{
    teamByNumber(number: """ + number + """) {
        name
        number
        events(season: 2024) {
            event {
                name
                type
                start
                ongoing
                location {
                    venue
                    city
                    state
                    country
                }
            }
        }
    }
}
    """

    success, data = queryUtils.parseQuery(query)
    if not success:
        return QueryResult(data, success)

    team = data.data.teamByNumber

    events = team.events

    ongoing_events = [event for event in events if event.event.ongoing]

    ev: list[Event] = []

    for event in ongoing_events:
        ev.append(queryUtils.formatEventInfo(event.event))

    t = Team(team.name, team.number)

    result = OngoingEvents(t, ev)

    return QueryResult(result, success)

def qual_states(number) -> QueryResult:
    query: str = """
{
    teamByNumber(number: """+number+""") {
        name
        number
        events(season: 2024) {
            event {
                name
                type
                start
                started
                awards {
                    teamNumber
                    type
                    placement
                }
                location {
                    city
                    state
                    country
                    venue
                }
            }
            stats {
                ... on TeamEventStats2024 {
                    w: wins
                    l: losses
                    t: ties
                    rank
                }
            }
        }
    }
}
"""

    success, data = queryUtils.parseQuery(query)
    if not success:
        return QueryResult(data, success)

    team = data.data.teamByNumber

    qualifiable_events = [event for event in team.events if event.event.type in ('Qualifier', 'LeagueTournament')]

    qualified_events = [event for event in qualifiable_events for award in event.event.awards if number == str(award.teamNumber) and ((award.type == 'Winner' and (award.placement in (1, 2))) or (award.type == 'Inspire' and award.placement == 1))]

    if not qualified_events:
        qualified_event = None
        has_qualified = False
    else:
        qualified_event = queryUtils.formatTeamEventData(qualified_events[0], team.number)
        has_qualified = True

    team = Team(team.name, team.number)
    result = TeamQualified(team, has_qualified, qualified_event)

    return QueryResult(result, success)

def qual_worlds(number) -> QueryResult:
    query: str = """
{
    teamByNumber(number: """+number+""") {
        name
        number
        events(season: 2024) {
            event {
                name
                type
                start
                started
                awards {
                    teamNumber
                    type
                    placement
                }
                location {
                    city
                    state
                    country
                    venue
                }
            }
            stats {
                ... on TeamEventStats2024 {
                    w: wins
                    l: losses
                    t: ties
                    rank
                }
            }
        }
    }
}
"""

    success, data = queryUtils.parseQuery(query)
    if not success:
        return QueryResult(data, success)

    team = data.data.teamByNumber

    qualifiable_events = [event for event in team.events if event.event.type == 'Championship']

    qualified_events = [event for event in qualifiable_events for award in event.event.awards if number == str(award.teamNumber) and ((award.type == 'Winner' and (award.placement in (1, 2))) or (award.type == 'Inspire' and award.placement == 1))]

    if not qualified_events:
        qualified_event = None
        has_qualified = False
    else:
        qualified_event = queryUtils.formatTeamEventData(qualified_events[0], team.number)
        has_qualified = True

    team = Team(team.name, team.number)
    result = TeamQualified(team, has_qualified, qualified_event)

    return QueryResult(result, success)

def worlds_query(div: str) -> str: # diff func because seasons
    return '''
    {
        eventsSearch(searchText: "''' + div + ''' Division", season: 2024, type: FIRSTChampionship) {
            start
            end
            started
            ongoing
            finished
            name
            stream: liveStreamURL
            teams {
                team {
                    name
                    number
                }
            }
        }

    }    
    '''

def worlds() -> QueryResult:
    divs: list[MajorQualifyingEvent] = []
    for i in ['finals', 'edison', 'jemison', 'franklin', 'ochoa']:

        query = worlds_query(i)

        success, data = queryUtils.parseQuery(query)
        if not success:
            return QueryResult(data, success)

        div = data.data.eventsSearch[0]

        e = div.end.split(sep="-") #eg: ['2025', '04', '19']
        s = div.start.split(sep="-") #eg: ['2025', '04', '15']
        start: EventDates = EventDates(s[0], s[1], s[2], e[2])

        div_name = div.name

        teams: list[Team] = []

        stream: str = div.stream

        for team in div.teams:
            teams.append(Team(team.team.name, team.team.number))

        divs.append(MajorQualifyingEvent(div_name, start, teams, [], div.started, div.ongoing, div.finished, stream)) # not giving matches for worlds due to the sheer number

    result = WorldsEvent(divs[0], divs[1], divs[2], divs[3], divs[4])

    return QueryResult(result, success)