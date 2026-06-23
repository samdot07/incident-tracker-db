CREATE TABLE event_actor (
    event_id          INTEGER NOT NULL,
    actor_id          INTEGER NOT NULL,
    actor_role                actor_role_enum NOT NULL,
    attribution_confidence    attribution_confidence_enum NOT NULL DEFAULT 'confirmed',
    notes             TEXT NULL,

    CONSTRAINT fk_event_actor_event
        FOREIGN KEY (event_id)
        REFERENCES event (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_event_actor_actor
        FOREIGN KEY (actor_id)
        REFERENCES actor (id)
        ON DELETE CASCADE,
    CONSTRAINT pk_event_actors
        PRIMARY KEY (event_id, actor_id),
    CONSTRAINT ck_event_actor_fields_non_empty
        CHECK (notes IS NULL OR TRIM(notes) != '')
);

COMMENT ON TABLE event_actor IS 'Junction table linking events to participating organizational actors';

COMMENT ON COLUMN event_actor.event_id               IS 'FOREIGN KEY referencing events table.';
COMMENT ON COLUMN event_actor.actor_id               IS 'FOREIGN KEY referencing actors table.';
COMMENT ON COLUMN event_actor.actor_role             IS 'Role played in incident (Initiator, Responder, Target, Participant, Claimant, Observer). Useful for action-reaction analysis.';
COMMENT ON COLUMN event_actor.attribution_confidence IS 'Confidence level for actor attribution (Confirmed, Suspected, Third-Party, Contested). Defaults to Confirmed.';
COMMENT ON COLUMN event_actor.notes                  IS 'Additional remarks about the actor''s specific role or the evidence supporting the attribution.';

CREATE INDEX ix_event_actors_actor_id ON event_actors (actor_id);
COMMENT ON INDEX ix_event_actors_actor_id IS
    'Optimizes queries filtering by actor_id.';
CREATE INDEX ix_event_actors_actor_role ON event_actors (actor_id, actor_role);
COMMENT ON INDEX ix_event_actors_actor_role IS
    'Composite for queries filtering actor events by role (e.g., all Initiator events for a given actor).';
CREATE INDEX ix_event_actors_actor_id_attribution_confidence ON event_actors (actor_id, attribution_confidence);
COMMENT ON INDEX ix_event_actors_actor_id_attribution_confidence IS
    'Composite for filtering actor event associations by attribution confidence level.';