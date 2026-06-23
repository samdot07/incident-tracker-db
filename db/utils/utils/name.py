from __future__ import annotations
import re

from sqlalchemy import Connection, MetaData
from sqlalchemy.sql.compiler import IdentifierPreparer
import inflect

def _quoted_identifier(
    conn: Connection,
    name: str
) -> str:
    """
    Quote a SQL identifier using the dialect-specific quoting rules of the
    active database connection.

    This function delegates to the connection's `IdentifierPreparer` to
    produce a properly quoted identifier. This is essential for identifiers
    that contain mixed case, special characters, or are PostgreSQL reserved
    keywords (e.g., `"order"`, `"myTable"`, `"user-id"`). The quoting style
    is determined by the underlying database dialect (e.g., double quotes for
    PostgreSQL, backticks for MySQL).

    Parameters:
        conn (Connection): An active SQLAlchemy `Connection` (or an `Engine`)
            that provides the dialect information.
        name (str): The unquoted identifier (e.g., table name, column name,
            schema name, function name).

    Returns:
        str: The identifier wrapped in the appropriate quoting characters
            for the target database.

    Notes:
        - This function is the primary utility for safely constructing SQL
          statements that include dynamic object names. It prevents SQL
          injection and syntax errors caused by unquoted reserved words.
        - The returned string is suitable for concatenation into raw SQL
          strings (though using SQLAlchemy's text() or other parameterized
          approaches is still recommended for values).
        - For schema‑qualified identifiers, call this function on each
          component separately (e.g., schema and table) and join with '.'.

    Example:
        >>> quoted = _quoted_identifier(conn, "myTable")
        >>> print(quoted)   # '"myTable"'
        >>> quoted_reserved = _quoted_identifier(conn, "order")
        >>> print(quoted_reserved)   # '"order"'
        >>> # Schema-qualified:
        >>> schema = _quoted_identifier(conn, "public")
        >>> table = _quoted_identifier(conn, "user")
        >>> full = f"{schema}.{table}"   # '"public"."user"'
    """
    preparer: IdentifierPreparer = conn.dialect.identifier_preparer
    return preparer.quote_identifier(name)

def _snake_case(name: str) -> str:
    """
    Convert a CamelCase string to snake_case.

    This function is used to transform Python class names (typically Enum
    class names) into PostgreSQL‑friendly type names. The conversion follows
    standard snake_case rules:
        - Insert underscores before each uppercase letter that is followed
          by a lowercase letter or digit.
        - Handle consecutive uppercase letters (acronyms) appropriately.
        - Convert the result to lowercase.

    Parameters:
        name (str): A string in CamelCase (e.g., `'UserRole'`, `'HTTPStatusCode'`).

    Returns:
        str: The snake_case version of the input (e.g., `'user_role'`,
            `'http_status_code'`).

    Notes:
        - This function does **not** handle all edge cases (e.g., numbers)
          perfectly, but it is sufficient for the typical enum class names
          used in this project.
        - It is used in the enum registry (`_get_enum()`) to generate SQL
          type names that are consistent with PostgreSQL naming conventions.

    Example:
        >>> _snake_case('UserRole')          # 'user_role'
        >>> _snake_case('HTTPStatusCode')    # 'http_status_code'
        >>> _snake_case('ActorType')         # 'actor_type'
    """
    s: str = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    return re.sub(r'([a-z\d]+)([A-Z])', r'\1_\2', s).lower()  
        
_p = inflect.engine()

def _fk_ref(metadata: MetaData, tbl_col: str) -> str:
    """
    Build a schema‑qualified foreign key reference string from a `table.column`
    specification, optionally prefixing the schema if set on the metadata.

    This function is intended for constructing strings to be used inside
    SQLAlchemy `ForeignKey` declarations, especially when the application
    schema is not the default `public`. If `metadata.schema` is `None`,
    the returned string is the original `tbl_col` (with the table name
    pluralized). If a schema is set, the result is `schema.qualified`,
    where `qualified` is the pluralized form of the table name plus the column.

    The function uses the `inflect` engine to pluralize the table name,
    which is an unusual choice for foreign key references (typically the
    table name is used as‑is). **This behavior is preserved as written in the
    current implementation** – the docstring reflects the actual logic.

    Parameters:
        metadata (MetaData): The SQLAlchemy `MetaData` object containing
            the schema information.
        tbl_col (str): A string in the format `'table.column'` (e.g., `'actor.id'`).

    Returns:
        str: A foreign key reference string. If `metadata.schema` is set,
            returns `'schema.plural_table.column'`. Otherwise returns
            `'plural_table.column'`.

    Notes:
        - The function **does not** quote any identifiers; for quoting,
          combine with `_quoted_identifier()` on each component.
        - The pluralization is performed using `inflect.engine().plural()`.
          This may be intentional if the foreign key references a table name
          that is conventionally plural (e.g., `actors`), but it is an
          unusual practice in SQLAlchemy.
        - If `tbl_col` does not contain a dot, the behavior is undefined
          (the `partition` will return an empty column string).

    Example:
        >>> # Assume metadata.schema = 'cinema'
        >>> _fk_ref(metadata, 'actor.id')      # -> 'cinema.actors.id'
        >>> # If metadata.schema is None:
        >>> _fk_ref(metadata, 'actor.id')      # -> 'actors.id'

    See Also:
        `_secondary_ref()` – for schema‑qualifying association table names.
    """
    schema: str | None = metadata.schema
    tbl, _, col = tbl_col.partition(".")
    plural: str = _p.plural(tbl) # type: ignore
    qualified: str = f"{plural}.{col}" if col else plural
    
    return f"{schema}.{qualified}" if schema else qualified

def _secondary_ref(metadata: MetaData, tbl_name: str) -> str:
    """
    Build a schema‑qualified table name for a many‑to‑many relationship's
    `secondary` parameter.

    This function is used when defining SQLAlchemy relationships that involve
    a secondary association table. If `metadata.schema` is set, it prefixes
    the schema name to the table name; otherwise, it returns the table name
    pluralized (using `inflect`). The pluralization is applied **only** when
    no schema is defined.

    Parameters:
        metadata (MetaData): The SQLAlchemy `MetaData` object containing
            the schema information.
        tbl_name (str): The base name of the association table (e.g., `'event_actor'`).

    Returns:
        str: A schema‑qualified table name if `metadata.schema` is set,
            otherwise the pluralized version of `tbl_name`.

    Notes:
        - Like `_fk_ref()`, this function does **not** quote identifiers.
        - The pluralization when no schema is defined is likely a historical
          artifact; in typical usage, the association table name is used
          exactly as defined in the metadata.
        - If the metadata schema is set, the table name is **not** pluralized
          (the original `tbl_name` is used without change).

    Example:
        >>> # Assume metadata.schema = 'cinema'
        >>> _secondary_ref(metadata, 'event_actor')   # -> 'cinema.event_actor'
        >>> # If metadata.schema is None:
        >>> _secondary_ref(metadata, 'event_actor')   # -> 'event_actors'

    See Also:
        `_fk_ref()` – for foreign key references with similar schema handling.
    """
    schema: str | None = metadata.schema
    plural: str = _p.plural(tbl_name) # type: ignore

    return f"{schema}.{tbl_name}" if schema else plural