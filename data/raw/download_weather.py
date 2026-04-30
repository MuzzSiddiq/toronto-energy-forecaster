import requests
import os
import time

STATION_ID = 51459
YEARS = [2023, 2024, 2025]
BASE_URL = "https://climate.weather.gc.ca/climate_data/bulk_data_e.html"

output_dir = "weather"
os.makedirs(output_dir, exist_ok=True)

for year in YEARS:
    for month in range(1, 13):
        print("Downloading weather for " + str(month) + "/" + str(year))

        params = {
            "format": "csv",
            "stationID": STATION_ID,
            "Year": year,
            "Month": month,
            "Day": 1,
            "timeframe": 1,  # 1 = Hourly
            "submit": "Download Data"
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            filename = f"weather_toronto_{year}_{month:02d}.csv"
            with open(os.path.join(output_dir, filename), 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download {year}-{month}")

        # Be a good citizen: wait 1 second between requests so we don't spam the server
        time.sleep(1)

print("All weather data downloaded successfully!")