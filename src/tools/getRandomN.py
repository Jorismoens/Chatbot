import json

import requests
from requests import Response


# Use randomnumber API to get a series of random numbers
def get_random_numbers(min: int, max: int, count: int) -> str:
    url = "http://www.randomnumberapi.com/api/v1.0/random"
    params = {
        'min': min,
        'max': max,
        'count': count
    }
    response = requests.get(url,
                            params=params)
    return json.dumps({"random numbers": response.json()})
