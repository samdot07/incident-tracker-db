from sqlalchemy import Index

from mdls.core import Actor

ix_actor_country_id: Index = Index(
    'ix_actor_country_id',
    Actor.__table__.c.country_id,
    comment='Speeds up lookups by country ID, commonly used for filtering actors by their country of origin.'
)

ix_parent_actor_id: Index = Index(
    'ix_parent_actor_id',
    Actor.__table__.c.parent_actor_id,
    comment='Optimizes queries that navigate hierarchical relationships between actors (e.g., parent-child associations).'
)

ix_actor_created_at: Index = Index(
    'ix_actor_created_at',
    Actor.__table__.c.created_at,
    comment='Supports time-based queries such as sorting or filtering actors by creation date.'
)

ix_actor_type_country_id: Index = Index(
    'ix_actor_type_country_id',
    Actor.__table__.c.actor_type,
    Actor.__table__.c.country_id,
    comment='Efficiently serves queries filtering by actor type and country together, often used in reports or category filters.'
)

ix_actor_type_created_at: Index = Index(
    'ix_actor_type_created_at',
    Actor.__table__.c.actor_type,
    Actor.__table__.c.created_at,
    comment='Optimizes queries that combine actor type with creation date, such as listing actors of a specific type ordered by creation time.'
)
