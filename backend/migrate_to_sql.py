from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine('postgresql://user:password@localhost:5432/toronto_pulse')


def migrate_data():
    df = pd.read_csv("data/processed/toronto_energy_final.csv")

    # Using 'replace' for now is okay while you're learning,
    # but in a real app, we'd use a temporary table and 'ON CONFLICT'
    print("Syncing database with master CSV...")
    df.to_sql('energy_data', engine, if_exists='replace', index=False)

    # IMPORTANT: Re-add the index if we used 'replace'
    with engine.connect() as conn:
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_timestamp ON energy_data(timestamp);"))
        conn.commit()
    print("Database sync complete.")


