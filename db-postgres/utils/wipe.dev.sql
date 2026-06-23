DROP TRIGGER IF EXISTS tg_actor_updated ON actors;
DROP TRIGGER IF EXISTS tg_country_updated ON countries;
DROP TRIGGER IF EXISTS tg_event_type_updated ON event_types;
DROP TRIGGER IF EXISTS tg_event_updated ON events;
DROP TRIGGER IF EXISTS tg_impact_assessment_updated ON impact_assessments;
DROP TRIGGER IF EXISTS tg_location_updated ON locations;
DROP TRIGGER IF EXISTS tg_source_updated ON sources;

DROP FUNCTION IF EXISTS update_tg() CASCADE;

DROP SCHEMA IF EXISTS geopolitical_tracker CASCADE;