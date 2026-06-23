from sqlalchemy import Index

from mdls.core import Event

ix_location_id_event_date: Index = Index(
    'ix_location_id_event_date', 
    Event.__table__.c.location_id, 
    Event.__table__.c.event_date, 
    comment='Composite for geospatial-temporal queries filtering events by location within a date range.'
)

ix_event_type_id: Index = Index(
    'ix_event_type_id', 
    Event.__table__.c.event_type_id,
    comment='Speeds up lookups by event type ID, used for filtering events by their dedicated type.'
)

ix_event_type_id_event_date: Index = Index(
    'ix_event_type_id_event_date',
    Event.__table__.c.event_type_id, 
    Event.__table__.c.event_date,
    comment='Supports filtering by event type combined with date range, common for dashboard queries.'
)

ix_event_date_range: Index = Index(
    'ix_event_date_range',
    Event.__table__.c.event_date,
    Event.__table__.c.event_end_date,
    postgresql_where=Event.__table__.c.event_end_date.isnot(None),
    comment='Partial composite for temporal range queries on extended-duration events only.'
)

ix_attribution_confidence_event_date: Index = Index(
    'ix_attribution_confidence_event_date',
    Event.__table__.c.attribution_confidence,
    Event.__table__.c.event_date,
    postgresql_where=(
        Event.__table__.c.attribution_confidence != 'Confirmed'
    ),
    comment='Partial index for non-default attribution confidence values and event date.'
)

ix_event_created_at: Index = Index(
    'ix_event_created_at',
    Event.__table__.c.created_at,
    comment='Supports time-based queries such as sorting or filtering events by creation date.'
)