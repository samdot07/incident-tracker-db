from sqlalchemy import Index

from mdls.core import CountryEvent

ix_country_events_country_id: Index = Index(
    'ix_country_events_country_id',
    CountryEvent.__table__.c.country_id,
    comment='Supports efficient lookups and joins on country_id.'
)

ix_country_events_involvement_type: Index = Index(
    'ix_country_events_involvement_type',
    CountryEvent.__table__.c.country_id,
    CountryEvent.__table__.c.involvement_type,
    comment='Composite for role-filtered country lookups (e.g., all events where country was Target).'
)