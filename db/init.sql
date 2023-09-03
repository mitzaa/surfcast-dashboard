-- SQL initialization script
-- Will add tables and data here

CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT,
    description TEXT
);

CREATE TABLE forecasts (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    timestamp TIMESTAMP,
    waveHeight FLOAT,
    waveDirection FLOAT,
);
