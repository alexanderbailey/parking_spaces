-- create-server-response-table
-- depends: 20240227_03_fliGq-create-spaces-table

-- ######################### CREATE TABLES #########################

-- Create server_reponse table
CREATE TABLE server_response
(
    timestamp                       BIGINT                                                  NOT NULL,
    response                        JSONB                                                   NOT NULL
);

-- ######################### ADD KEYS AND INDEXES #########################

-- Keys and indexes for server_response

-- Make timestamp the primary key
ALTER TABLE server_response ADD PRIMARY KEY (timestamp);