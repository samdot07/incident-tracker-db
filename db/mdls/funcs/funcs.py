from __future__ import annotations

from sqlalchemy import Connection

from utils.utils.name import _quoted_identifier

def _quoted_func_name(
    conn: Connection,
    schema: str,
    name: str
) -> str:
    """
    Return a fully quoted qualified function name as ``"schema"."name"``.

    This helper uses SQLAlchemy's dialect‑specific quoting mechanism to safely
    quote both the schema and the function name. The quoted components are then
    concatenated with a period (``.``) to form a valid, safely quoted identifier
    suitable for use in dynamic SQL statements (e.g., inside ``CREATE OR REPLACE
    FUNCTION``).

    **Why quoting is necessary:**
        - Prevents SQL injection when schema or function names come from
          untrusted sources (though here they are internal).
        - Allows identifiers that contain mixed case, spaces, or reserved words
          (e.g., ``"My Schema"."update-tg"``).
        - Respects the quoting rules of the underlying database dialect
          (PostgreSQL uses double quotes).

    **Parameters:**
        conn : ``Connection``
            An active SQLAlchemy database connection. Used to obtain the
            dialect's identifier quoting behaviour via
            ``dialect.identifier_preparer``.
        schema : ``str``
            The database schema name (e.g., ``'public'``, ``'analytics'``).
        name : ``str``
            The unquoted function name (e.g., ``'update_tg'``).

    **Returns:**
        ``str``
            A string of the form ``"quoted_schema"."quoted_name"``. For example,
            with default PostgreSQL quoting and inputs ``schema='my schema'``,
            ``name='update-tg'``, the output would be:
            ``'"my schema"."update-tg"'``.

    **Raises:**
        No explicit exceptions; delegates to ``_quoted_identifier`` which may
        raise if the connection is closed or the preparer fails.

    **Usage example:**

        >>> from sqlalchemy import create_engine
        >>> engine = create_engine("postgresql://user:pass@localhost/db")
        >>> with engine.connect() as conn:
        ...     quoted = _quoted_func_name(conn, "analytics", "update_tg")
        ...     print(quoted)
        '"analytics"."update_tg"'

    **Note:**
        This function is intended for internal use within schema migration or
        dynamic DDL generation. It assumes the caller has already validated that
        ``schema`` and ``name`` are safe to quote (e.g., no embedded double
        quotes that would break quoting).
    """
    quoted_schema: str = _quoted_identifier(conn, schema)
    quoted_name: str = _quoted_identifier(conn, name)
    return f"{quoted_schema}.{quoted_name}"

def tg_function_updated_at(
    conn: Connection, 
    schema: str
) -> str:
    """
    Generate a PostgreSQL ``CREATE OR REPLACE FUNCTION`` statement for an
    ``updated_at`` trigger helper.

    The generated function (named ``update_tg`` in the given schema) is intended
    to be used in a ``BEFORE UPDATE`` trigger on tables that have an
    ``updated_at`` column of type ``timestamptz``. It conditionally sets
    ``NEW.updated_at`` to the current timestamp (using ``clock_timestamp()``)
    **only when** the row's data actually changes (i.e., ``OLD IS DISTINCT FROM
    NEW``). This avoids unnecessary timestamp updates on “no‑op” updates where
    every column remains the same.

    **Key behaviour:**
        - Uses ``clock_timestamp()`` (wall‑clock time with sub‑microsecond
          precision) rather than ``now()`` / ``transaction_timestamp()``, so the
          value advances even within a single transaction – useful for auditing
          and ordering updates.
        - The condition ``OLD IS DISTINCT FROM NEW`` handles ``NULL`` correctly:
          if a column changes from ``NULL`` to a value (or vice versa), it
          triggers the update. If all columns are identical (including nulls),
          the timestamp remains unchanged.
        - The function is idempotent – calling ``CREATE OR REPLACE FUNCTION``
          multiple times is safe and will not break existing triggers that
          reference it.

    **Parameters:**
        conn : ``Connection``
            An active SQLAlchemy connection, used to obtain the correct quoting
            for the function name via ``_quoted_func_name``.
        schema : ``str``
            The database schema where the function will be created (or replaced).
            The function will be named ``update_tg`` inside this schema.

    **Returns:**
        ``str``
            A multi‑line SQL string containing:
                - A ``CREATE OR REPLACE FUNCTION`` statement.
                - A ``COMMENT ON FUNCTION`` statement documenting the function.

    **Security considerations:**
        - The function name and schema are safely quoted using
          ``_quoted_func_name``, preventing SQL injection even if the schema
          argument is derived from user input (not recommended, but guarded).
        - The function body uses only immutable/stable built‑ins and has no
          data‑access side effects – it is safe for concurrent use.

    **Usage example:**

        >>> from sqlalchemy import create_engine, text
        >>> engine = create_engine("postgresql://user:pass@localhost/db")
        >>> with engine.connect() as conn:
        ...     sql = tg_function_updated_at(conn, "public")
        ...     conn.execute(text(sql))
        ...     conn.commit()

    **Applying the trigger to a table:**

        Once the function exists, you can attach it to any table with an
        ``updated_at`` column:

        .. code-block:: sql

            CREATE TRIGGER tr_my_table_updated_at
                BEFORE UPDATE ON my_table
                FOR EACH ROW
                EXECUTE FUNCTION public.update_tg();

    **Note:**
        - The function must be created in the same schema where the target tables
          reside (or be search‑path accessible). The generated SQL places it in
          the schema provided by the ``schema`` parameter.
        - If a function with the same name and argument types already exists, it
          is replaced; existing triggers will use the new definition
          automatically.
        - This function assumes the calling table has an ``updated_at`` column of
          type ``timestamp with time zone`` (``timestamptz``). If the column is
          missing, the trigger will fail at runtime.
    """
    func: str = _quoted_func_name(conn, schema, "update_tg")
    
    return f"""
        CREATE OR REPLACE FUNCTION {func}()
        RETURNS TRIGGER AS $$
        BEGIN
            IF OLD IS DISTINCT FROM NEW THEN
                NEW.updated_at = clock_timestamp();
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        COMMENT ON FUNCTION {func}() IS
            'Set updated_at to current timestamp only when row data actually changes';
    """