CREATE TABLE country_event (
    event_id          INTEGER NOT NULL,
    country_id        INTEGER NOT NULL,
    involvement_type  involvement_type_enum NOT NULL,
    notes             TEXT NULL,

    CONSTRAINT fk_country_event_event
        FOREIGN KEY (event_id)
        REFERENCES event (id)
        ON DELETE CASCADE,

    CONSTRAINT fk_country_event_country
        FOREIGN KEY (country_id)
        REFERENCES country (id)
        ON DELETE CASCADE,
    CONSTRAINT pk_country_events
        PRIMARY KEY (event_id, country_id),
    CONSTRAINT ck_country_event_fields_non_empty
        CHECK (notes IS NULL OR TRIM(notes) != '')
);

COMMENT ON TABLE country_event IS 'Junction table linking events to participating/affected countries';

COMMENT ON COLUMN country_event.event_id         IS 'FOREIGN KEY referencing Events table.';
COMMENT ON COLUMN country_event.country_id       IS 'FOREIGN KEY referencing Countries table.';
COMMENT ON COLUMN country_event.involvement_type IS 'Nature of involvement. Must not be NULL.';
COMMENT ON COLUMN country_event.notes            IS 'Additional contextual remarks about the country''s specific role in the event.';

CREATE INDEX ix_country_events_country_id ON country_events (country_id);
COMMENT ON INDEX ix_country_events_country_id IS
    'Supports efficient lookups and joins on country_id.';
CREATE INDEX ix_country_events_involvement_type ON country_events (country_id, involvement_type);
COMMENT ON INDEX ix_country_events_involvement_type IS
    'Composite for role-filtered country lookups (e.g., all events where country was Target).';
