from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Connection

from mdls.base.base import Base
from utils.utils.metadata import _get_schema
from utils.utils.name import _quoted_identifier
from utils.enums.registry import _get_enum

def upgrade() -> None:
    """
    Create all application-defined PostgreSQL ENUM types that are registered
    in the enumeration registry.

    This migration step is executed when upgrading the database schema. It
    iterates over every enum definition returned by `_get_enum()`, and for
    each one creates a corresponding PostgreSQL ENUM type using SQLAlchemy's
    `sa.Enum` construct. The types are created in the schema derived from
    `Base.metadata` (via `_get_schema`). If a type with the same name already
    exists, it is left untouched (`checkfirst=True`).

    The function relies on an active database connection obtained from the
    Alembic migration context. If no connection is available, a `RuntimeError`
    is raised.

    Raises:
        RuntimeError: If the Alembic migration context does not provide a
            database connection.

    Notes:
        - The enum names and their associated Python enum classes are sourced
          from the registry function `_get_enum()`, which is expected to return
          an iterable of `(attribute_name, enum_name, enum_class)` tuples.
        - The target schema is determined by `_get_schema(Base.metadata)`,
          which should return the schema name used by the base model.
        - The creation is performed via SQLAlchemy's DDL compiler, which
          issues a `CREATE TYPE` statement. The operation is safe to run
          repeatedly because of `checkfirst=True`.
        - This migration is typically run after the enum registry has been
          populated and before any tables that reference these enums are
          created.
    """
    conn: Connection | None = op.get_context().connection
    if conn is None:
        raise RuntimeError("Migration requires an active connection")
    
    for attr, enum, cls in _get_enum():
        sa_enum = sa.Enum(
            cls, 
            name=enum, 
            schema=_get_schema(Base.metadata), 
            create_type=True
        )
        sa_enum.create(conn, checkfirst=True)

def downgrade() -> None:
    """
    Drop all application-defined PostgreSQL ENUM types that were created
    by the corresponding `upgrade()` migration.

    This migration step is executed when downgrading the database schema. It
    iterates over the same enumeration registry as `upgrade()` and issues a
    `DROP TYPE ... CASCADE` statement for each registered enum type. The
    types are dropped from the schema derived from `Base.metadata`.

    The function requires an active database connection from the Alembic
    context. If the connection is `None`, a `RuntimeError` is raised.

    Important considerations:
        - The `CASCADE` option is used to automatically drop objects that
          depend on the enum type (e.g., table columns). This ensures that
          the downgrade can complete even if tables referencing the enum
          still exist, but it may cause data loss if those tables are not
          also dropped or altered beforehand.
        - The `DROP TYPE` statement is executed using raw SQL via
          `op.execute()` to ensure proper quoting of schema and type names,
          using `_quoted_identifier()` for safe identifier quoting.
        - If an enum type does not exist, the `IF EXISTS` clause prevents
          an error, making the operation idempotent.

    Raises:
        RuntimeError: If the Alembic migration context does not provide a
            database connection.

    Notes:
        - The downgrade assumes that the enum types are no longer needed by
          any table that should survive the downgrade. If tables still rely
          on these types, they must be altered or dropped in a preceding
          migration step.
        - The registry `_get_enum()` is called again to obtain the list of
          types to drop, which must match the set created in `upgrade()`.
        - This operation is not reversible within the same transaction if
          `CASCADE` removes dependent objects; it is recommended to ensure
          that all dependent objects are properly handled before running the
          downgrade.
    """
    schema: str= _get_schema(Base.metadata)
    conn: Connection | None = op.get_context().connection
    if conn is None:
        raise RuntimeError("Migration requires an active connection")
    
    for _, enum, _ in _get_enum():    
        op.execute(
            f"DROP TYPE IF EXISTS {_quoted_identifier(conn, schema)}.{_quoted_identifier(conn, enum)} CASCADE"
        )