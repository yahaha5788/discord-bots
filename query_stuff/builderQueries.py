import json

import requests
from types import SimpleNamespace

from misc.utils import GenericEventData, generate_event_data, AwardCompilation, generate_award_data, TeamData, generate_team_data


def _parse_query(query: str) -> SimpleNamespace | None:
    response = requests.post(url="https://api.ftcscout.org/graphql", json={"query": query})
    if response.status_code == 200:

        data: SimpleNamespace = json.loads(response.content, object_hook=lambda j: SimpleNamespace(**j))
        return data.data

    else:
        return None

def ping_query() -> bool:
    query: str = """
{
    activeTeamsCount(season: 2024)
}
"""
    data = _parse_query(query)
    if data is None:
        return False

    return True

def query_event(key: str, season: int, region: str, event_type: str) -> list[GenericEventData] | None:
    query = '''
{
    eventsSearch(searchText: "'''+key+'''", season: '''+str(season)+''', region: '''+region+''', type: '''+event_type+''') {
        name
        start
        end
        started
        ongoing
        type
        location {
            venue
            city
            state
            country
        }
        teams {
            teamNumber
        }
        matches {
            matchNum
        }
        code
    }
}
    ''' # yeah ik it's bad formatting but this is the only thing that works

    data = _parse_query(query=query)

    if data is None:
        return None

    catcher = data.eventsSearch[0] # raises IndexError if the query was successful but no events were found
    return generate_event_data(data.eventsSearch)


def query_event_awards(event_code: str, season: int) -> AwardCompilation | None:
    query = '''
{
    eventByCode(code: "'''+event_code+''''", season: '''+str(season)+''') {
        awards {
            team {
                name
                number
            }
            placement
            type
        }
    }
}
    '''

    data = _parse_query(query=query)

    if data is None:
        return None

    event_awards = data.eventByCode.awards
    awards = [generate_award_data(award) for award in event_awards]

    return AwardCompilation(awards)

def query_team_data(number: int) -> TeamData | None:
    query = '''
{
    team: teamByNumber(number: '''+str(number)+''') {
        name
        number
        location {
            city
            state
            country
        }
        website
        quickStats(season: 2024) {
            auto {
                rank
                value
            }
            tele: dc {
                rank
                value
            }
            endgame: eg {
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
    '''

    data = _parse_query(query=query)

    if data is None:
        return None

    team = data.team

    return generate_team_data(team)
