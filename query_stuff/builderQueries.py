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

def query_event(keyword: str, season: int, region: str, event_type: str) -> GenericEventData | None: # replace any when rtype is determined

    query = '''
{
    eventsSearch(searchText: "%s", season: %d, region: %s, type: %s) {
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
        {
        matches {
            matchNum
        }
    }
}
    ''' % (keyword, season, region, event_type) # bad method of formatting but others use {} so they won't work

    data = _parse_query(query=query)

    if data is None:
        return None

    return generate_event_data(data.eventsSearch[0])

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

