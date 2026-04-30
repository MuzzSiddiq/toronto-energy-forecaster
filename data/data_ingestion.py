import pandas as pd
import glob
import os


def load_and_clean_weather(folder_path):
    # This finds ALL weather CSVs in the folder
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    if not all_files:
        print("Warning: No weather files found!")
        return pd.DataFrame()

    weather_list = []
    for f in all_files:
        df = pd.read_csv(f, usecols=['Date/Time (LST)', 'Temp (°C)', 'Rel Hum (%)', 'Wind Spd (km/h)'])
        weather_list.append(df)

    weather_df = pd.concat(weather_list)
    weather_df['Date/Time (LST)'] = pd.to_datetime(weather_df['Date/Time (LST)'])
    weather_df.rename(columns={'Date/Time (LST)': 'timestamp'}, inplace=True)
    return weather_df


def load_and_clean_energy(folder_path):
    # This finds ALL IESO Demand files (2023, 2024, 2025, etc.)
    all_files = glob.glob(os.path.join(folder_path, "PUB_DemandZonal_*.csv"))
    if not all_files:
        print("Warning: No energy files found!")
        return pd.DataFrame()

    energy_list = []
    for f in all_files:
        df = pd.read_csv(f, skiprows=3)
        df = df[['Date', 'Hour', 'Toronto']]

        # Fixing the Hour 24 logic
        def fix_ieso_time(row):
            date = pd.to_datetime(row['Date'])
            if row['Hour'] == 24:
                return date + pd.Timedelta(days=1)
            else:
                return date + pd.Timedelta(hours=row['Hour'])

        df['timestamp'] = df.apply(fix_ieso_time, axis=1)
        energy_list.append(df[['timestamp', 'Toronto']])

    return pd.concat(energy_list)


# --- MAIN EXECUTION ---
weather = load_and_clean_weather("raw/weather/")
energy = load_and_clean_energy("raw/")

# Check if we actually got data
print(f"Weather rows: {len(weather)}")
print(f"Energy rows: {len(energy)}")

# Merge
master_df = pd.merge(energy, weather, on='timestamp', how='inner')
print(f"Merged rows: {len(master_df)}")

# Only save if we actually have data!
if not master_df.empty:
    master_df['hour'] = master_df['timestamp'].dt.hour
    master_df['day_of_week'] = master_df['timestamp'].dt.dayofweek
    master_df['is_weekend'] = master_df['day_of_week'].isin([5, 6]).astype(int)
    master_df.to_csv("processed/toronto_energy_final.csv", index=False)
    print("Success! Master file created.")
else:
    print("Error: Merged dataframe is empty. Check if your weather and energy years match.")