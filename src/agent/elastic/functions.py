import os
import requests
from dotenv import load_dotenv


load_dotenv()


ELASTIC_ENDPOINT = os.environ.get("ELASTIC_ENDPOINT")
HEADERS = {
    "Content-Type": "application/json",
    "accept": "application/json",
}


def elasticsearch_request(search_term: str, size: int):
    """Runs elasticsearch request in order to obtain information about given <search_term>. Will return <size>
    number of results.

    """

    data = {
      "from": 0,
      "indexes": [
        "materials.substances.id"
      ],
      "ranges": [
        {
          "field": "date.endDate",
          "gte": "2024-01-01T00:00:00",
          "lte": "2024-12-31T23:59:59"
        }
      ],
      "search_term": search_term,
      "size": size,
    }

    response = requests.post(ELASTIC_ENDPOINT, json=data, headers=HEADERS, verify=False)
    return response.json()
