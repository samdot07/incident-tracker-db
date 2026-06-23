from sqlalchemy import Index

from mdls.core import Source

ix_source_created_at: Index = Index(
    'ix_source_created_at',
    Source.__table__.c.created_at,
    comment='Supports time-based queries such as sorting or filtering sources by creation date.'
)

ix_publisher_non_default: Index = Index(
    'ix_publisher_non_default',
    Source.__table__.c.publisher,
    postgresql_where=(Source.__table__.c.publisher != 'Unknown'),
    comment='Partial B-tree for publisher lookups excluding the Unknown default, where cardinality is sufficient for index use.'
)

ix_source_type_publication_date: Index = Index(
    'ix_source_type_publication_date',
    Source.__table__.c.source_type,
    Source.__table__.c.publication_date,
    comment='Composite B-tree index to optimize queries filtering by Source_Type and sorting by Publication_Date.'
)

ix_source_type_created_at: Index = Index(
    'ix_source_type_created_at',
    Source.__table__.c.source_type,
    Source.__table__.c.created_at,
    comment='Composite B-tree index to optimize queries filtering by Source_Type and sorting by Created_At.'
)

ix_author_gin: Index = Index(
    'ix_author_gin',
    Source.__table__.c.author,
    postgresql_using='gin',
    postgresql_ops={'author': 'gin_trgm_ops'},
    comment='GIN trigram index enabling fast fuzzy and partial text searches on Author.'
)

ix_source_title_gin: Index = Index(
    'ix_source_title_gin',
    Source.__table__.c.source_title,
    postgresql_using='gin',
    postgresql_ops={'source_title': 'gin_trgm_ops'},
    comment='GIN trigram index enabling fast fuzzy and partial text searches on Source_Title.'
)

ix_url_non_null: Index = Index(
    'ix_url_non_null',
    Source.__table__.c.url,
    unique=True,
    postgresql_where=Source.__table__.c.url.isnot(None),
    comment='Partial unique index, only enforce uniqueness when url IS NOT NULL.'
)