-- Create the main table for historical energy and weather
CREATE TABLE energy_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP UNIQUE NOT NULL,
    demand_mw FLOAT NOT NULL,
    temperature FLOAT,
    humidity FLOAT,
    wind_speed FLOAT,
    hour INT,
    day_of_week INT,
    is_weekend INT
);

-- Create an index on timestamp for lightning-fast lookups
CREATE INDEX idx_timestamp ON energy_data(timestamp);


