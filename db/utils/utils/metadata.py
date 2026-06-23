from __future__ import annotations
from typing import Any

from sqlalchemy import MetaData, Table
from sqlalchemy.exc import NoReferencedTableError

def _get_tbl(
    metadata: MetaData,
    has_col: str | None = None
) -> list[str]:
    """
    Extract a list of table names from the given SQLAlchemy `MetaData` object,
    optionally filtered by the presence of a specific column.

    The function uses `metadata.sorted_tables`, which returns tables in a
    dependency‑aware order (parent tables before child tables, respecting
    foreign key constraints). This ensures that the order is consistent and
    can be used safely for operations that require topological sorting
    (e.g., creating tables in the correct sequence).

    If `has_col` is provided, only tables that contain a column with that
    exact name are included in the result. This is useful for identifying
    tables that have an `updated_at` column, for instance.

    Parameters:
        metadata (MetaData): The SQLAlchemy `MetaData` collection that
            contains all table definitions. Typically this is `Base.metadata`.
        has_col (str | None): An optional column name to filter tables.
            If given, only tables that have a column named `has_col` are
            returned. If `None` (default), all tables are returned.

    Returns:
        list[str]: A list of raw (unqualified) table names as strings, in
            the order determined by `metadata.sorted_tables`.

    Notes:
        - The returned names are **not** SQL‑escaped or schema‑qualified.
          For quoting or schema qualification, use `_quoted_identifier()`
          and `_get_schema()` respectively.
        - The dependency order is important for migrations where tables
          must be created/dropped in a specific sequence.

    Example:
        >>> from mdls.base.base import Base
        >>> all_tables = _get_tbl(Base.metadata)
        >>> updated_tables = _get_tbl(Base.metadata, has_col="updated_at")
        >>> print(all_tables)   # ['user', 'address', 'order']
        >>> print(updated_tables)  # ['user', 'order']  (if address lacks updated_at)
    """
    tbls: list[Table] = metadata.sorted_tables
    if has_col:
        tbls: list[Table] = [t for t in tbls if has_col in t.c]
    return [t.name for t in tbls]

def _get_schema(metadata: MetaData) -> str:
    """
    Return the schema name from the given SQLAlchemy `MetaData` object,
    defaulting to `'public'` if no schema is explicitly set.

    This function is used throughout migrations and utilities to obtain the
    target schema for all database objects. It ensures that a string is
    always returned, avoiding `None` values that could cause issues in
    SQL generation.

    Parameters:
        metadata (MetaData): The SQLAlchemy `MetaData` instance, typically
            `Base.metadata`, which may have a `schema` attribute defined.

    Returns:
        str: The schema name as a string. If `metadata.schema` is `None`,
            returns `'public'` (the PostgreSQL default).

    Notes:
        - In PostgreSQL, if no schema is specified, objects are created in
          the first schema in the `search_path`, which often is `public`.
          Returning `'public'` as a fallback is a safe convention.
        - The returned value is not quoted; for safe SQL construction,
          combine with `_quoted_identifier()`.

    Example:
        >>> schema = _get_schema(Base.metadata)
        >>> print(schema)   # 'geopolitical_tracker' or 'public'
    """
    return metadata.schema or "public"

def _get_trg(metadata: MetaData) -> list[tuple[str, str]]:
    """
    Generate a list of (table_name, trigger_name) pairs for creating triggers
    that automatically update a timestamp column on row updates.

    This function is intended to be used in migration scripts that need to
    create `BEFORE UPDATE` triggers on all tables. It applies a fixed naming
    convention: `tg_{table_name}_updated` for the trigger name, where
    `{table_name}` is the raw name of the table.

    The trigger is typically used in conjunction with a stored function
    (e.g., `update_tg`) that sets an `updated_at` column to `CURRENT_TIMESTAMP`.
    The table name is taken from `metadata.sorted_tables` to ensure a
    consistent, dependency‑aware order.

    Parameters:
        metadata (MetaData): The SQLAlchemy `MetaData` collection.

    Returns:
        list[tuple[str, str]]: A list of tuples, each containing:
            - The raw table name (str)
            - The corresponding trigger name (str) following the pattern
              `tg_{table_name}_updated`.

    Notes:
        - This function does **not** check whether a trigger already exists
          on the table; it simply generates the names.
        - The returned names are not schema‑qualified; schema qualification
          is handled separately by the migration code.
        - If the table name contains special characters, the trigger name
          may need to be quoted; use `_quoted_tg_name()` for that purpose.

    Example:
        >>> pairs = _get_trg(Base.metadata)
        >>> for tbl, trg in pairs:
        ...     print(f"CREATE TRIGGER {trg} ON {tbl} ...")
        # Output: ('user', 'tg_user_updated'), ('address', 'tg_address_updated')
    """
    return [(t.name, f"tg_{t.name}_updated") for t in metadata.sorted_tables]

def _resolve_tbl(
    metadata: MetaData, 
    tbl_name: str
) -> Table:
    """
    Resolve a table name to its corresponding `Table` object from the metadata.

    This function attempts to find a table by its full, schema‑qualified name
    (e.g., `'public.user'`) or by its unqualified name (e.g., `'user'`).
    It first checks `metadata.tables` for an exact match on the full name.
    If that fails, it iterates through `metadata.sorted_tables` to find a
    table whose `t.name` matches the given `tbl_name` exactly.

    This is primarily used internally by `_validate_metadata()` to resolve
    foreign key target tables and verify their existence.

    Parameters:
        metadata (MetaData): The SQLAlchemy `MetaData` instance containing
            all table definitions.
        tbl_name (str): The table name to resolve. It may include a schema
            prefix (e.g., `'public.user'`) or be unqualified (`'user'`).

    Returns:
        Table: The matching SQLAlchemy `Table` object.

    Raises:
        KeyError: If no table matching the given name is found in the metadata.

    Notes:
        - The function does not check for ambiguous matches (e.g., if two
          tables have the same unqualified name in different schemas).
          In such cases, the first match found in `metadata.tables` or
          `sorted_tables` is returned.
        - This is a low‑level helper and is not typically called directly
          in application code.

    Example:
        >>> tbl = _resolve_tbl(Base.metadata, 'user')
        >>> print(tbl.c)   # ColumnCollection of the 'user' table
    """
    if tbl_name in metadata.tables:
        return metadata.tables[tbl_name]
    
    for t in metadata.sorted_tables:
        if t.name == tbl_name:
            return t
    
    raise KeyError("Table name not found in metadata")

def _validate_metadata(metadata: MetaData) -> None:
    """
    Validate all foreign key constraints and relationship secondary table
    references in the given SQLAlchemy `MetaData` object.

    This function performs a thorough check of every foreign key constraint
    defined on every table in the metadata. For each foreign key, it verifies
    that the referenced table and column exist within the same `MetaData`
    collection. It also catches `NoReferencedTableError` exceptions that
    SQLAlchemy might raise during reflection.

    This validation is essential to catch mis‑configured relationships early,
    before any database operations (such as `create_all()` or migration
    generation) are attempted. It is especially useful in complex schemas
    with cross‑schema dependencies.

    The function aggregates all errors and raises a single `ValueError`
    containing a detailed list of all failing constraints.

    Parameters:
        metadata (MetaData): The SQLAlchemy `MetaData` instance to validate.

    Raises:
        ValueError: If any foreign key constraint references a non‑existent
            table or column. The error message includes a list of all
            problematic constraints, each with the parent table name,
            the column involved, the target reference, and the underlying
            exception.

    Usage:
        This function should be called **after** all model classes have been
        imported and registered with `Base.metadata`, typically at application
        startup or during migration script generation.

        Example:
            # After all model definitions are loaded
            from mdls.base.base import Base
            from utils.utils.metadata import _validate_metadata
            _validate_metadata(Base.metadata)

    Notes:
        - The function iterates over `metadata.sorted_tables`, which respects
          the dependency order.
        - It uses `_resolve_tbl()` to look up referenced tables, which handles
          both qualified and unqualified names.
        - This validation does **not** modify the metadata; it only performs
          read‑only checks.
        - If the metadata is invalid, the raised exception will prevent the
          application from proceeding with an inconsistent schema.

    Example error output:
        ValueError: Metadata validation failed:
        Table 'order': FK order.user_id -> public.user.id: Table name not found in metadata
        Table 'address': FK address.city_id -> city.id: Column not found
    """
    errors: list[str] = []
    for t in metadata.sorted_tables:
        for fk in t.foreign_key_constraints:
            for c in fk.elements:
                fullname: Any = c.target_fullname
                tbl_name, _, col = fullname.rpartition(".")
                try:
                    tbl: Table = _resolve_tbl(metadata, tbl_name)
                    if col not in tbl.c:
                        raise KeyError(f"Column not found")
                except (KeyError, NoReferencedTableError) as e:
                    errors.append(
                        f"Table '{t.name}': FK {c.parent} -> {fullname}: {e}"
                    )
                    
    if errors: 
        raise ValueError(
            "Metadata validation failed:\n" + "\n".join(errors)
        )