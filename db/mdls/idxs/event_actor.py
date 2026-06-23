from sqlalchemy import Index

from mdls.core import EventActor

ix_event_actors_actor_id: Index = Index(
    'ix_event_actors_actor_id',
    EventActor.__table__.c.actor_id,
    comment='Optimizes queries filtering by actor_id.'
)

ix_event_actors_actor_role: Index = Index(
    'ix_event_actors_actor_role',
    EventActor.__table__.c.actor_id,
    EventActor.__table__.c.actor_role,
    comment='Composite for queries filtering actor events by role (e.g., all Initiator events for a given actor).'
)

ix_event_actors_actor_id_attribution_confidence: Index = Index(
    'ix_event_actors_actor_id_attribution_confidence',
    EventActor.__table__.c.actor_id,
    EventActor.__table__.c.attribution_confidence,
    comment='Composite for filtering actor event associations by attribution confidence level.'
)