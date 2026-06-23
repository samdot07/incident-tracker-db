# ASEAN Geopolitical Events Tracker Database

## A Comprehensive PostgreSQL Database for ASEAN Security Incident Analysis

---

### 📌 Overview

This project implements a PostgreSQL database containing for ASEAN incidents from 2016 to the present. Designed for policy researchers, analysts, and students of international affairs, the database enables advanced analytical querying of diplomatic, economic, and military events across Southeast Asia.

**Primary Focus Areas:**
- South China Sea maritime tensions and militarization
- ASEAN diplomatic cohesion and institutional responses
- Economic statecraft and coercion in regional relations
- Myanmar crisis regional spillover effects
- U.S.-China strategic competition manifestations

---

### 🎯 Key Objectives

- **Comprehensive Coverage**: 1,000+ incidents spanning diplomatic engagement, economic statecraft, military operations, and security incidents
- **Multi-Dimensional Impact Assessment**: Quantifiable metrics (casualties, economic impact, displacement) combined with qualitative rubrics (political relationship impact, legal-normative implications, strategic significance)
- **Two-Tier Event Taxonomy**: 12-15 subcategories with operational definitions and anchoring examples
- **Actor Typology**: 8-10 actor categories with organizational scope definitions
- **Attribution Confidence Framework**: Four-level coding protocol (Confirmed, Suspected, Third-Party Attribution, Contested)
- **Spatial Analysis Capabilities**: PostGIS extension for geographic coordinates and distance calculations
- **Portfolio-Ready**: Complete documentation, query library, and visualization exports

---

### 📊 Database Schema

The database implements a normalized relational structure with:

| Core Tables | Junction/Supporting Tables | Specialized Tables |
|-------------|---------------------------|-------------------|
| Events | Event Actors | Impact Assessments |
| Countries | Country Events | Source Documentation |
| Actors | Location Events | (Materialized Views) |
| Event Types | | |
| Locations | | |

**Key Relationships:**
- Many-to-many between events and actors
- Many-to-many between events and countries (bilateral/multilateral tracking)
- One-to-many for impact assessments and source documentation

---

### 🗂️ Data Sources

The database should integrates data from trusted sources, such as:

**Academic/Structured Datasets:**
- Uppsala Conflict Data Program (UCDP) Georeferenced Event Dataset
- Armed Conflict Location & Event Data Project (ACLED)
- CSIS Asia Maritime Transparency Initiative (AMTI)

**Specialized Policy Sources:**
- RSIS Commentaries & Reports (Singapore)
- ISEAS-Yusof Ishak Institute Publications
- International Crisis Group Southeast Asia Briefings
- Asia Maritime Transparency Initiative Analyses
- Center for Strategic and International Studies (CSIS)
- Carnegie Endowment for International Peace
- The Diplomat, Jane's Defence Weekly, Defense News

---

### 🔍 Analytical Query Capabilities

**Foundational Queries:**
- Simple filtering and aggregation by event type, country, date
- Basic statistical summaries (frequencies, totals, averages)

**Intermediate Queries:**
- Multi-table joins linking events to actors and countries
- Subqueries for comparative analysis
- Conditional aggregations with CASE statements

**Example Analytical Questions the Database Can Answer:**
- Does South China Sea incident frequency accelerate or stabilize over time?
- Do ASEAN-China diplomatic engagements correlate with reduced subsequent incidents?
- Do economic coercion incidents predict military escalation?
- How does the Myanmar crisis generate cross-border spillover?

---

### 📁 Project Structure

```
db/                                      # Python app implementation
├── deps/                                # Dependecies dir
│   └── deps.py                          # Custom bulk insert function
├── mdls/                                # Database core dir
│   ├── base/                            # Base model dir
│   │   └── base.py                      # Declarative base and MixIns
│   ├── core/                            # Core models dir
│   │   ├── actor.py                     # Actor table definition
│   │   ├── country_event.py             # Country-Event junction table definition
│   │   ├── country.py                   # Country table definition
│   │   ├── event_actor.py               # Event-Actor junction table definition
│   │   ├── event_source.py              # Event-Source junction table definition
│   │   ├── event_type.py                # Event Type table definition
│   │   ├── event.py                     # Event table definition
│   │   ├── impact_assessment.py         # Impact Assessment table definition
│   │   ├── location.py                  # Location table definition
│   │   └── source.py                    # Source table definition
│   ├── funcs/                           # Fuctions dir
│   │   └── funcs.py                     # Functions definition
│   ├── idxs/                            # Indexes dir
│   │   ├── actor.py                     # Actor table indexes
│   │   ├── country_event.py             # Country-Event junction table indexes
│   │   ├── country.py                   # Country indexes
│   │   ├── event_actor.py               # Event-Actor junction table indexes
│   │   ├── event_source.py              # Event-Source junction table indexes
│   │   ├── event_type.py                # Event Type table indexes
│   │   ├── event.py                     # Event indexes
│   │   ├── impact_assessment.py         # Impact-Assessment indexes
│   │   ├── location.py                  # Location indexes
│   │   └── source.py                    # Source indexes
│   └── trgs/                            # Triggers dir
│       └── trgs.py                      # Triggers definition
├── migrs/                               # Alembic migrations dir
│   ├── enums/                           # Enums migration dir
│   │   └── enums.py                     # Enums migration definition
│   ├── funcs/                           # Functions migration dir
│   │   └── funcs.py                     # Funtions migration definition
│   ├── trgs/                            # Triggers migration dir
│   │   └── trgs.py                      # Triggers migration definition
│   ├── versions/                        # Alembic versions dir
│   │   └── 2026..._inital.py            # Autogenerated alembic revision
│   └── xts/                             # Extensions migration dir
│       └── xts.py                       # Extensions migration definition
├── src/                                 # Source dir
│   └── config/                          # App config dir
│       └── config.py                    # App config settings definition
├── utils/                               # Utilities dir
│   ├── enums/                           # Enums dir
│   │   ├── enums.py                     # Enums definition
│   │   └── registry.py                  # Enums registry
│   └── utils/                           # Utilities dir
│       ├── metadata.py                  # Metadata retrieval
│       ├── name.py                      # Names quoting
│       ├── sec.py                       # DSN security
│       └── utils.py                     # Custom insert
├── alembic.ini                          # Alembic migration configuration
├── main.py                              # Database deployment orchestrator
└── README.md                            # This file
```

```
db-postgres/
├── mdls/                                # Database core dir
│   ├── core/                            # Core models dir
│   │   ├── actor.sql                    # Actor table definition
│   │   ├── country_event.sql            # Country-Event junction table definition
│   │   ├── country.sql                  # Country table definition
│   │   ├── event_actor.sql              # Event-Actor junction table definition
│   │   ├── event_source.sql             # Event-Source junction table definition
│   │   ├── event_type.sql               # Event Type table definition
│   │   ├── event.sql                    # Event table definition
│   │   ├── impact_assessment.sql        # Impact Assessment table definition
│   │   ├── location.sql                 # Location table definition
│   │   └── source.sql                   # Source table definition
│   ├── funcs/                           # Fuctions dir
│   │   └── funcs.sql                    # Functions definition
│   └── schema/                          # Schema dir
│       └── schema.sql                   # Schema definition
└── utils/                               # Utilities dir
    ├── enums.sql                        # Enums definition
    ├── wipe.dev.sql                     # Database teardown and schema wipeout
    └── xts.sql                          # Extensions definition
```

```
docs/                                # App documentation
├── actor/                           # Actor documentation
│   ├── attr_confidence.yaml         # Attribution Confidence Protocols
│   ├── categories.yaml              # Actor Category Definitions
│   └── decision_tree.yaml           # Attribution Coding Decision Trees
├── impact_assessment/               # Impact assessment documentation
│   ├── economic.yaml                # Economic Impact Dimensions
│   ├── military.yaml                # Military Impact Dimensions
│   ├── normative.yaml               # Legal-Normative Impact Dimensions
│   ├── political.yaml               # Political Impact Dimensions
│   └── stratigic.yaml               # Strategic Significance Assessment
├── taxonomy/                        # Taxonomy documentation
│   ├── diplomatic.yaml              # Diplomatic Event Category
│   ├── economic.yaml                # Economic Event Category
│   └── military.yaml                # Military Event Category
└── coding_manual.md                 # Complete incident coding protocols
```

---

### 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Database Engine | PostgreSQL 14+ | Relational database management |
| Spatial Extension | PostGIS | Geographic coordinates and spatial analysis |
| Database management and query execution |
| Data Transformation | Python 3.10+ | SQLAlchemy + Alembic |
| Database Connectivity | psycopg2 | Python-PostgreSQL interface |
| Version Control | Git + GitHub | Code and documentation hosting |

---

### 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

| Document | Description |
|----------|-------------|
| [Attribution Confidence](docs/actor/attr_confidence.yaml) | Complete attribution confidence protocols definition, coded, categorized, with anchoring examples for consistent coding |
| [Categories](docs/actor/categories.yaml) | Complete actor categories definition, coded with anchoring examples for consistent coding |
| [Economic](docs/impact_assesment/economic.yaml) | Complete economic impact dimension definition, measurements and approaches, coding protocols, source standards, missing data handling |
| [Military](docs/impact_assesment/military.yaml) | Complete military impact dimension definition, measurements and approaches, coding protocols, source standards, missing data handling |
| [Normative](docs/impact_assesment/normative.yaml) | Complete normative impact dimension definition, indicators, coded with anchoring examples for consistent coding |
| [Political](docs/impact_assesment/political.yaml) | Complete political impact dimension definition, measurements and approaches, coding protocols, source standards, missing data handling |
| [Strategic](docs/impact_assesment/strategic.yaml) | Complete strategic impact dimension definition, measurements and approaches, coding protocols, source standards, missing data handling |
| [Diplomatic](docs/taxonomy/diplomatic.yaml) | Complete diplomatic event category taxonomy definitions, inclusion and exclusion criteria, boundary cases, with anchoring examples for consistent coding |
| [Economic](docs/taxonomy/economic.yaml) | Complete economic event category taxonomy definitions, inclusion and exclusion criteria, boundary cases, with anchoring examples for consistent coding |
| [Military](docs/taxonomy/military.yaml) | Complete military event category taxonomy definitions, inclusion and exclusion criteria, boundary cases, with anchoring examples for consistent coding |
| [Coding Manual](docs/coding_manual.md) | Complete taxonomic frameworks, operational definitions, decision trees, and anchoring examples for consistent incident coding |
---

### 🎓 Academic and Professional Alignment

This project is designed to demonstrate proficiency in:

- **Relational Database Design**: Normalization, entity-relationship modeling, constraint implementation
- **SQL/Python integration**: SQLAlchemy/PostgreSQL integration, Alembic migrations
- **Policy Research Methodology**: Systematic incident coding, source triangulation, analytical validation
- **Regional Security Analysis**: ASEAN political-security dynamics, great power competition, maritime disputes
- **Data-Driven Policy Analysis**: Translating raw incident data into actionable policy insights

---

### 🤝 Contributing

This is a personal portfolio project, but feedback and collaboration inquiries are welcome:

- **Issues**: Report bugs or suggest improvements via GitHub Issues
- **Suggestions**: Share ideas for additional analytical queries or data sources
- **Academic Use**: Contact for access to anonymized sample data

---

### 📞 Contact

**Author**: [Samuele Moio] 
**Email**: samuelemoio@icloud.com
**Purpose**: Portfolio project

---

### 📌 Quick Links

| Resource | Link |
|----------|------|
| PostgreSQL Documentation | [postgresql.org/docs](https://www.postgresql.org/docs/) |
| PostGIS Documentation | [postgis.net/docs](https://postgis.net/docs/) |
| SQLAlchemy Documentation | [docs.sqlalchemy.org/en](https://docs.sqlalchemy.org/en/20/) |
| Alembic Documentation | [alembic.sqlalchemy.org/en](https://alembic.sqlalchemy.org/en/latest/) |
