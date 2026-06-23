CREATE OR REPLACE FUNCTION update_tg()
    RETURNS TRIGGER AS $$
    BEGIN
        IF OLD IS DISTINCT FROM NEW THEN
            NEW.updated_at = clock_timestamp();
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

COMMENT ON FUNCTION update_tg() IS 
    'Set updated_at to current timestamp only when row data actually changes';