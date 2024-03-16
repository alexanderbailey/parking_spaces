-- create-spaces-table
-- depends: 20240227_02_ydmdB-create-carpark-table

-- ######################### CREATE TABLES #########################

-- Create spaces table
CREATE TABLE spaces
(
    id                              UUID                        DEFAULT UUID_GENERATE_V4()  NOT NULL,
    carpark_id                      UUID                                                    NOT NULL,
    open                            BOOL                                                    NOT NULL,
    spaces                          INTEGER                                                 NOT NULL,
    unusable_spaces                 INTEGER                                                 NOT NULL,
    time                            TIMESTAMP WITH TIME ZONE                                NOT NULL
);

-- ######################### ADD KEYS AND INDEXES #########################

-- Keys and indexes for carpark

-- Make id the primary key
ALTER TABLE spaces ADD PRIMARY KEY (id);
-- Add a foreign key to the carpark table
ALTER TABLE spaces ADD FOREIGN KEY (carpark_id) REFERENCES carpark (id) ON DELETE SET NULL;