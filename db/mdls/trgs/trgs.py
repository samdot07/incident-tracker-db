from __future__ import annotations

from sqlalchemy import Connection

from utils.utils.name import _quoted_identifier
from mdls.funcs.funcs import _quoted_func_name

def _quoted_tg_name(
    conn: Connection,
    tbl: str, 
    suffix: str = "updated"
) -> str:
    """
    Generate a quoted PostgreSQL trigger name from a table name and a suffix.

    The trigger name is constructed as ``tg_{tbl}_{suffix}``, then passed
    through ``_quoted_identifier()`` to return a properly quoted identifier
    suitable for use in dynamic DDL statements. Quoting is essential to
    safely handle table names that contain uppercase letters, spaces, or
    reserved SQL keywords.

    Args:
        conn: Active SQLAlchemy Connection (used by ``_quoted_identifier``
            to determine the database dialect's quoting rules, typically via
            ``conn.dialect``).
        tbl: Base table name (unquoted). The function will construct the
            raw trigger name from this string. Must not be ``None`` or empty.
        suffix: Optional suffix appended to the trigger name. Defaults to
            ``"updated"`` (typical for ``updated_at`` timestamps). The suffix
            is **not** quoted separately; it becomes part of the raw identifier.

    Returns:
        A string containing the fully quoted trigger name, e.g.:
        ``'"tg_events_updated"'`` for a table named ``"events"`` when using
        standard PostgreSQL quoting (double quotes).

    Notes:
        - This function does **not** validate that the trigger name is
          within PostgreSQL's 63‑byte identifier length limit. Callers should
          ensure that ``tbl`` and ``suffix`` are sufficiently short.
        - The returned name is safe to interpolate directly into DDL strings
          because it has been quoted by the database dialect. However, always
          use the returned value as a single token; do not further format it.
        - This is a helper for `updated_at_trigger()` and similar trigger
          generation utilities.

    Example:
        >>> from sqlalchemy import create_engine
        >>> engine = create_engine("postgresql://...")
        >>> with engine.connect() as conn:
        ...     quoted = _quoted_tg_name(conn, "user_sessions", "last_modified")
        ...     print(quoted)
        ...     # Output: "tg_user_sessions_last_modified" (with appropriate quoting)
    """
    trg: str = f"tg_{tbl}_{suffix}"
    return _quoted_identifier(conn, trg)
    
def updated_at_trigger(
    conn: Connection,
    tbl: str,
    schema: str
) -> str:
    """
    Generate a DDL statement to create a PostgreSQL ``BEFORE UPDATE`` trigger
    that calls a generic ``update_tg()`` function (assumed to exist in the
    given schema) for the specified table.

    The generated trigger is named ``tg_{tbl}_updated`` (quoted) and executes
    the function ``update_tg()`` **for each row** before an update operation.
    It is typically used to automatically maintain an ``updated_at`` timestamp
    column on the target table.

    Args:
        conn: Active SQLAlchemy Connection. Used to determine quoting rules
            for table and function names via the dialect.
        tbl: Name of the target table (unquoted). The table is assumed to
            already exist in the given schema. The trigger will be created
            **on** this table.
        schema: Database schema name (unquoted, e.g., ``"public"``). The
            trigger, the table, and the ``update_tg()`` function are all
            assumed to reside in this schema.

    Returns:
        A string containing a complete PostgreSQL ``CREATE OR REPLACE TRIGGER``
        statement. The statement uses quoted identifiers for the trigger name,
        the table name, and the function name, making it safe against SQL
        injection and identifier collisions.

    Raises:
        No explicit exceptions. However, the generated DDL will fail at
        execution time if:
            - The target table does not exist in the specified schema.
            - The function ``update_tg()`` does not exist in that schema.
            - The function signature does not match a ``BEFORE UPDATE … FOR EACH ROW``
              trigger (typically it should return ``TRIGGER`` and accept no
              arguments).

    Notes:
        - The generated string uses ``CREATE OR REPLACE TRIGGER``, which will
          replace an existing trigger with the same name. Be aware that this
          overwrites any prior definition (including trigger parameters).
        - The trigger assumes the existence of a **trigger function** named
          ``update_tg()`` in the same schema. A typical implementation might be:

          .. code-block:: sql

              CREATE OR REPLACE FUNCTION public.update_tg()
              RETURNS TRIGGER AS $$
              BEGIN
                  NEW.updated_at = NOW();
                  RETURN NEW;
              END;
              $$ LANGUAGE plpgsql;

        - The trigger does **not** check for the presence of an ``updated_at``
          column; if the column is missing, the function will raise an error
          at runtime.
        - All identifiers (table, schema, trigger name) are quoted using the
          connection's dialect. This ensures correct handling of mixed‑case
          or reserved‑word names.

    Security considerations:
        - Because all identifiers are properly quoted via the helper functions,
          there is **no SQL injection risk** when the input strings come from
          trusted internal sources (e.g., configuration, hard‑coded table names).
          However, if ``tbl`` or ``schema`` are derived from user input, they
          must still be validated against an allowlist of existing tables/schemas
          **before** calling this function, because quoting does not prevent
          the use of non‑existent or maliciously crafted identifiers (e.g.,
          ``"tbl; DROP TABLE users; --"`` would be quoted as a single identifier,
          not executed as a command).

    Example:
        >>> from sqlalchemy import create_engine, text
        >>> engine = create_engine("postgresql://...")
        >>> with engine.connect() as conn:
        ...     ddl = updated_at_trigger(conn, "events", "public")
        ...     print(ddl)
        ...     # conn.execute(text(ddl))   # execute after table & function exist
        ...
        # Output (with standard PostgreSQL quoting):
        # CREATE OR REPLACE TRIGGER "tg_events_updated"
        #     BEFORE UPDATE ON "public"."events"
        #     FOR EACH ROW
        #     EXECUTE FUNCTION "public"."update_tg"();
    """
    quoted_tbl: str = _quoted_func_name(conn, schema, tbl)
    quoted_trg: str = _quoted_tg_name(conn, tbl)
    quoted_func: str = _quoted_func_name(conn, schema, "update_tg")

    return f"""
        CREATE OR REPLACE TRIGGER {quoted_trg}
            BEFORE UPDATE ON {quoted_tbl}
            FOR EACH ROW
            EXECUTE FUNCTION {quoted_func}();
    """