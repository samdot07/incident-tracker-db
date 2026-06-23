from alembic import op

def upgrade() -> None:
    """
    Create (if not already present) the `pg_trgm` and `postgis` PostgreSQL
    extensions in the current database.

    This migration step is executed when upgrading the database schema. It uses
    `CREATE EXTENSION IF NOT EXISTS` to ensure that the required extensions are
    available without causing errors if they already exist. The `pg_trgm`
    extension provides trigram-based text similarity functions and operators,
    which are used for advanced text search capabilities (e.g., `%` similarity
    operator, `similarity()` function) and GIN index support. The `postgis`
    extension adds geospatial data types (e.g., `GEOMETRY`, `GEOGRAPHY`) and
    functions, enabling geographic queries and spatial indexing.

    Both extensions are installed in the default schema (typically `public`),
    as PostgreSQL does not allow specifying a schema with `CREATE EXTENSION`
    in a portable way. The extensions are created in the current database
    and are shared across all schemas.

    The operation is idempotent: if an extension is already installed, the
    `IF NOT EXISTS` clause prevents an error and the command succeeds silently.

    Dependencies:
        - The PostgreSQL server must have the `pg_trgm` and `postgis` contrib
          packages installed (e.g., via `postgresql-contrib` and `postgis`
          packages). If they are not available, the migration will fail with
          a `FATAL` error.
        - The user executing the migration must have the `CREATE EXTENSION`
          privilege on the database.

    Raises:
        - This function does not explicitly raise exceptions, but `op.execute()`
          may raise if the extensions are not available or if privileges are
          insufficient.

    Notes:
        - The `postgis` extension can be heavy to install; ensure that the
          database server has sufficient resources.
        - Installing `postgis` also creates many functions and tables in the
          `public` schema; this is expected behavior.
        - This migration should be run before any table that uses geospatial
          columns or trigram indexes is created.
        - The `IF NOT EXISTS` makes this migration safe to run multiple times
          and allows it to be run in environments where the extensions may
          already exist.
    """
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    
def downgrade() -> None:
    """
    Intentionally left empty – does not drop the `pg_trgm` or `postgis`
    extensions during schema downgrade.

    This migration step is deliberately a no‑op to prevent catastrophic data
    loss and dependency failures. The reasons for not dropping these extensions
    are as follows:

        1. **PostGIS – Cascade destruction**:
           Dropping the `postgis` extension with `CASCADE` would remove all
           `GEOMETRY` and `GEOGRAPHY` columns, spatial indexes, and functions
           from every table in the database. This would result in irreversible
           loss of geospatial data unless a full backup is restored.

        2. **pg_trgm – Index loss**:
           Dropping `pg_trgm` would automatically drop all GIN trigram indexes
           that depend on it. This could severely degrade query performance on
           tables that rely on these indexes for text search, and the indexes
           would need to be recreated manually.

        3. **Shared nature**:
           Extensions are database‑wide objects. They are typically used by
           multiple schemas and applications. Dropping them as part of a single
           migration downgrade may break other parts of the system that are
           unaware of the downgrade.

    Given these risks, the appropriate procedure for removing these extensions
    is a **manual administrative action** performed by a database administrator
    after ensuring:
        - All dependent objects (tables, views, functions, indexes) have been
          either dropped or altered to remove references.
        - A full backup has been created.
        - The application code that depends on these extensions has been
          updated or removed.

    The downgrade function is left empty to avoid accidental execution. Any
    attempt to remove these extensions should be handled outside the migration
    workflow, using careful planning and validation.

    Notes:
        - This no‑op downgrade does not raise any errors; it simply completes
          without making any schema changes.
        - If you absolutely must drop the extensions as part of a downgrade,
          you can manually add the `DROP EXTENSION` statements to this function,
          but you do so at your own risk.
        - The empty downgrade ensures that the migration history remains
          consistent (i.e., the downgrade from the upgrade state is a no‑op),
          which is often preferable to a destructive action.
    """
    pass