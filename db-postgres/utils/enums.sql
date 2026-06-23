CREATE TYPE actor_type AS ENUM (
    'GOVERNMENT',
    'REBEL_GROUP',
    'CORPORATE',
    'NGO',
    'OTHER'
);

CREATE TYPE region AS ENUM (
    'MAINLAND_SE_ASIA',
    'MARITIME_SE_ASIA',
    'EAST_ASIA',
    'SOUTH_ASIA',
    'OCEANIA',
    'NORTH_AMERICA',
    'EUROPE',
    'OTHER'
);

CREATE TYPE event_type_enum AS ENUM (
    'CYBER_ATTACK',
    'MALWARE',
    'FRAUD',
    'PHYSICAL_ATTACK',
    'NATURAL_DISASTER',
    'OTHER'
);

CREATE TYPE attribution_confidence AS ENUM (
    'CONFIRMED',
    'LIKELY',
    'POSSIBLE',
    'UNLIKELY',
    'UNKOWN'
);

CREATE TYPE strategic_significance AS ENUM (
    'LOW',
    'MEDIUM',
    'HIGH',
    'CRITICAL'
);

CREATE TYPE political_impact AS ENUM (
    'IMPROVED',
    'STABLE',
    'DETERIORATED',
    'RUPTURED'
);

CREATE TYPE legal_precedent AS ENUM (
    'AFFIRMING',
    'NEUTRAL',
    'TESTING',
    'VIOLATING'
);

CREATE TYPE location_type AS ENUM (
    'DISPUTED_ISLAND',
    'MARITIME_FEATURE',
    'BORDER_REGION',
    'CAPITAL_CITY',
    'MILITARY_INSTALLATION',
    'ECONOMIC_ZONE',
    'INTERNATIONAL_WATERS',
    'OTHER'
);

CREATE TYPE source_type AS ENUM (
    'NEWS_ARTICLE',
    'GOVERNMENT_REPORT',
    'ACADEMIC_PAPER',
    'BLOG_POST',
    'INTERVIEW',
    'DATASET',
    'OTHER'
);

CREATE TYPE involvement_type AS ENUM (
    'VICTIM',
    'PERPETRATOR',
    'AFFECTED_TERRITORY',
    'OBSERVER',
    'OTHER'
);

CREATE TYPE actor_role AS ENUM (
    'INITIATOR',
    'RESPONDER',
    'TARGET',
    'PARTICIPANT',
    'CLAIMANT',
    'OBSERVER'
);