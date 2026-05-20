import requests
import pandas as pd
import joblib
from sqlalchemy import create_engine, text
import os

# step phase
MODEL_PATH = "backend/models/toronto_energy_model.pkl" # update path if necessary
EXTERNAL_URL = "postgresql://user:ZM0GnPNfhxiw11t3nlC13qF97eu5HmUk@dpg-d81ng1cdirrc73dpd9fg-a.oregon-postgres.render.com/toronto_pulse"

if EXTERNAL_URL.startswith("postgres://"):
    EXTERNAL_URL = EXTERNAL_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(EXTERNAL_URL)

def get_weather_forecast():
    # Toronto Coordinates: 43.65, -79.38
    url = "https://api.open-meteo.com/v1/forecast?latitude=43.65&longitude=-79.38&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

    print("Fetching 7-day weather forecast for Toronto...")
    response = requests.get(url).json()

    # Parse the JSON response into a DataFrame
    hourly = response['hourly']
    df = pd.DataFrame({
        'timestamp': pd.to_datetime(hourly['time']),
        'Temp (°C)': hourly['temperature_2m'],
        'Rel Hum (%)': hourly['relative_humidity_2m'],
        'Wind Spd (km/h)': hourly['wind_speed_10m']
    })
    return df

def generate_forecast():
    # Load the weather and the ML model
    forecast_df = get_weather_forecast()
    model = joblib.load(MODEL_PATH)

    # Feature Engineering (creating the same columns the model was trained on)
    forecast_df['hour'] = forecast_df['timestamp'].dt.hour
    forecast_df['day_of_week'] = forecast_df['timestamp'].dt.dayofweek
    forecast_df['is_weekend'] = forecast_df['day_of_week'].isin([5, 6]).astype(int)

    # Define features and predict
    features = ['Temp (°C)', 'Rel Hum (%)', 'Wind Spd (km/h)', 'hour', 'day_of_week', 'is_weekend']
    forecast_df['predicted_demand'] = model.predict(forecast_df[features])

    # Save to a NEW table in SQL
    print("Saving 7-day forecast to database...")
    forecast_df[['timestamp', 'predicted_demand']].to_sql('forecasts', engine, if_exists='replace', index=False)
    print("Forecast complete!")


if __name__ == "__main__":
    generate_forecast()
