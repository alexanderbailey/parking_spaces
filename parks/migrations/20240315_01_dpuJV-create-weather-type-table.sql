-- create-weather-type-table
-- depends: 20240314_01_Vpvt4-add-historic-field-to-weather-table

-- ######################### CREATE TABLES #########################

-- Create weather_type table
CREATE TABLE weather_type
(
    id                              UUID                        DEFAULT UUID_GENERATE_V4()  NOT NULL,
    name                            TEXT                                                    NOT NULL,
    endpoint                        TEXT                                                    NOT NULL
);

-- ######################### ADD KEYS AND INDEXES #########################

-- Keys and indexes for weather_type

-- Make id the primary key
ALTER TABLE weather_type ADD PRIMARY KEY (id);


-- Add weather_type_id to weather table
ALTER TABLE weather ADD COLUMN type_id UUID;

-- Add foreign key to weather table
ALTER TABLE weather
ADD FOREIGN KEY (type_id)
    REFERENCES weather_type (id)
    ON DELETE SET NULL;