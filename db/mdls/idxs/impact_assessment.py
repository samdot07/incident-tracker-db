from sqlalchemy import Index

from mdls.core import ImpactAssessment

ix_strategic_significance_created_at: Index = Index(
    'ix_strategic_significance_created_at',
    ImpactAssessment.__table__.c.strategic_significance,
    ImpactAssessment.__table__.c.created_at,
    postgresql_where=ImpactAssessment.__table__.c.strategic_significance.isnot(None),
    comment='Partial index excluding NULL strategic_significance for improved selectivity.'
)

ix_political_impact_created_at: Index = Index(
    'ix_political_impact_created_at',
    ImpactAssessment.__table__.c.political_impact,
    ImpactAssessment.__table__.c.created_at,
    postgresql_where=ImpactAssessment.__table__.c.political_impact.isnot(None),
    comment='Partial index excluding NULL political_impact for improved selectivity.'
)

ix_legal_precedent_created_at: Index = Index(
    'ix_legal_precedent_created_at',
    ImpactAssessment.__table__.c.legal_precedent,
    ImpactAssessment.__table__.c.created_at,
    postgresql_where=ImpactAssessment.__table__.c.legal_precedent.isnot(None),
    comment='Partial index excluding NULL legal_precedent for improved selectivity.'
)

ix_strategic_significance_economic_impact_usd: Index = Index(
    'ix_strategic_significance_economic_impact_usd',
    ImpactAssessment.__table__.c.strategic_significance,
    ImpactAssessment.__table__.c.economic_impact_usd,
    postgresql_where=ImpactAssessment.__table__.c.economic_impact_usd.isnot(None),
    comment='Partial index to accelerate queries combining strategic significance with non‑null economic impact.'
)

ix_casualties_killed: Index = Index(
    'ix_casualties_killed',
    ImpactAssessment.__table__.c.casualties_killed,
    postgresql_where=ImpactAssessment.__table__.c.casualties_killed.isnot(None),
    comment='Partial index for efficient filtering on non‑null killed casualty counts.'
)

ix_casualties_wounded: Index = Index(
    'ix_casualties_wounded',
    ImpactAssessment.__table__.c.casualties_wounded,
    postgresql_where=ImpactAssessment.__table__.c.casualties_wounded.isnot(None),
    comment='Partial index for efficient filtering on non‑null wounded casualty counts.'
)

ix_displaced_persons: Index = Index(
    'ix_displaced_persons',
    ImpactAssessment.__table__.c.displaced_persons,
    postgresql_where=ImpactAssessment.__table__.c.displaced_persons.isnot(None),
    comment='Partial index for efficient filtering on non‑null displaced persons counts.'
)
