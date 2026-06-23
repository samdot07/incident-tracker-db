CREATE TABLE event_type (
    id                INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid              UUID NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    notes             TEXT NULL,
    type_name         VARCHAR(100) NOT NULL,
    parent_type_id    INTEGER NULL,
    event_type        event_type_enum NOT NULL,
    definition        TEXT NOT NULL,
    examples          TEXT NULL,

    CONSTRAINT fk_event_type_parent
        FOREIGN KEY (parent_type_id)
        REFERENCES event_type (id)
        ON DELETE RESTRICT,
    CONSTRAINT uq_event_types_type_name_parent_type_id
        UNIQUE (type_name, parent_type_id),
    CONSTRAINT ck_event_types_fields_non_empty
        CHECK (
            TRIM(type_name) != ''
            AND TRIM(definition) != ''
            AND (examples IS NULL OR TRIM(examples) != '')
            AND (notes IS NULL OR TRIM(notes) != '')
        )
);

COMMENT ON TABLE event_type IS 'Implements two-tier hierarchical taxonomy distinguishing primary categories from subcategories.';

COMMENT ON COLUMN event_type.id                IS 'Integer primary key (from IdMixin).';
COMMENT ON COLUMN event_type.uuid              IS 'Universally unique identifier (from UUIDMixin).';
COMMENT ON COLUMN event_type.created_at        IS 'Timestamp of row creation (from TimestampMixin).';
COMMENT ON COLUMN event_type.updated_at        IS 'Timestamp of last update (from TimestampMixin).';
COMMENT ON COLUMN event_type.notes             IS 'Free-text notes about the category (e.g., changes in definition over time).';
COMMENT ON COLUMN event_type.type_name         IS 'Category or subcategory name.';
COMMENT ON COLUMN event_type.parent_type_id    IS 'Self-referential FOREIGN KEY implementing hierarchical taxonomy. NULL for primary categories, populated for subcategories.';
COMMENT ON COLUMN event_type.event_type        IS 'Primary category from the fixed taxonomy.';
COMMENT ON COLUMN event_type.definition        IS 'Operational definition specifying scope, inclusion criteria, boundary conditions, and disambiguation from related categories.';
COMMENT ON COLUMN event_type.examples          IS 'Representative incidents exemplifying the category, supporting decisions for ambiguous cases.';

CREATE INDEX ix_parent_type_id ON event_types (parent_type_id);
COMMENT ON INDEX ix_parent_type_id IS
    'Optimizes lookups for events by parent type, commonly used in hierarchical queries and foreign key joins.';
CREATE INDEX ix_event_type_created_at ON event_types (created_at);
COMMENT ON INDEX ix_event_type_created_at IS
    'Supports time-based queries such as sorting or filtering event types by creation date.';

CREATE OR REPLACE TRIGGER tg_event_type_updated
    BEFORE UPDATE ON event_type
    FOR EACH ROW
    EXECUTE FUNCTION update_tg();