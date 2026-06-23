from sqlalchemy import Index

from mdls.core import EventType

ix_parent_type_id: Index = Index(
    'ix_parent_type_id',
    EventType.__table__.c.parent_type_id,
    comment='Optimizes lookups for events by parent type, commonly used in hierarchical queries and foreign key joins.'
)

ix_event_type_created_at: Index = Index(
    'ix_event_type_created_at',
    EventType.__table__.c.created_at,
    comment='Supports time-based queries such as sorting or filtering event types by creation date.'
)