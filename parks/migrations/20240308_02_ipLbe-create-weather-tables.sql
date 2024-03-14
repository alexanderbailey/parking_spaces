-- create-weather-tables
-- depends: 20240308_01_kKWih-create-trigger-to-extract-carpark-spaces-from-server-response

-- ######################### CREATE TABLES #########################

-- Create weather_location table
CREATE TABLE weather_location
(
    id                              UUID                        DEFAULT UUID_GENERATE_V4()  NOT NULL,
    name                            TEXT                                                    NOT NULL,
    lat                             REAL                                                    NOT NULL,
    lon                             REAL                                                    NOT NULL,
    timezone                        TEXT                                                    NOT NULL,
    timezone_offset                 INTEGER                                                 NOT NULL
);

-- Create weather table
CREATE TABLE weather
(
    weather_location_id             UUID                                                    NOT NULL,
    time                            TIMESTAMP WITH TIME ZONE                                NOT NULL,
    data                            JSONB                                                   NOT NULL
);

-- ######################### ADD KEYS AND INDEXES #########################

-- Keys and indexes for weather_location

-- Make id the primary key
ALTER TABLE weather_location ADD PRIMARY KEY (id);

-- Keys and indexes for weather

-- Make weather_location_id and time the primary key
ALTER TABLE weather ADD PRIMARY KEY (weather_location_id, time);

-- Add foreign key to the weather_location table
ALTER TABLE weather ADD FOREIGN KEY (weather_location_id) REFERENCES weather_location(id) ON DELETE SET NULL;

-- Add index to time column
CREATE INDEX ON weather (time);