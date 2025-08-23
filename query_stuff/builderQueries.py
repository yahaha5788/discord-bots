import json

import requests
from types import SimpleNamespace

from misc.utils import GenericEventData, generate_event_data


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
    teamByNumber(number: 21336) {
        name
    }
}
"""
    data = _parse_query(query)
    if data is None:
        return False

    return True

def  query_event(key: str, season: int, region: str, event_type: str) -> list[GenericEventData] | None: # replace any when rtype is determined
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
    '''

    data = _parse_query(query=query)

    if data is None:
        return None

    catcher = data.eventsSearch[0] # raises IndexError if the query was successful but no events were found
    return generate_event_data(data.eventsSearch)


def query_event_awards(event_code: str, season: int):
    query = '''
{
    eventByCode(code: "%s", season: %d) {
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
    ''' % (event_code, season)

    data = _parse_query(query=query)

    if data is None:
        return None

    return

