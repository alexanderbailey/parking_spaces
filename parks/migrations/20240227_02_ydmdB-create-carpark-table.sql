-- create-carpark-table
-- depends: 20240227_01_mNXbP-initialise

-- ######################### CREATE TABLES #########################

-- Create carpark table
CREATE TABLE carpark
(
    id                              UUID                        DEFAULT UUID_GENERATE_V4()  NOT NULL,
    name                            TEXT                                                    NOT NULL,
    code                            TEXT                                                    NOT NULL,
    type                            TEXT                                                    NOT NULL,
    low                             INTEGER                                                 NOT NULL
);

-- ######################### ADD KEYS AND INDEXES #########################

-- Keys and indexes for carpark

-- Make id the primary key
ALTER TABLE carpark ADD PRIMARY KEY (id);
-- Add uniqueness constraint to code
ALTER TABLE carpark ADD UNIQUE (code);

