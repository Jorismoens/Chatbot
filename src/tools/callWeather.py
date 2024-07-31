import json

import openmeteo_requests

import requests_cache


# Call the openmeteo weather API to retrieve the temperature for a specific location.
def get_temperature(latitude: float, longitude: float) -> str:
	cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
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
