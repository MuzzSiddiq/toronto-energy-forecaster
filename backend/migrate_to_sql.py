from sqlalchemy import create_engine, text
import pandas as pd

# 1. Setup the connection to your Docker container
engine = create_engine('postgresql://user:password@localhost:5432/toronto_pulse')


def migrate_data():
    # 2. Load the cleaned master CSV (which now includes 2023-2026)
    df = pd.read_csv("data/processed/toronto_energy_final.csv")

    # Ensure pandas treats the timestamp as an actual datetime object
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # 3. Load the data into PostgreSQL (The "Load" part of ETL)
    # 'replace' drops the old table and makes a fresh one with the new 2026 data
    print("Syncing database with master CSV (including 2026 updates)...")
    df.to_sql('energy_data', engine, if_exists='replace', index=False)

    # 4. Re-add the index (DDL operation)
    # This makes 'SELECT' queries much faster when we look up dates
    with engine.connect() as conn:
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_timestamp ON energy_data(timestamp);"))
        conn.commit()

    print(f"Database sync complete. {len(df)} rows migrated.")


# --- THIS IS THE MISSING PART: EXECUTION ---
if __name__ == "__main__":
    migrate_data()

