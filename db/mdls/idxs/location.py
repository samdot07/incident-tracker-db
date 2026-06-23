from sqlalchemy import Index, func

from mdls.core import Location

ix_location_type: Index = Index(
    'ix_location_type',
    Location.__table__.c.location_type,
    comment='Speeds up queries filtering by location type, e.g., WHERE Location_Type = "Disputed Island".'
)

ix_country_id_location_type: Index = Index(
    'ix_country_id_location_type',
    Location.__table__.c.country_id,
    Location.__table__.c.location_type,
    comment='Composite index for queries filtering by both country and location type, avoiding multiple index scans.'
)

ix_country_id_created_at: Index = Index(
    'ix_country_id_created_at',
    Location.__table__.c.country_id,
    Location.__table__.c.created_at,
    comment='Optimizes queries that filter by country and order by creation date, supporting efficient pagination.'
)

ix_location_created_at: Index = Index(
    'ix_location_created_at',
    Location.__table__.c.created_at,
    comment='Supports time-based queries such as sorting or filtering location by creation date.'
)

ix_location_name: Index = Index(
    'ix_location_name',
    Location.__table__.c.location_name,
    comment='Supports exact match lookups on location name, often used in point queries or unique constraint checks.'
)

ix_coordinates: Index = Index(
    'ix_coordinates',
    Location.__table__.c.coordinates,
    postgresql_using='gist',
    comment='GiST index for spatial queries (distance, bounding box) on the coordinate column.'
)

ix_location_name_gin: Index = Index(
    'ix_location_name_gin',
    Location.__table__.c.location_name,
    postgresql_using='gin',
    postgresql_ops={'location_name': 'gin_trgm_ops'},
    comment='GIN trigram index enabling fast ILIKE and similarity searches on location names with wildcards.'
)

ix_location_name_lower: Index = Index(
    'ix_location_name_lower',
    func.lower(Location.__table__.c.location_name),
    comment='Functional index for case-insensitive equality searches, useful when normalized names are required.'
)

ix_location_unattributed: Index = Index(
    'ix_location_unattributed',
    Location.__table__.c.location_name,
    postgresql_where=(Location.__table__.c.country_id.is_(None)),
    comment='Partial index for lookups and audits of locations with no country attribution (disputed territories, international waters).'
)