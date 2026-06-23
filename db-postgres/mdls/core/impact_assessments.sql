CREATE TABLE impact_assessment (
    id                INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid              UUID NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    notes             TEXT NULL,
    event_id                  INTEGER NOT NULL,
    strategic_significance    strategic_significance_enum NULL,
    casualties_killed         INTEGER NULL,
    casualties_wounded        INTEGER NULL,
    displaced_persons         INTEGER NULL,
    economic_impact_usd       NUMERIC(15, 2) NULL,
    political_impact          political_impact_enum NULL,
    legal_precedent           legal_precedent_enum NULL,

    CONSTRAINT fk_impact_assessment_event
        FOREIGN KEY (event_id)
        REFERENCES event (id)
        ON DELETE CASCADE,
    CONSTRAINT uq_impact_assessment_event_id UNIQUE (event_id),
    CONSTRAINT ck_impact_assessments_positive_or_null
        CHECK (
            (casualties_killed IS NULL OR casualties_killed >= 0) AND
            (casualties_wounded IS NULL OR casualties_wounded >= 0) AND
            (displaced_persons IS NULL OR displaced_persons >= 0) AND
            (economic_impact_usd IS NULL OR economic_impact_usd >= 0)
        ),
    CONSTRAINT ck_impact_assessments_fields_non_empty
        CHECK (notes IS NULL OR TRIM(notes) != '')
);

COMMENT ON TABLE impact_assessment IS 'Models consequences and significance of incidents across multiple dimensions.';

COMMENT ON COLUMN impact_assessment.id                     IS 'Integer primary key (from IdMixin).';
COMMENT ON COLUMN impact_assessment.uuid                   IS 'Universally unique identifier (from UUIDMixin).';
COMMENT ON COLUMN impact_assessment.created_at             IS 'Timestamp of row creation (from TimestampMixin).';
COMMENT ON COLUMN impact_assessment.updated_at             IS 'Timestamp of last update (from TimestampMixin).';
COMMENT ON COLUMN impact_assessment.notes                  IS 'Additional context, methodology notes, or uncertainty explanations.';
COMMENT ON COLUMN impact_assessment.event_id               IS 'FOREIGN KEY to events table. Must not be NULL.';
COMMENT ON COLUMN impact_assessment.strategic_significance IS 'Strategic importance level (Low, Medium, High, Critical). Nullable if indeterminate.';
COMMENT ON COLUMN impact_assessment.casualties_killed      IS 'Count of fatalities. Nullable if not applicable.';
COMMENT ON COLUMN impact_assessment.casualties_wounded     IS 'Count of injured persons. Nullable if not applicable.';
COMMENT ON COLUMN impact_assessment.displaced_persons      IS 'Count of displaced persons. Nullable if not applicable.';
COMMENT ON COLUMN impact_assessment.economic_impact_usd    IS 'Economic impact in USD. Nullable if not applicable.';
COMMENT ON COLUMN impact_assessment.political_impact       IS 'Assessment of diplomatic relationship consequences (Improved, Stable, Deteriorated, Ruptured). Nullable if not applicable.';
COMMENT ON COLUMN impact_assessment.legal_precedent        IS 'Assessment of implications for international legal norms (Affirming, Neutral, Testing, Violating). Nullable if not applicable.';

CREATE INDEX ix_strategic_significance_created_at ON impact_assessments (strategic_significance, created_at)
    WHERE strategic_significance IS NOT NULL;
COMMENT ON INDEX ix_strategic_significance_created_at IS
    'Partial index excluding NULL strategic_significance for improved selectivity.';
CREATE INDEX ix_political_impact_created_at ON impact_assessments (political_impact, created_at)
    WHERE political_impact IS NOT NULL;
COMMENT ON INDEX ix_political_impact_created_at IS
    'Partial index excluding NULL political_impact for improved selectivity.';
CREATE INDEX ix_legal_precedent_created_at ON impact_assessments (legal_precedent, created_at)
    WHERE legal_precedent IS NOT NULL;
COMMENT ON INDEX ix_legal_precedent_created_at IS
    'Partial index excluding NULL legal_precedent for improved selectivity.';
CREATE INDEX ix_strategic_significance_economic_impact_usd ON impact_assessments (strategic_significance, economic_impact_usd)
    WHERE economic_impact_usd IS NOT NULL;
COMMENT ON INDEX ix_strategic_significance_economic_impact_usd IS
    'Partial index to accelerate queries combining strategic significance with non‑null economic impact.';
CREATE INDEX ix_casualties_killed ON impact_assessments (casualties_killed)
    WHERE casualties_killed IS NOT NULL;
COMMENT ON INDEX ix_casualties_killed IS
    'Partial index for efficient filtering on non‑null killed casualty counts.';
CREATE INDEX ix_casualties_wounded ON impact_assessments (casualties_wounded)
    WHERE casualties_wounded IS NOT NULL;
COMMENT ON INDEX ix_casualties_wounded IS
    'Partial index for efficient filtering on non‑null wounded casualty counts.';
CREATE INDEX ix_displaced_persons ON impact_assessments (displaced_persons)
    WHERE displaced_persons IS NOT NULL;
COMMENT ON INDEX ix_displaced_persons IS
    'Partial index for efficient filtering on non‑null displaced persons counts.';

CREATE OR REPLACE TRIGGER tg_impact_assessment_updated
    BEFORE UPDATE ON impact_assessment
    FOR EACH ROW
    EXECUTE FUNCTION update_tg();