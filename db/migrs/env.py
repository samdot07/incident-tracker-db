from __future__ import annotations
import sys
import os
from pathlib import Path

_PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from sqlalchemy import Engine, engine_from_config, pool, MetaData
from alembic import context

import mdls.core
from mdls.base.base import Base 
from src.config.config import Settings, get_settings

config = context.config
_settings: Settings = get_settings()
db_url: str = os.getenv("ALEMBIC_DB_URL") or str(_settings.DB_URL)
config.set_main_option("sqlalchemy.url", str(db_url))

# Set the target metadata with the correct schema
target_metadata: MetaData = Base.metadata

def include_object(object, name, type_, reflected, compare_to) -> bool:
    """
    Filter callback for Alembic's autogenerate process, determining which
    database objects should be included in migration generation and comparison.

    This function is passed to `context.configure()` via the `include_object`
    parameter. It is called for every object (tables, indexes, constraints,
    etc.) that Alembic encounters during schema comparison or autogeneration.
    Returning `False` excludes the object from consideration; returning `True`
    includes it.

    Currently, this filter excludes the following objects:
        - The `alembic_version` table (which Alembic uses internally to track
          migration versions). This exclusion prevents the autogenerate from
          accidentally including it in user‑generated migrations.
        - The `spatial_ref_sys` table, which is created by the PostGIS
          extension. This table contains spatial reference system metadata and
          should not be managed by application migrations; it is maintained
          solely by the PostGIS extension.

    All other objects (application tables, indexes, constraints, etc.) are
    included, allowing Alembic to generate appropriate migration operations
    for them.

    Parameters:
        object: The SQLAlchemy schema object being evaluated (e.g., a `Table`,
            `Index`, `Sequence`).
        name (str): The name of the object.
        type_ (str): The type of the object (e.g., 'table', 'index',
            'foreign_key_constraint', 'column').
        reflected (bool): Indicates whether the object was reflected from the
            database rather than from the metadata.
        compare_to: The corresponding object from the other side of the
            comparison (metadata vs. database), if available.

    Returns:
        bool: `True` if the object should be included in migration generation
            or comparison; `False` if it should be ignored.

    Notes:
        - This filter is applied during both offline and online migration runs.
        - It is critical for avoiding conflicts with system‑owned objects like
          the alembic version table and spatial reference tables.
        - If additional system tables from other extensions need to be ignored,
          they should be added to this filter.
    """
    if type_ == "table" and name in "alembic_version":
        return False
    if type_ == "table" and name in "spatial_ref_sys":
        return False
    return True

def run_migrations_offline() -> None:
    """
    Execute database migrations in "offline" mode, generating SQL scripts
    without connecting to a live database.

    In offline mode, Alembic uses the `url` from the configuration to generate
    the necessary SQL statements for the migration, but does not actually
    apply them to a database. This is useful for:
        - Generating migration scripts for review or manual execution.
        - Environments where a direct database connection is not available
          (e.g., during deployment pipelines that produce SQL files).
        - Testing migration correctness without affecting a real database.

    The function configures the Alembic context with the following settings:
        - `include_schemas=True`: Enables cross‑schema dependency tracking.
        - `version_table_schema`: The specific schema where the Alembic version
          table should reside, taken from the application settings
          (`_settings.DB_SCHEMA`).
        - `url`: The database connection URL from the Alembic configuration.
        - `target_metadata`: The SQLAlchemy metadata that defines the desired
          schema state (from `Base.metadata`).
        - `literal_binds=True`: Forces SQLAlchemy to render literal values
          instead of using bound parameters, which is required for offline
          SQL generation.
        - `dialect_opts={"paramstyle": "named"}`: Ensures compatibility with
          the PostgreSQL dialect's parameter style.
        - `include_object`: The filter function to exclude system objects.
        - `compare_type=True` and `compare_server_default=True`: Enable
          detection of column type changes and server default changes during
          autogeneration (these are primarily useful during `revision --autogenerate`).

    After configuration, a transaction block is started and `run_migrations()`
    is called to generate and execute (or output) the migration operations.

    Raises:
        - This function does not explicitly raise exceptions, but any errors
          from `context.configure()` or `context.run_migrations()` will
          propagate upward.

    Notes:
        - Offline mode does not apply any changes to the database; it only
          produces SQL statements that can be captured via the Alembic output.
        - The `context.begin_transaction()` is used for compatibility, but in
          offline mode transactions are not actually committed.
        - This mode is selected automatically by Alembic based on the absence
          of a live connection (i.e., when `context.is_offline_mode()` is
          `True`).
    """
    schema: str = _settings.DB_SCHEMA
    context.configure(
        include_schemas=True,
        version_table_schema=schema,
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        compare_type=True,
        compare_server_default=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """
    Execute database migrations in "online" mode, applying changes directly to
    a live database using a SQLAlchemy engine.

    In online mode, Alembic connects to the database specified in the
    configuration and applies the migration operations within a transaction.
    This is the normal mode used during deployment or local development to
    actually update the schema.

    The function performs the following steps:
        1. Retrieves the configuration section from the Alembic ini file.
        2. Constructs a SQLAlchemy `Engine` using `engine_from_config()`,
           with the following settings:
            - `poolclass=pool.NullPool`: Disables connection pooling to avoid
              lingering connections after the migration completes.
            - `connect_args={"options": f"-c search_path={schema},public"}`:
              Sets the PostgreSQL `search_path` to include the application's
              target schema first, ensuring that all schema operations (e.g.,
              creating tables, functions) occur in the correct schema by default.
        3. Connects to the database and configures the Alembic context with:
            - `include_schemas=True`: Enables cross‑schema object tracking.
            - `version_table_schema`: The schema where the Alembic version
              table is stored (derived from `_settings.DB_SCHEMA`).
            - `connection`: The live database connection.
            - `target_metadata`: The application metadata (`Base.metadata`).
            - `include_object`: The filter function to skip system objects.
            - `compare_type=True` and `compare_server_default=True`: Enable
              detection of type changes and default changes during autogenerate.
        4. Starts a transaction with `context.begin_transaction()` and executes
           the migration operations via `context.run_migrations()`.
        5. Disposes of the engine to release connections.

    Raises:
        ValueError: If the Alembic configuration section cannot be found.
        RuntimeError: Propagated from `context.run_migrations()` if any
            migration fails.

    Notes:
        - The `search_path` setting is crucial for ensuring that all DDL
          statements (CREATE TABLE, ALTER TABLE, etc.) are executed in the
          intended schema, especially when tables reference each other across
          schemas.
        - Using `NullPool` prevents connection reuse issues that could arise
          if the same engine is used later in the application.
        - The function is called automatically when Alembic is not in offline
          mode (i.e., `context.is_offline_mode()` is `False`).
        - This online mode is the default for most migrations; offline mode is
          typically used only for generating SQL scripts.
    """
    section: dict[str, str] | None = config.get_section(config.config_ini_section)
    if section is None:
        raise ValueError("Configuration section not found")
    
    schema: str = _settings.DB_SCHEMA
    connectable: Engine = engine_from_config(
        section,
        prefix="sqlalchemy.",
        url = config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
        connect_args={"options": f"-c search_path={schema},public"}
    )
    with connectable.connect() as connection:
        context.configure(
            include_schemas=True,
            version_table_schema=schema,
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            compare_type=True,
            compare_server_default=True
        )
        with context.begin_transaction():
            context.run_migrations()
    
    connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
