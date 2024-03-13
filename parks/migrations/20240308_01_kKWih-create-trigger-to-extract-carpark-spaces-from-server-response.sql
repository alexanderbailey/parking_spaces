-- create-trigger-to-extract-carpark-spaces-from-server-response
-- depends: 20240227_04_MvBhJ-create-server-response-table

-- Create function to insert spaces
CREATE FUNCTION insert_spaces(
    _carpark_code TEXT,
    _open BOOL,
    _spaces INTEGER,
    _unusable_spaces INTEGER,
    _timestamp TIMESTAMP WITH TIME ZONE
) RETURNS BOOL AS
$$
    INSERT INTO spaces (
        carpark_id,
        open,
        spaces,
        unusable_spaces,
        time
    )
	VALUES (
		(
			SELECT id
			FROM carpark
			WHERE code = _carpark_code
		),
		_open,
		_spaces,
		_unusable_spaces,
		_timestamp
	)
    RETURNING TRUE;
$$ LANGUAGE sql;

-- Create trigger function to loop through carparks and insert spaces
CREATE OR REPLACE FUNCTION extract_carpark_spaces() RETURNS trigger
    LANGUAGE plpgsql
AS
$$
DECLARE carpark JSONB;
BEGIN
	FOR carpark IN
		SELECT * FROM JSONB_ARRAY_ELEMENTS((NEW.response->'carparkData'->'Jersey'->'carpark'))
	LOOP
		PERFORM public.insert_spaces(
			carpark->>'code',
			(carpark->'carparkOpen')::BOOL,
			(carpark->'spaces')::INTEGER,
			(carpark->'numberOfSpacesConsideredLow')::INTEGER,
			TO_TIMESTAMP(SUBSTRING(NEW.response->'carparkData'->>'Timestamp', 33) || ' ' || DATE_PART('year', now()) , 'HH24:MI:SS on Day DD Month YYYY')
		);
	END LOOP;
    RETURN NEW;
END;
$$;

-- Create trigger after insert on server_response table
CREATE OR REPLACE TRIGGER insert_spaces_trigger
    AFTER INSERT
    ON public.server_response
    FOR EACH ROW
    EXECUTE FUNCTION public.extract_carpark_spaces();
