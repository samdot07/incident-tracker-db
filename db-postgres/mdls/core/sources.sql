CREATE TABLE source (
    id                INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid              UUID NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    notes             TEXT NULL,
    source_title      VARCHAR(500) NOT NULL,
    author            VARCHAR(200) NULL,
    publication_date  DATE NULL,
    url               VARCHAR(2048) NULL,
    source_type       source_type_enum NOT NULL,
    publisher         VARCHAR(200) NOT NULL DEFAULT 'Unknown',

    CONSTRAINT ck_sources_valid_publication_date
        CHECK (publication_date <= CURRENT_DATE),
    CONSTRAINT ck_sources_fields_non_empty
        CHECK (
            TRIM(source_title) != ''
            AND (author IS NULL OR TRIM(author) != '')
            AND TRIM(publisher) != ''
            AND (notes IS NULL OR TRIM(notes) != '')
        ),
    CONSTRAINT ck_sources_valid_url
        CHECK (url IS NULL OR url ~ '^https?://[^/\s]+')
);

COMMENT ON TABLE source IS 'Documents sources used for incident coding to enable validation via triangulation and protect intellectual property through attribution.';

COMMENT ON COLUMN source.id                IS 'Integer primary key (from IdMixin).';
COMMENT ON COLUMN source.uuid              IS 'Universally unique identifier (from UUIDMixin).';
COMMENT ON COLUMN source.created_at        IS 'Timestamp of row creation (from TimestampMixin).';
COMMENT ON COLUMN source.updated_at        IS 'Timestamp of last update (from TimestampMixin).';
COMMENT ON COLUMN source.notes             IS 'Additional remarks (e.g. translation notes, access date for URLs).';
COMMENT ON COLUMN source.source_title      IS 'Publication or document title.';
COMMENT ON COLUMN source.author            IS 'Individual author or organizational publisher.';
COMMENT ON COLUMN source.publication_date  IS 'When the source was published. Nullable for undated materials.';
COMMENT ON COLUMN source.url               IS 'Web location for online sources. Nullable for offline materials.';
COMMENT ON COLUMN source.source_type       IS 'Source classification for assessing reliability and formatting citations.';
COMMENT ON COLUMN source.publisher         IS 'Who the source was published by. Defaults to Unknown.';

CREATE INDEX ix_source_created_at ON sources (created_at);
COMMENT ON INDEX ix_source_created_at IS
    'Supports time-based queries such as sorting or filtering sources by creation date.';
CREATE INDEX ix_publisher_non_default ON sources (publisher)
    WHERE publisher != 'Unknown';
COMMENT ON INDEX ix_publisher_non_default IS
    'Partial B-tree for publisher lookups excluding the Unknown default, where cardinality is sufficient for index use.';
CREATE INDEX ix_source_type_publication_date ON sources (source_type, publication_date);
COMMENT ON INDEX ix_source_type_publication_date IS
    'Composite B-tree index to optimize queries filtering by Source_Type and sorting by Publication_Date.';
CREATE INDEX ix_source_type_created_at ON sources (source_type, created_at);
COMMENT ON INDEX ix_source_type_created_at IS
    'Composite B-tree index to optimize queries filtering by Source_Type and sorting by Created_At.';
CREATE INDEX ix_author_gin ON sources USING GIN (author gin_trgm_ops);
COMMENT ON INDEX ix_author_gin IS
    'GIN trigram index enabling fast fuzzy and partial text searches on Author.';
CREATE INDEX ix_source_title_gin ON sources USING GIN (source_title gin_trgm_ops);
COMMENT ON INDEX ix_source_title_gin IS
    'GIN trigram index enabling fast fuzzy and partial text searches on Source_Title.';
CREATE UNIQUE INDEX ix_url_non_null ON sources (url)
    WHERE url IS NOT NULL;
COMMENT ON INDEX ix_url_non_null IS
    'Partial unique index, only enforce uniqueness when url IS NOT NULL.';

CREATE OR REPLACE TRIGGER tg_source_updated
    BEFORE UPDATE ON source
    FOR EACH ROW
    EXECUTE FUNCTION update_tg();