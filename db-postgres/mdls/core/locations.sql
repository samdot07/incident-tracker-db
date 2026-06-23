CREATE TABLE location (
    id                INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid              UUID NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    notes             TEXT NULL,
    location_name     VARCHAR(200) NOT NULL,
    coordinates       GEOGRAPHY(POINT, 4326) NULL,   -- WGS84 point
    location_type     location_type_enum NOT NULL,
    country_id        INTEGER NULL,
    description       TEXT NULL,
    
    CONSTRAINT fk_location_country
        FOREIGN KEY (country_id)
        REFERENCES country (id)
        ON DELETE SET NULL,
    CONSTRAINT ck_locations_fields_non_empty
        CHECK (
            TRIM(location_name) != ''
            AND (description IS NULL OR TRIM(description) != '')
            AND (notes IS NULL OR TRIM(notes) != '')
        )
);

COMMENT ON TABLE location IS 'Models specific geographic points or areas where incidents occur.';

COMMENT ON COLUMN location.id                IS 'Integer primary key (from IdMixin).';
COMMENT ON COLUMN location.uuid              IS 'Universally unique identifier (from UUIDMixin).';
COMMENT ON COLUMN location.created_at        IS 'Timestamp of row creation (from TimestampMixin).';
COMMENT ON COLUMN location.updated_at        IS 'Timestamp of last update (from TimestampMixin).';
COMMENT ON COLUMN location.notes             IS 'Additional remarks (from NotesMixin).';
COMMENT ON COLUMN location.location_name     IS 'Geographic feature or area name.';
COMMENT ON COLUMN location.coordinates       IS 'PostGIS GEOGRAPHY point (lat/long in WGS84). Nullable for approximate/regional coordinates.';
COMMENT ON COLUMN location.location_type     IS 'Classification for pattern analysis (Disputed Island, Maritime Feature, Border Region, Capital City, Military Installation, Economic Zone, International Waters, Other).';
COMMENT ON COLUMN location.country_id        IS 'FOREIGN KEY to countries table. Nullable for disputed territories or international waters.';
COMMENT ON COLUMN location.description       IS 'Contextual details for analyst understanding and disambiguation.';

CREATE INDEX ix_location_type ON locations (location_type);
COMMENT ON INDEX ix_location_type IS
    'Speeds up queries filtering by location type, e.g., WHERE Location_Type = "Disputed Island".';
CREATE INDEX ix_country_id_location_type ON locations (country_id, location_type);
COMMENT ON INDEX ix_country_id_location_type IS
    'Composite index for queries filtering by both country and location type, avoiding multiple index scans.';
CREATE INDEX ix_country_id_created_at ON locations (country_id, created_at);
COMMENT ON INDEX ix_country_id_created_at IS
    'Optimizes queries that filter by country and order by creation date, supporting efficient pagination.';
CREATE INDEX ix_location_created_at ON locations (created_at);
COMMENT ON INDEX ix_location_created_at IS
    'Supports time-based queries such as sorting or filtering location by creation date.';
CREATE INDEX ix_location_name ON locations (location_name);
COMMENT ON INDEX ix_location_name IS
    'Supports exact match lookups on location name, often used in point queries or unique constraint checks.';
CREATE INDEX ix_coordinates ON locations USING GIST (coordinates);
COMMENT ON INDEX ix_coordinates IS
    'GiST index for spatial queries (distance, bounding box) on the coordinate column.';
CREATE INDEX ix_location_name_gin ON locations USING GIN (location_name gin_trgm_ops);
COMMENT ON INDEX ix_location_name_gin IS
    'GIN trigram index enabling fast ILIKE and similarity searches on location names with wildcards.';
CREATE INDEX ix_location_name_lower ON locations (lower(location_name));
COMMENT ON INDEX ix_location_name_lower IS
    'Functional index for case-insensitive equality searches, useful when normalized names are required.';
CREATE INDEX ix_location_unattributed ON locations (location_name)
    WHERE country_id IS NULL;
COMMENT ON INDEX ix_location_unattributed IS
    'Partial index for lookups and audits of locations with no country attribution (disputed territories, international waters).';

CREATE OR REPLACE TRIGGER tg_location_updated
    BEFORE UPDATE ON location
    FOR EACH ROW
    EXECUTE FUNCTION update_tg();