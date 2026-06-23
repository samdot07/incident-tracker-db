from __future__ import annotations
from typing import Any, TypeVar

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql.dml import Insert as PGInsert
from sqlalchemy.orm.mapper import Mapper
    
T = TypeVar("T")
    
def build_insert(
    model: type[T],
    mapper: Mapper[T],
    *,
    on_conflict: str | None = None,
    idx_elements: list[str] | None = None
) -> PGInsert:
    """
    Construct a PostgreSQL `INSERT` statement with optional `ON CONFLICT`
    handling, using SQLAlchemy's dialect‑specific `Insert` construct.

    This helper is designed for bulk upsert operations (e.g., with
    `session.execute(stmt, list_of_dicts)`) where you need to insert new
    rows and, if a conflict occurs, either ignore the insertion or update
    the conflicting row. It abstracts the complexity of building the
    `ON CONFLICT` clause and automatically filters out columns that should
    never be updated during an upsert.

    The function requires both the model class and its corresponding
    SQLAlchemy `Mapper` object (obtained via `inspect(model)`). This allows
    it to inspect column attributes like `server_default`, `identity`, and
    `computed` to determine which columns should be excluded from the
    update set.

    **Supported conflict actions**:
        - `None` (default): plain `INSERT` without any conflict clause.
        - `'do_nothing'`: `ON CONFLICT ... DO NOTHING` – silently skips
          rows that violate the uniqueness constraint.
        - `'do_update'`: `ON CONFLICT ... DO UPDATE SET ...` – performs an
          upsert, updating all non‑excluded columns with the proposed values.

    **Automatic exclusion for `DO UPDATE`**:
    When `on_conflict='do_update'`, the following columns are **never**
    included in the `SET` clause, preserving their existing values on conflict:

        - All columns listed in `idx_elements` (the conflict target).
        - System/timestamp columns: `'created_at'`, `'updated_at'`, `'uuid'`,
          and `'id'`.
        - Any column that has:
            - A `server_default` without a corresponding `server_onupdate`
              (i.e., default value set by the database on insert only).
            - An `identity` column (e.g., `GENERATED AS IDENTITY`).
            - A `computed` column (e.g., `GENERATED ALWAYS AS ...`).

    This ensures that primary keys, auto‑generated timestamps, and
    database‑managed values are not overwritten by the upsert, which would
    otherwise cause errors or unexpected behavior.

    Parameters:
        model (type[T]): The SQLAlchemy ORM model class (e.g., `User`).
            Used as the target of the insert.
        mapper (Mapper[T]): The corresponding SQLAlchemy `Mapper` object,
            typically obtained via `inspect(model)`. Provides column
            metadata for exclusion logic.
        on_conflict (str | None, optional): Determines the conflict handling
            strategy. Acceptable values:
                - `None`: No `ON CONFLICT` clause (plain insert).
                - `'do_nothing'`: Add `ON CONFLICT ... DO NOTHING`.
                - `'do_update'`: Add `ON CONFLICT ... DO UPDATE SET ...`.
            Defaults to `None`.
        idx_elements (list[str] | None, optional): A list of column names
            that define the conflict target (e.g., `['email']` or
            `['user_id', 'role_id']`). This is **required** if `on_conflict`
            is not `None`. The columns must have a unique constraint or
            unique index in the database.

    Returns:
        PGInsert: A SQLAlchemy `Insert` construct (specifically the
            PostgreSQL dialect's `PGInsert` subclass) that can be executed
            using a session or connection. The construct includes the
            `ON CONFLICT` clause if specified.

    Raises:
        ValueError: If `on_conflict` is `'do_nothing'` or `'do_update'`
            and `idx_elements` is `None` or an empty list.
        ValueError: If `on_conflict` is a string that is not one of
            `None`, `'do_nothing'`, or `'do_update'`.

    Notes:
        - The function uses `stmt.excluded[c.name]` in the `DO UPDATE SET`
          clause to reference the values that would have been inserted.
        - The returned statement is not executed; it must be passed to
          `session.execute()` or `connection.execute()` along with the
          parameter list.
        - This function does **not** perform any validation of column names
          in `idx_elements`; it is the caller's responsibility to ensure
          they are valid and form a unique constraint.
        - If the model uses a custom schema, the statement will automatically
          include the schema via the model's table metadata.

    Example:
        >>> from sqlalchemy.orm import inspect
        >>> from myapp.models import User
        >>> mapper = inspect(User)
        >>> 
        >>> # Plain insert
        >>> stmt = build_insert(User, mapper)
        >>> session.execute(stmt, [{'name': 'Alice', 'email': 'a@b.com'}])
        >>> 
        >>> # Upsert with ON CONFLICT DO UPDATE
        >>> stmt = build_insert(
        ...     User, mapper,
        ...     on_conflict='do_update',
        ...     idx_elements=['email']
        ... )
        >>> data = [
        ...     {'email': 'a@b.com', 'name': 'Alice Updated'},
        ...     {'email': 'c@d.com', 'name': 'Charlie'}
        ... ]
        >>> session.execute(stmt, data)
        >>> 
        >>> # Ignore conflicts
        >>> stmt = build_insert(
        ...     User, mapper,
        ...     on_conflict='do_nothing',
        ...     idx_elements=['email']
        ... )
        >>> session.execute(stmt, data)

    See Also:
        - PostgreSQL `INSERT ... ON CONFLICT` documentation:
          https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT
        - SQLAlchemy `Insert` dialect documentation:
          https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-insert-on-conflict
    """
    if on_conflict is None:
        return PGInsert(model)
    
    elif on_conflict == 'do_nothing':
        if not idx_elements:
            raise ValueError("idx_elements required for ON CONFLICT")
        stmt: PGInsert = PGInsert(model).on_conflict_do_nothing(
            index_elements=idx_elements
        )
        return stmt
    
    elif on_conflict == 'do_update':
        if not idx_elements:
            raise ValueError("idx_elements required for ON CONFLICT")
        stmt = PGInsert(model)
        
        always_exclude: set[str] = set(idx_elements) | {"created_at", "updated_at","uuid", "id"}
        
        read_cols: set[Column[Any]] = {
            c for c in mapper.columns
            if (c.server_default is not None and c.server_onupdate is None)
            or c.identity is not None
            or c.computed is not None
        }
        
        excluded: set[str] = always_exclude.union({c.name for c in read_cols})
        
        update_cols: dict[str, Column[Any]] = {
            c.name: c for c in mapper.columns
            if c.name not in excluded
        }
        
        stmt = stmt.on_conflict_do_update(
            index_elements=idx_elements,
            set_={
                c.name: stmt.excluded[c.name] for c in update_cols.values()
            }
        )
        return stmt
    
    else:
        raise ValueError("Unsupported on_conflict")