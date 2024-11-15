import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
	"latitude": 28.6519,
	"longitude": 77.2315,
	"hourly": ["pm10", "pm2_5", "carbon_monoxide", "sulphur_dioxide", "ozone", "dust", "uv_index"],
	"timezone": "Asia/Singapore",
	"past_days": 92
}

def get_latest_data():
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]
	print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
	print(f"Elevation {response.Elevation()} m asl")
	print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
	print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_pm10 = hourly.Variables(0).ValuesAsNumpy()
	hourly_pm2_5 = hourly.Variables(1).ValuesAsNumpy()
	hourly_carbon_monoxide = hourly.Variables(2).ValuesAsNumpy()
	hourly_sulphur_dioxide = hourly.Variables(3).ValuesAsNumpy()
	hourly_ozone = hourly.Variables(4).ValuesAsNumpy()
	hourly_dust = hourly.Variables(5).ValuesAsNumpy()
	hourly_uv_index = hourly.Variables(6).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}
	hourly_data["pm10"] = hourly_pm10
	hourly_data["pm2_5"] = hourly_pm2_5
	hourly_data["carbon_monoxide"] = hourly_carbon_monoxide
	hourly_data["sulphur_dioxide"] = hourly_sulphur_dioxide
	hourly_data["ozone"] = hourly_ozone
	hourly_data["dust"] = hourly_dust
	hourly_data["uv_index"] = hourly_uv_index

	hourly_dataframe = pd.DataFrame(data = hourly_data)

	hourly_dataframe.to_csv("./aqi.csv")
	print(hourly_dataframe)