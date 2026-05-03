from sqlalchemy import create_engine, text

# Connect to the DB
engine = create_engine('postgresql://user:password@localhost:5432/toronto_pulse')

# Use standard SQL to query the first 5 rows
with engine.connect() as connection:
    # Change 'demand_mw' to 'Toronto'
    result = connection.execute(text('SELECT "timestamp", "Toronto" FROM energy_data LIMIT 5'))
    print("--- Database Sample ---")
    for row in result:
        print(f"Time: {row[0]} | Demand: {row[1]} MW")