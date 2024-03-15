-- add-historic-field-to-weather-table
-- depends: 20240308_02_ipLbe-create-weather-tables

-- Add a historic field to the weather table
ALTER TABLE weather ADD COLUMN historic BOOLEAN NOT NULL DEFAULT FALSE;