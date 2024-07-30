import json

import openmeteo_requests

import requests_cache


def get_temperature(latitude: float, longitude: float) -> float:
	global url, params, response, value # TODO remove of refactor this line
	# Set up the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
	# retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session=cache_session)

	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": latitude,
		"longitude": longitude,
		"current": "temperature_2m"
	}
	responses = openmeteo.weather_api(url, params=params)
	value = responses[0].Current().Variables(0).Value()
	# value = -10.0
	return json.dumps({"temperature": str(value)})
