CREATE TABLE event_source (
    event_id         INTEGER NOT NULL,
    source_id        INTEGER NOT NULL,
    page_reference   VARCHAR(50) NULL,
    notes            TEXT NULL,

    CONSTRAINT fk_event_source_event
        FOREIGN KEY (event_id)
        REFERENCES event (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_event_source_source
        FOREIGN KEY (source_id)
        REFERENCES source (id)
        ON DELETE CASCADE,
    CONSTRAINT pk_event_sources
        PRIMARY KEY (event_id, source_id),
    CONSTRAINT ck_event_source_fields_non_empty
        CHECK (notes IS NULL OR TRIM(notes) != '')
);

COMMENT ON TABLE event_source IS 'Junction table linking events to documentary sources with citation details.';

COMMENT ON COLUMN event_source.event_id        IS 'FOREIGN KEY referencing events table.';
COMMENT ON COLUMN event_source.source_id       IS 'FOREIGN KEY referencing sources table.';
COMMENT ON COLUMN event_source.page_reference  IS 'Specific page numbers or section identifiers within source documents.';
COMMENT ON COLUMN event_source.notes           IS 'Additional contextual remarks about the credibility, interpretation, or significance of this source for the given event.';

CREATE INDEX ix_event_sources_source_id ON event_sources (source_id);
COMMENT ON INDEX ix_event_sources_source_id IS
    'Optimizes lookups by source_id.';
