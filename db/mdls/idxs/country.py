from sqlalchemy import Index

from mdls.core import Country

ix_region_asean_member: Index = Index(
    'ix_region_asean_member',
    Country.__table__.c.region,
    Country.__table__.c.asean_member,
    comment='Supports queries filtering by region and ASEAN membership, especially for combined lookups.'
)

ix_country_created_at: Index = Index(
    'ix_country_created_at',
    Country.__table__.c.created_at,
    postgresql_where=(Country.__table__.c.asean_member == True),
    comment='Efficient index for creation date queries limited to ASEAN members, reducing index size and maintenance overhead.'
)