from sqlalchemy import Index

from mdls.core import EventSource

ix_event_sources_source_id: Index = Index(
    'ix_event_sources_source_id',
    EventSource.__table__.c.source_id,
    comment='Optimizes lookups by source_id.'
)