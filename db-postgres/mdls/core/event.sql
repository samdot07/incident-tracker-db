CREATE TABLE event (
    id                INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid              UUID NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    notes             TEXT NULL,
    event_name                VARCHAR(100) NOT NULL,
    event_date                DATE NOT NULL,
    event_end_date            DATE NULL,
    location_id               INTEGER NULL,
    event_type_id             INTEGER NOT NULL,
    description               TEXT NOT NULL,
    attribution_confidence    attribution_confidence_enum NOT NULL DEFAULT 'confirmed',

    CONSTRAINT fk_event_location
        FOREIGN KEY (location_id)
        REFERENCES location (id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_event_event_type
        FOREIGN KEY (event_type_id)
        REFERENCES event_type (id)
        ON DELETE RESTRICT,
    CONSTRAINT ck_events_valid_event_end_date
        CHECK (event_end_date IS NULL OR event_end_date >= event_date),
    CONSTRAINT ck_events_fields_non_empty
        CHECK (
            TRIM(event_name) != ''
            AND TRIM(description) != ''
            AND (notes IS NULL OR TRIM(notes) != '')
        )
);

COMMENT ON TABLE event IS 'Stores individual geopolitical incidents as the primary unit of analysis.';

COMMENT ON COLUMN event.id                     IS 'Integer primary key (from IdMixin).';
COMMENT ON COLUMN event.uuid                   IS 'Universally unique identifier (from UUIDMixin).';
COMMENT ON COLUMN event.created_at             IS 'Timestamp of row creation (from TimestampMixin).';
COMMENT ON COLUMN event.updated_at             IS 'Timestamp of last update (from TimestampMixin).';
COMMENT ON COLUMN event.notes                  IS 'Free-text analyst remarks (from NotesMixin). Non-empty if provided.';
COMMENT ON COLUMN event.event_name             IS 'Full event name.';
COMMENT ON COLUMN event.event_date             IS 'Occurrence DATE of the incident (without time). Must not be NULL.';
COMMENT ON COLUMN event.event_end_date         IS 'End DATE for extended-duration events (optional). Must be on or after event_date.';
COMMENT ON COLUMN event.location_id            IS 'FOREIGN KEY to locations table. Nullable if event lacks precise spatial attribution.';
COMMENT ON COLUMN event.event_type_id          IS 'FOREIGN KEY to event_type table. Must not be NULL.';
COMMENT ON COLUMN event.description            IS 'Narrative summary of the incident. Must not be NULL.';
COMMENT ON COLUMN event.attribution_confidence IS 'Confidence level in actor attribution and factual accuracy. Defaults to "confirmed".';

CREATE INDEX ix_location_id_event_date ON events (location_id, event_date);
COMMENT ON INDEX ix_location_id_event_date IS
    'Composite for geospatial-temporal queries filtering events by location within a date range.';
CREATE INDEX ix_event_type_id ON events (event_type_id);
COMMENT ON INDEX ix_event_type_id IS
    'Speeds up lookups by event type ID, used for filtering events by their dedicated type.';
CREATE INDEX ix_event_type_id_event_date ON events (event_type_id, event_date);
COMMENT ON INDEX ix_event_type_id_event_date IS
    'Supports filtering by event type combined with date range, common for dashboard queries.';

CREATE OR REPLACE TRIGGER tg_event_updated
    BEFORE UPDATE ON event
    FOR EACH ROW
    EXECUTE FUNCTION update_tg();