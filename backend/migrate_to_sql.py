import pandas as pd
from sqlalchemy import create_engine

# 1. Load the CSV we made in Step 1 & 2
df = pd.read_csv("data/processed/toronto_energy_final.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 2. Connect to the Dockerized Postgres
# Format: postgresql://username:password@localhost:5432/database_name
engine = create_engine('postgresql://user:password@localhost:5432/toronto_pulse')

# 3. Upload the data
print("Uploading data to PostgreSQL...")
df.to_sql('energy_data', engine, if_exists='replace', index=False)

print("Migration successful! Your data is now in a real relational database.")