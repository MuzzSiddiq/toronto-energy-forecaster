import pandas as pd
import glob
import os


def load_and_clean_weather(folder_path):
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    weather_list = []

    for f in all_files:
        # We only need the timestamp and the core metrics
        df = pd.read_csv(f, usecols=['Date/Time (LST)', 'Temp (°C)', 'Rel Hum (%)', 'Wind Spd (km/h)'])
        weather_list.append(df)

    weather_df = pd.concat(weather_list)
    weather_df['Date/Time (LST)'] = pd.to_datetime(weather_df['Date/Time (LST)'])
    weather_df.rename(columns={'Date/Time (LST)': 'timestamp'}, inplace=True)
    return weather_df


def load_and_clean_energy(file_path):
    df = pd.read_csv(file_path, skiprows=3)
    df = df[['Date', 'Hour', 'Toronto']]

    # Logic to convert IESO "Date + Hour" to a real timestamp
    # If Hour is 24, we set it to 0 and add 1 day
    def fix_ieso_time(row):
        date = pd.to_datetime(row['Date'])
        if row['Hour'] == 24:
            return date + pd.Timedelta(days=1)
        else:
            return date + pd.Timedelta(hours=row['Hour'])

    df['timestamp'] = df.apply(fix_ieso_time, axis=1)
    return df[['timestamp', 'Toronto']]


# --- MAIN EXECUTION ---
print("Wrangling weather data...")
weather = load_and_clean_weather("raw/weather/")

print("Wrangling energy data...")
energy_2025 = load_and_clean_energy("PUB_DemandZonal_2025.csv")  # Repeat for other years

# Merge them!
master_df = pd.merge(energy_2025, weather, on='timestamp', how='inner')

# Feature Engineering: Add the "Time" context for the ML model
master_df['hour'] = master_df['timestamp'].dt.hour
master_df['day_of_week'] = master_df['timestamp'].dt.dayofweek
master_df['is_weekend'] = master_df['day_of_week'].isin([5, 6]).astype(int)

master_df.to_csv("data/processed/toronto_energy_final.csv", index=False)
print("Merge Complete! Your training data is ready.")