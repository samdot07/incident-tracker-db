"""inital

Revision ID: 76c2c381f2fe
Revises:
Create Date: 2026-06-17 14:01:20.703571+00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import geoalchemy2

revision = "76c2c381f2fe"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "countries",
        sa.Column(
            "country_name",
            sa.String(length=100),
            nullable=False,
            comment="Official name of the country. Must be UNIQUE.",
        ),
        sa.Column(
            "iso_alpha_2",
            sa.String(length=2),
            nullable=False,
            comment="ISO 3166-1 alpha-2 country code. UNIQUE.",
        ),
        sa.Column(
            "iso_alpha_3",
            sa.String(length=3),
            nullable=False,
            comment="ISO 3166-1 alpha-3 country code. UNIQUE.",
        ),
        sa.Column(
            "region",
            postgresql.ENUM(
                "mainland_south_eastern_asia",
                "maritime_south_eastern_asia",
                "eastern_asia",
                "southern_asia",
                "central_asia",
                "western_asia",
                "northern_africa",
                "eastern_africa",
                "middle_africa",
                "southern_africa",
                "western_africa",
                "caribbean",
                "central_america",
                "south_america",
                "northern_america",
                "eastern_europe",
                "northern_europe",
                "southern_europe",
                "western_europe",
                "australia_and_new_zealand",
                "melanesia",
                "micronesia",
                "polynesia",
                "other",
                name="region",
                schema="geopolitical_tracker",
                create_type=False
            ),
            nullable=False,
            comment="Geographic region for grouping data (Mainland Southeast Asia, Maritime Southeast Asia, East Asia, South Asia, Oceania, North America, Europe, Other).",
        ),
        sa.Column(
            "asean_member",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
            comment="BOOLEAN flag indicating ASEAN membership status.",
        ),
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=True, start=1, increment=1),
            nullable=False,
            comment="Auto-incrementing PRIMARY KEY.",
        ),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
            comment="Supplementary observations. Nullable.",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="TIMESTAMP when the record was created (automatically set).",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="TIMESTAMP of the most recent update (set by TRIGGER). Initially set to creation time; updated by trigger on every subsequent modification.",
        ),
        sa.CheckConstraint(
            "TRIM(country_name) != '' AND (notes IS NULL OR TRIM(notes) != '')",
            name=op.f("ck_countries_ck_countries_fields_non_empty"),
        ),
        sa.CheckConstraint(
            "LENGTH(iso_alpha_2) = 2 AND LENGTH(iso_alpha_3) = 3",
            name=op.f("ck_countries_ck_countries_iso_length"),
        ),
        sa.CheckConstraint(
            "iso_alpha_2 = UPPER(iso_alpha_2) AND iso_alpha_3 = UPPER(iso_alpha_3)",
            name=op.f("ck_countries_ck_countries_iso_upper_case"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_countries")),
        sa.UniqueConstraint("country_name", name=op.f("uq_countries_country_name")),
        sa.UniqueConstraint("iso_alpha_2", name=op.f("uq_countries_iso_alpha_2")),
        sa.UniqueConstraint("iso_alpha_3", name=op.f("uq_countries_iso_alpha_3")),
        sa.UniqueConstraint("uuid", name=op.f("uq_countries_uuid")),
        schema="geopolitical_tracker",
        comment="Stores country data for analysis, focusing on ASEAN members and their key dialogue partners.",
    )
    op.create_table(
        "event_types",
        sa.Column(
            "type_name",
            sa.String(length=100),
            nullable=False,
            comment="Category or subcategory name.",
        ),
        sa.Column(
            "parent_type_id",
            sa.Integer(),
            nullable=True,
            comment="Self-referential FOREIGN KEY implementing hierarchical taxonomy. NULL for primary categories, populated for subcategories.",
        ),
        sa.Column(
            "event_type",
            postgresql.ENUM(
                "high_level_summit",
                "ministerial_engagement",
                "diplomatic_signaling",
                "institutional_mechanism",
                "trade_agreement",
                "investment_and_financing",
                "economic_coercion",
                "supply_chain_initiative",
                "maritime_operations",
                "military_exercises",
                "defense_cooperation",
                "military_deployment",
                "armed_incident",
                "airspace_operations",
                name="event_type_enum",
                schema="geopolitical_tracker",
                create_type=False
            ),
            nullable=False,
            comment="Primary category from the fixed taxonomy.",
        ),
        sa.Column(
            "definition",
            sa.Text(),
            nullable=False,
            comment="Operational definition specifying scope, inclusion criteria, boundary conditions, and disambiguation from related categories.",
        ),
        sa.Column(
            "examples",
            sa.Text(),
            nullable=True,
            comment="Representative incidents exemplifying the category, supporting decisions for ambiguous cases.",
        ),
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=True, start=1, increment=1),
            nullable=False,
            comment="Auto-incrementing PRIMARY KEY.",
        ),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
            comment="Supplementary observations. Nullable.",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="TIMESTAMP when the record was created (automatically set).",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="TIMESTAMP of the most recent update (set by TRIGGER). Initially set to creation time; updated by trigger on every subsequent modification.",
        ),
        sa.CheckConstraint(
            "TRIM(type_name) != '' AND TRIM(definition) != '' AND (examples IS NULL OR TRIM(examples) != '') AND (notes IS NULL OR TRIM(notes) != '')",
            name=op.f("ck_event_types_ck_event_types_fields_non_empty"),
        ),
        sa.ForeignKeyConstraint(
            ["parent_type_id"],
            ["geopolitical_tracker.event_types.id"],
            name=op.f("fk_event_types_parent_type_id_event_types"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_event_types")),
        sa.UniqueConstraint(
            "type_name",
            "parent_type_id",
            name="uq_event_types_type_name_parent_type_id",
        ),
        sa.UniqueConstraint("uuid", name=op.f("uq_event_types_uuid")),
        schema="geopolitical_tracker",
        comment="Implements two-tier hierarchical taxonomy distinguishing primary categories from subcategories.",
    )
    op.create_table(
        "sources",
        sa.Column(
            "source_title",
            sa.String(length=500),
            nullable=False,
            comment="Publication or document title.",
        ),
        sa.Column(
            "author",
            sa.String(length=200),
            nullable=True,
            comment="Individual author or organizational publisher.",
        ),
        sa.Column(
            "publication_date",
            sa.Date(),
            nullable=True,
            comment="When the source was published. Nullable for undated materials.",
        ),
        sa.Column(
            "url",
            sa.String(length=2048),
            nullable=True,
            comment="Web location for online sources. Nullable for offline materials.",
        ),
        sa.Column(
            "source_type",
            postgresql.ENUM(
                "academic_dataset",
                "government_release",
                "think_tank_report",
                "news_article",
                "primary_document",
                "book",
                "academic_journal",
                "other",
                name="source_type",
                schema="geopolitical_tracker",
                create_type=False
            ),
            nullable=False,
            comment="Source classification for assessing reliability and formatting citations.",
        ),
        sa.Column(
            "publisher",
            sa.String(length=200),
            server_default="Unknown",
            nullable=False,
            comment="Who the source was published by. Defaults to Unknown.",
        ),
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=True, start=1, increment=1),
            nullable=False,
            comment="Auto-incrementing PRIMARY KEY.",
        ),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
            comment="Supplementary observations. Nullable.",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="TIMESTAMP when the record was created (automatically set).",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="TIMESTAMP of the most recent update (set by TRIGGER). Initially set to creation time; updated by trigger on every subsequent modification.",
        ),
        sa.CheckConstraint(
            "TRIM(source_title) != '' AND (author IS NULL OR TRIM(author) != '') AND TRIM(publisher) != '' AND (notes IS NULL OR TRIM(notes) != '')",
            name=op.f("ck_sources_ck_sources_fields_non_empty"),
        ),
        sa.CheckConstraint(
            "url IS NULL OR url ~ '^https?://[^/[:space:]]+'",
            name=op.f("ck_sources_ck_sources_valid_url"),
        ),
        sa.CheckConstraint(
            "publication_date <= CURRENT_DATE",
            name=op.f("ck_sources_ck_sources_valid_publication_date"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sources")),
        sa.UniqueConstraint("uuid", name=op.f("uq_sources_uuid")),
        schema="geopolitical_tracker",
        comment="Documents sources used for incident coding to enable validation via triangulation and protect intellectual property through attribution.",
    )
    op.create_table(
        "actors",
        sa.Column(
            "actor_name",
            sa.String(length=200),
            nullable=False,
            comment="Full organizational name potentially including hierarchical designations.",
        ),
        sa.Column(
            "actor_type",
            postgresql.ENUM(
                "state_military",
                "state_paramilitary",
                "government_civilian",
                "non_state_armed_group",
                "criminal_network",
                "private_security",
                "international_organization",
                "other",
                name="actor_type",
                schema="geopolitical_tracker",
                create_type=False
            ),
            nullable=False,
            comment="Categorical classification of actor type.",
        ),
        sa.Column(
            "country_id",
            sa.Integer(),
            nullable=True,
            comment="FOREIGN KEY to Countries table. Nullable if entities lack single national affiliation.",
        ),
        sa.Column(
            "parent_actor_id",
            sa.Integer(),
            nullable=True,
            comment="Self-referential FOREIGN KEY for modeling organizational hierarchies. NULL for top-level entities.",
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
            comment="Contextual details for analyst understanding and disambiguation.",
        ),
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=True, start=1, increment=1),
            nullable=False,
            comment="Auto-incrementing PRIMARY KEY.",
        ),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
            comment="Supplementary observations. Nullable.",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="TIMESTAMP when the record was created (automatically set).",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="TIMESTAMP of the most recent update (set by TRIGGER). Initially set to creation time; updated by trigger on every subsequent modification.",
        ),
        sa.CheckConstraint(
            "TRIM(actor_name) != '' AND (description IS NULL OR TRIM(description) != '') AND (notes IS NULL OR TRIM(notes) != '')",
            name=op.f("ck_actors_ck_actors_fields_non_empty"),
        ),
        sa.CheckConstraint(
            "parent_actor_id IS NULL OR parent_actor_id != id",
            name=op.f("ck_actors_ck_actors_no_self_reference"),
        ),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["geopolitical_tracker.countries.id"],
            name=op.f("fk_actors_country_id_countries"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["parent_actor_id"],
            ["geopolitical_tracker.actors.id"],
            name=op.f("fk_actors_parent_actor_id_actors"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_actors")),
        sa.UniqueConstraint(
            "actor_name", "country_id", name="uq_actors_actor_name_country_id"
        ),
        sa.UniqueConstraint("uuid", name=op.f("uq_actors_uuid")),
        schema="geopolitical_tracker",
        comment="Models specific organizational entities participating in incidents, distinguished from Countries which represent abstract nation-state units.",
    )
    op.create_table(
        "locations",
        sa.Column(
            "location_name",
            sa.String(length=200),
            nullable=False,
            comment="Geographic feature or area name.",
        ),
        sa.Column(
            "coordinates",
            geoalchemy2.types.Geography(
                geometry_type="POINT",
                srid=4326,
                dimension=2,
                from_text="ST_GeogFromText",
                name="geography",
            ),
            nullable=True,
            comment="PostGIS GEOGRAPHY point (lat/long in WGS84). Nullable for approximate/regional coordinates.",
        ),
        sa.Column(
            "location_type",
            postgresql.ENUM(
                "disputed_island",
                "maritime_feature",
                "border_region",
                "capital_city",
                "military_installation",
                "economic_zone",
                "international_waters",
                "other",
                name="location_type",
                schema="geopolitical_tracker",
                create_type=False
            ),
            nullable=False,
            comment="Classification for pattern analysis (Disputed Island, Maritime Feature, Border Region, Capital City, Military Installation, Economic Zone, International Waters, Other).",
        ),
        sa.Column(
            "country_id",
            sa.Integer(),
            nullable=True,
            comment="FOREIGN KEY to countries table. Nullable for disputed territories or international waters.",
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
            comment="Contextual details for analyst understanding and disambiguation.",
        ),
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=True, start=1, increment=1),
            nullable=False,
            comment="Auto-incrementing PRIMARY KEY.",
        ),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
            comment="Supplementary observations. Nullable.",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="TIMESTAMP when the record was created (automatically set).",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="TIMESTAMP of the most recent update (set by TRIGGER). Initially set to creation time; updated by trigger on every subsequent modification.",
        ),
        sa.CheckConstraint(
            "TRIM(location_name) != '' AND (description IS NULL OR TRIM(description) != '') AND (notes IS NULL OR TRIM(notes) != '')",
            name=op.f("ck_locations_ck_locations_fields_non_empty"),
        ),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["geopolitical_tracker.countries.id"],
            name=op.f("fk_locations_country_id_countries"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_locations")),
        sa.UniqueConstraint("uuid", name=op.f("uq_locations_uuid")),
        schema="geopolitical_tracker",
        comment="Models specific geographic points or areas where incidents occur.",
    )
    op.create_table(
        "events",
        sa.Column(
            "event_name",
            sa.String(length=100),
            nullable=False,
            comment="Full event name.",
        ),
        sa.Column(
            "event_date",
            sa.Date(),
            nullable=False,
            comment="Occurrence DATE of the incident (without time). Must not be NULL.",
        ),
        sa.Column(
            "event_end_date",
            sa.Date(),
            nullable=True,
            comment="End DATE for extended-duration events (optional). Must be on or after event_date.",
        ),
        sa.Column(
            "location_id",
            sa.Integer(),
            nullable=True,
            comment="FOREIGN KEY to locations table. Nullable if event lacks precise spatial attribution.",
        ),
        sa.Column(
            "event_type_id",
            sa.Integer(),
            nullable=False,
            comment="FOREIGN KEY to event_type table. Must not be NULL.",
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=False,
            comment="Narrative summary of the incident. Must not be NULL.",
        ),
        sa.Column(
            "attribution_confidence",
            postgresql.ENUM(
                "confirmed",
                "suspected",
                "third_party",
                "contested",
                name="attribution_confidence",
                schema="geopolitical_tracker",
                create_type=False
            ),
            server_default=sa.text("'confirmed'::attribution_confidence"),
            nullable=False,
            comment='Confidence level in actor attribution and factual accuracy. Defaults to "confirmed".',
        ),
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=True, start=1, increment=1),
            nullable=False,
            comment="Auto-incrementing PRIMARY KEY.",
        ),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
            comment="Supplementary observations. Nullable.",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="TIMESTAMP when the record was created (automatically set).",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="TIMESTAMP of the most recent update (set by TRIGGER). Initially set to creation time; updated by trigger on every subsequent modification.",
        ),
        sa.CheckConstraint(
            "TRIM(event_name) != '' AND TRIM(description) != '' AND (notes IS NULL OR TRIM(notes) != '')",
            name=op.f("ck_events_ck_events_fields_non_empty"),
        ),
        sa.CheckConstraint(
            "(event_end_date IS NULL) OR (event_end_date >= event_date)",
            name=op.f("ck_events_ck_events_valid_event_end_date"),
        ),
        sa.ForeignKeyConstraint(
            ["event_type_id"],
            ["geopolitical_tracker.event_types.id"],
            name=op.f("fk_events_event_type_id_event_types"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["location_id"],
            ["geopolitical_tracker.locations.id"],
            name=op.f("fk_events_location_id_locations"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_events")),
        sa.UniqueConstraint("uuid", name=op.f("uq_events_uuid")),
        schema="geopolitical_tracker",
        comment="Stores individual geopolitical incidents as the primary unit of analysis.",
    )
    op.create_table(
        "country_events",
        sa.Column(
            "event_id",
            sa.Integer(),
            nullable=False,
            comment="FOREIGN KEY referencing Events table.",
        ),
        sa.Column(
            "country_id",
            sa.Integer(),
            nullable=False,
            comment="FOREIGN KEY referencing Countries table.",
        ),
        sa.Column(
            "involvement_type",
            postgresql.ENUM(
                "primary_actor",
                "supporting_actor",
                "affected_party",
                "mediator",
                "observer",
                name="involvement_type",
                schema="geopolitical_tracker",
                native_enum=False,
                create_type=False
            ),
            nullable=False,
            comment="Nature of involvement. Must not be NULL",
        ),
        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
            comment="Supplementary observations. Nullable.",
        ),
        sa.CheckConstraint(
            "(notes IS NULL OR TRIM(notes) != '')",
            name=op.f("ck_country_events_ck_country_event_fields_non_empty"),
        ),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["geopolitical_tracker.countries.id"],
            name=op.f("fk_country_events_country_id_countries"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["geopolitical_tracker.events.id"],
            name=op.f("fk_country_events_event_id_events"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("event_id", "country_id", name="pk_country_events"),
        schema="geopolitical_tracker",
        comment="Junction table linking events to participating/affected countries",
    )
    op.create_table(
        "event_actors",
        sa.Column(
            "event_id",
            sa.Integer(),
            nullable=False,
            comment="FOREIGN KEY referencing events table.",
        ),
        sa.Column(
            "actor_id",
            sa.Integer(),
            nullable=False,
            comment="FOREIGN KEY referencing actors table.",
        ),
        sa.Column(
            "actor_role",
            postgresql.ENUM(
                "initiator",
                "responder",
                "target",
                "participant",
                "claimant",
                "observer",
                name="actor_role",
                schema="geopolitical_tracker",
                native_enum=False,
                create_type=False
            ),
            nullable=False,
            comment="Role played in incident (Initiator, Responder, Target, Participant, Claimant, Observer). Useful for action-reaction analysis.",
        ),
        sa.Column(
            "attribution_confidence",
            postgresql.ENUM(
                "confirmed",
                "suspected",
                "third_party",
                "contested",
                name="attribution_confidence",
                schema="geopolitical_tracker",
                create_type=False
            ),
            server_default=sa.text("'confirmed'::attribution_confidence"),
            nullable=False,
            comment="Confidence level for actor attribution (Confirmed, Suspected, Third-Party, Contested). Defaults to Confirmed.",
        ),
        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
            comment="Supplementary observations. Nullable.",
        ),
        sa.CheckConstraint(
            "(notes IS NULL OR TRIM(notes) != '')",
            name=op.f("ck_event_actors_ck_event_actor_fields_non_empty"),
        ),
        sa.ForeignKeyConstraint(
            ["actor_id"],
            ["geopolitical_tracker.actors.id"],
            name=op.f("fk_event_actors_actor_id_actors"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["geopolitical_tracker.events.id"],
            name=op.f("fk_event_actors_event_id_events"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("event_id", "actor_id", name="pk_event_actors"),
        schema="geopolitical_tracker",
        comment="Junction table linking events to participating organizational actors",
    )
    op.create_table(
        "event_sources",
        sa.Column(
            "event_id",
            sa.Integer(),
            nullable=False,
            comment="FOREIGN KEY referencing events table.",
        ),
        sa.Column(
            "source_id",
            sa.Integer(),
            nullable=False,
            comment="FOREIGN KEY referencing sources table.",
        ),
        sa.Column(
            "page_reference",
            sa.String(length=50),
            nullable=True,
            comment="Specific page numbers or section identifiers within source documents.",
        ),
        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
            comment="Supplementary observations. Nullable.",
        ),
        sa.CheckConstraint(
            "(notes IS NULL) OR (TRIM(notes) != '')",
            name=op.f("ck_event_sources_ck_event_source_fields_non_empty"),
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["geopolitical_tracker.events.id"],
            name=op.f("fk_event_sources_event_id_events"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["source_id"],
            ["geopolitical_tracker.sources.id"],
            name=op.f("fk_event_sources_source_id_sources"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("event_id", "source_id", name="pk_event_sources"),
        schema="geopolitical_tracker",
        comment="Junction table linking events to documentary sources with citation details.",
    )
    op.create_table(
        "impact_assessments",
        sa.Column(
            "event_id",
            sa.Integer(),
            nullable=False,
            comment="FOREIGN KEY to events table. Must not be NULL.",
        ),
        sa.Column(
            "strategic_significance",
            postgresql.ENUM(
                "low",
                "medium",
                "high",
                "critical",
                name="strategic_significance",
                schema="geopolitical_tracker",
                create_type=False
            ),
            nullable=True,
            comment="Strategic importance level (Low, Medium, High, Critical). Nullable if indeterminate.",
        ),
        sa.Column(
            "casualties_killed",
            sa.Integer(),
            nullable=True,
            comment="Count of fatalities. Nullable if not applicable.",
        ),
        sa.Column(
            "casualties_wounded",
            sa.Integer(),
            nullable=True,
            comment="Count of injured persons. Nullable if not applicable.",
        ),
        sa.Column(
            "displaced_persons",
            sa.Integer(),
            nullable=True,
            comment="Count of displaced persons. Nullable if not applicable.",
        ),
        sa.Column(
            "economic_impact_usd",
            sa.Numeric(precision=15, scale=2),
            nullable=True,
            comment="Economic impact in USD. Nullable if not applicable.",
        ),
        sa.Column(
            "political_impact",
            postgresql.ENUM(
                "improved",
                "stable",
                "deteriorated",
                "ruptured",
                name="political_impact",
                schema="geopolitical_tracker",
                create_type=False
            ),
            nullable=True,
            comment="Assessment of diplomatic relationship consequences (Improved, Stable, Deteriorated, Ruptured). Nullable if not applicable.",
        ),
        sa.Column(
            "legal_precedent",
            postgresql.ENUM(
                "affirming",
                "neutral",
                "testing",
                "violating",
                name="legal_precedent",
                schema="geopolitical_tracker",
                create_type=False
            ),
            nullable=True,
            comment="Assessment of implications for international legal norms (Affirming, Neutral, Testing, Violating). Nullable if not applicable.",
        ),
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=True, start=1, increment=1),
            nullable=False,
            comment="Auto-incrementing PRIMARY KEY.",
        ),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
            comment="Supplementary observations. Nullable.",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="TIMESTAMP when the record was created (automatically set).",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="TIMESTAMP of the most recent update (set by TRIGGER). Initially set to creation time; updated by trigger on every subsequent modification.",
        ),
        sa.CheckConstraint(
            "(notes IS NULL OR trim(notes) != '')",
            name=op.f("ck_impact_assessments_ck_impact_assessments_fields_non_empty"),
        ),
        sa.CheckConstraint(
            "(casualties_killed IS NULL OR casualties_killed >= 0) AND (casualties_wounded IS NULL OR casualties_wounded >= 0) AND (displaced_persons IS NULL OR displaced_persons >= 0) AND (economic_impact_usd IS NULL OR economic_impact_usd >= 0)",
            name=op.f("ck_impact_assessments_ck_impact_assessments_positive_or_null"),
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["geopolitical_tracker.events.id"],
            name=op.f("fk_impact_assessments_event_id_events"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_impact_assessments")),
        sa.UniqueConstraint("event_id", name=op.f("uq_impact_assessments_event_id")),
        sa.UniqueConstraint("uuid", name=op.f("uq_impact_assessments_uuid")),
        schema="geopolitical_tracker",
        comment="Models consequences and significance of incidents across multiple dimensions.",
    )

def downgrade() -> None:
    op.drop_table("impact_assessments", schema="geopolitical_tracker")
    op.drop_table("event_sources", schema="geopolitical_tracker")
    op.drop_table("event_actors", schema="geopolitical_tracker")
    op.drop_table("country_events", schema="geopolitical_tracker")
    op.drop_table("events", schema="geopolitical_tracker")
    op.drop_table("locations", schema="geopolitical_tracker")
    op.drop_table("actors", schema="geopolitical_tracker")
    op.drop_table("sources", schema="geopolitical_tracker")
    op.drop_table("event_types", schema="geopolitical_tracker")
    op.drop_table("countries", schema="geopolitical_tracker")
