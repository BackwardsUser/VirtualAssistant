import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

import math

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 43.7001,
	"longitude": -79.4163,
	"current": ["temperature_2m", "relative_humidity_2m", "precipitation", "rain", "showers", "snowfall",
				"cloud_cover", "wind_speed_10m"],
	"daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_probability_max", "wind_speed_10m_max"],
	"timezone": "America/New_York"
}


def get_weather():
	global openmeteo, params, url

	responses = openmeteo.weather_api(url, params=params)
	response = responses[0]

	current = response.Current()

	temperature = current.Variables(0).Value()
	humidity = current.Variables(1).Value()
	precipitation = current.Variables(2).Value()
	rain = current.Variables(3).Value()
	showers = current.Variables(4).Value()
	snowfall = current.Variables(5).Value()
	cloud_coverage = current.Variables(6).Value()
	wind_speed = current.Variables(7).Value()

	daily = response.Daily()

	max_temp = daily.Variables(0).Value()
	min_temp = daily.Variables(1).Value()
	precipitation_sum = daily.Variables(2).Value()
	rain_sum = daily.Variables(3).Value()

	wind_speed_knt = wind_speed/1.852

	wind_chill = (0.6215 * temperature) - (11.37 * math.pow(wind_speed, 0.16)) + (0.3965 * temperature * math.pow(wind_speed, 0.16)) + 13.12

	if wind_chill < 0:
		wear = "Coat and Pants! Bundle up! "
	elif wind_chill < 10:
		wear = "Coat and Pants! "
	elif wind_chill < 15:
		wear = "Sweater and Pants! "
	else:
		wear = "T-Shirt and Shorts! "

	retval = f"The temperature is {round(temperature)} Celsius,"
	if round(temperature) != round(wind_chill):
		retval += f" however it will feel like {round(wind_chill)} Celsius with the wind chill"
	if humidity:
		retval += f" but mind the humidity at {round(humidity)}%"
	retval += f", I'd recommend wearing a, {wear}"

	if precipitation > 0:
		retval += f" Expect precipitation of around {round(precipitation)}mm."
	if rain > 0:
		retval += f" Expect rainfall of around {round(rain)}mm."
	if showers > 0:
		retval += f" Expect showers of around {round(showers)}mm"
	if snowfall > 0:
		ending = "! That's a lot!" if snowfall > 91.44 else "."
		retval += f" Expect snowfall of around {round(snowfall)}cm{ending}"

	if cloud_coverage == 0:
		retval += f" and expect clear skies!"
	elif 25 > cloud_coverage > 0:
		retval += f" and expect partially clear skies."
	elif 50 > cloud_coverage > 25:
		retval += f" and expect cloudy skies."
	elif 75 > cloud_coverage > 50:
		retval += f" and expect largely cloudy skies."
	else:
		retval += f" and expect heavy cloud coverage."

	# retval += f" Today's high is {max_temp} with a low of {min_temp}."

	return retval