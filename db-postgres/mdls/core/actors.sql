CREATE TABLE actor (
    id                  INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid                UUID NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    notes               TEXT NULL,
    actor_name          VARCHAR(200) NOT NULL,
    actor_type          actor_type_enum NOT NULL,
    country_id          INTEGER,
    parent_actor_id     INTEGER,
    description         TEXT,

    CONSTRAINT uq_actors_actor_name_country_id
        UNIQUE (actor_name, country_id),
    CONSTRAINT ck_actors_fields_non_empty
        CHECK (
            TRIM(actor_name) != ''
            AND (description IS NULL OR TRIM(description) != '')
            AND (notes IS NULL OR TRIM(notes) != '')
        ),
    CONSTRAINT ck_actors_no_self_reference
        CHECK (parent_actor_id IS NULL OR parent_actor_id != id),
    CONSTRAINT fk_actor_country
        FOREIGN KEY (country_id)
        REFERENCES country (id)
        ON DELETE SET NULL,
    CONSTRAINT fk_actor_parent
        FOREIGN KEY (parent_actor_id)
        REFERENCES actor (id)
        ON DELETE SET NULL
);

COMMENT ON TABLE actor IS
    'Models specific organizational entities participating in incidents, distinguished from Countries which represent abstract nation‑state units.';

COMMENT ON COLUMN actor.id                  IS 'Surrogate primary key.';
COMMENT ON COLUMN actor.uuid                IS 'Universally unique identifier for external references.';
COMMENT ON COLUMN actor.notes               IS 'Free‑form remarks from NotesMixin.';
COMMENT ON COLUMN actor.created_at          IS 'Timestamp when the record was created.';
COMMENT ON COLUMN actor.updated_at          IS 'Timestamp when the record was last updated.';
COMMENT ON COLUMN actor.actor_name          IS 'Full organizational name potentially including hierarchical designations.';
COMMENT ON COLUMN actor.actor_type          IS 'Categorical classification of actor type.';
COMMENT ON COLUMN actor.country_id          IS 'FOREIGN KEY to Countries table. Nullable if entities lack single national affiliation.';
COMMENT ON COLUMN actor.parent_actor_id     IS 'Self‑referential FOREIGN KEY for modeling organizational hierarchies. NULL for top‑level entities.';
COMMENT ON COLUMN actor.description         IS 'Contextual details for analyst understanding and disambiguation.';

CREATE INDEX ix_actor_country_id ON actors (country_id);
COMMENT ON INDEX ix_actor_country_id IS
    'Speeds up lookups by country ID, commonly used for filtering actors by their country of origin.';
CREATE INDEX ix_parent_actor_id ON actors (parent_actor_id);
COMMENT ON INDEX ix_parent_actor_id IS
    'Optimizes queries that navigate hierarchical relationships between actors (e.g., parent-child associations).';
CREATE INDEX ix_actor_created_at ON actors (created_at);
COMMENT ON INDEX ix_actor_created_at IS
    'Supports time-based queries such as sorting or filtering actors by creation date.';
CREATE INDEX ix_actor_type_country_id ON actors (actor_type, country_id);
COMMENT ON INDEX ix_actor_type_country_id IS
    'Efficiently serves queries filtering by actor type and country together, often used in reports or category filters.';
CREATE INDEX ix_actor_type_created_at ON actors (actor_type, created_at);
COMMENT ON INDEX ix_actor_type_created_at IS
    'Optimizes queries that combine actor type with creation date, such as listing actors of a specific type ordered by creation time.';

CREATE OR REPLACE TRIGGER tg_actor_updated
    BEFORE UPDATE ON actor
    FOR EACH ROW
    EXECUTE FUNCTION update_tg();