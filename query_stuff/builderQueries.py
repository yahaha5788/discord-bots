import json
from typing import Any

import requests
from types import SimpleNamespace

def _parse_query(query: str) -> SimpleNamespace | None:
    response = requests.post(url="https://api.ftcscout.org/graphql", json={"query": query})
    if response.status_code == 200:

        data: SimpleNamespace = json.loads(response.content, object_hook=lambda j: SimpleNamespace(**j))
        return data

    else:
        return None

def query_event(keyword: str, season: int, region: str, event_type: str) -> Any | None: # replace any when rtype is determined

    query = """
{
    eventsSearch(searchText: %s, season: %d, region: %s, type: %s) {
        name
        start
        end
        started
        ongoing
        finished
        type
        location {
            venue
            city
            state
            country
        }
    }
}
    """ % (keyword, season, region, event_type) # bad method of formatting but others use {} so they won't work

    data = _parse_query(query=query)

    if data is None:
        return None


