CREATE TABLE country (
    id                INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid              UUID NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    notes             TEXT NULL,
    country_name      VARCHAR(100) NOT NULL,
    iso_alpha_2       VARCHAR(2) NOT NULL,
    iso_alpha_3       VARCHAR(3) NOT NULL,
    region            region_enum NOT NULL,
    asean_member      BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT uq_country_country_name UNIQUE (country_name),
    CONSTRAINT uq_country_iso_alpha_2  UNIQUE (iso_alpha_2),
    CONSTRAINT uq_country_iso_alpha_3  UNIQUE (iso_alpha_3),
    CONSTRAINT ck_countries_iso_upper_case
        CHECK (iso_alpha_2 = UPPER(iso_alpha_2) AND iso_alpha_3 = UPPER(iso_alpha_3)),
    CONSTRAINT ck_countries_iso_length
        CHECK (LENGTH(iso_alpha_2) = 2 AND LENGTH(iso_alpha_3) = 3),
    CONSTRAINT ck_countries_fields_non_empty
        CHECK (TRIM(country_name) != '' AND (notes IS NULL OR TRIM(notes) != ''))
);

COMMENT ON TABLE country IS 'Stores country data for analysis, focusing on ASEAN members and their key dialogue partners.';

COMMENT ON COLUMN country.id                IS 'Integer primary key (from IdMixin).';
COMMENT ON COLUMN country.uuid              IS 'Universally unique identifier (from UUIDMixin).';
COMMENT ON COLUMN country.created_at        IS 'Timestamp of row creation (from TimestampMixin).';
COMMENT ON COLUMN country.updated_at        IS 'Timestamp of last update (from TimestampMixin).';
COMMENT ON COLUMN country.notes             IS 'Free-text analyst remarks (from NotesMixin). Non-empty if provided.';
COMMENT ON COLUMN country.country_name      IS 'Official name of the country. Must be UNIQUE.';
COMMENT ON COLUMN country.iso_alpha_2       IS 'ISO 3166-1 alpha-2 country code. UNIQUE.';
COMMENT ON COLUMN country.iso_alpha_3       IS 'ISO 3166-1 alpha-3 country code. UNIQUE.';
COMMENT ON COLUMN country.region            IS 'Geographic region for grouping data (Mainland Southeast Asia, Maritime Southeast Asia, East Asia, South Asia, Oceania, North America, Europe, Other).';
COMMENT ON COLUMN country.asean_member      IS 'BOOLEAN flag indicating ASEAN membership status. Default FALSE.';

CREATE INDEX ix_region_asean_member ON countries (region, asean_member);
COMMENT ON INDEX ix_region_asean_member IS
    'Supports queries filtering by region and ASEAN membership, especially for combined lookups.';
CREATE INDEX ix_country_created_at ON countries (created_at)
    WHERE asean_member = true;
COMMENT ON INDEX ix_country_created_at IS
    'Efficient index for creation date queries limited to ASEAN members, reducing index size and maintenance overhead.';
CREATE INDEX ix_region_asean_member ON countries (region, asean_member);
COMMENT ON INDEX ix_region_asean_member IS
    'Supports queries filtering by region and ASEAN membership, especially for combined lookups.';
CREATE INDEX ix_country_created_at ON countries (created_at)
    WHERE asean_member = true;
COMMENT ON INDEX ix_country_created_at IS
    'Efficient index for creation date queries limited to ASEAN members, reducing index size and maintenance overhead.';

CREATE OR REPLACE TRIGGER tg_country_updated
    BEFORE UPDATE ON country
    FOR EACH ROW
    EXECUTE FUNCTION update_tg();