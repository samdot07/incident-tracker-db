from __future__ import annotations

from sqlalchemy import URL
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError

def sec_dsn(dsn: object) -> str:
    """
    Safely redact the password (and other sensitive details) from a database
    connection string, returning a simplified representation.

    This function takes any input (typically a PostgreSQL DSN string) and
    attempts to parse it using SQLAlchemy's `make_url()`. If successful, it
    returns a compact string containing only the host, port, and database name,
    omitting the username, password, and any query parameters. This provides a
    human‑readable, non‑sensitive identifier for logging, error messages, or
    debugging without exposing credentials.

    If the input is not a string, or if parsing fails, the function returns
    one of several safe placeholder messages instead of raising an exception.
    This makes it suitable for use in contexts where robustness is more
    important than exact output.

    Parameters:
        dsn (object): A database connection string (e.g.,
            `"postgresql://user:pass@host:5432/db"`) or any other object.
            Typically a `str`, but the function accepts any type gracefully.

    Returns:
        str: A redacted representation of the DSN, or a placeholder string:
            - On successful parsing: `"{host}:{port}/{database}"` (e.g.,
              `"myhost:5432/mydb"`). The port defaults to `5432` if not
              explicitly provided in the DSN.
            - If `dsn` is not a `str`: `"<invalid dsn type>"`.
            - If the DSN lacks a host or database name: `"<incomplete dsn>"`.
            - If parsing fails (e.g., malformed URL): `"<unparseable dsn>"`.

    Raises:
        This function does **not** raise any exceptions. All errors (including
        `ValueError`, `ArgumentError`, and `TypeError` from the parsing step)
        are caught and result in the `"<unparseable dsn>"` placeholder.

    Notes:
        - The function intentionally discards the username, password, and any
          query parameters (e.g., `?sslmode=require`) to ensure no sensitive
          information leaks.
        - The default port (`5432`) is used only when the DSN does not specify
          a port. This is the standard PostgreSQL default.
        - The redacted output is **not** a valid DSN for reconnection; it is
          purely informational.
        - This function is primarily intended for logging, error reporting, or
          debugging contexts where showing the full DSN would be a security
          risk.

    Example:
        >>> sec_dsn("postgresql://alice:secret@db.example.com:5432/analytics")
        'db.example.com:5432/analytics'

        >>> sec_dsn("postgresql://user@host/db")
        'host:5432/db'

        >>> sec_dsn("invalid-dsn")
        '<unparseable dsn>'

        >>> sec_dsn(None)
        '<invalid dsn type>'

        >>> sec_dsn("postgresql://host/db")   # no port specified
        'host:5432/db'

        >>> sec_dsn("postgresql://host")      # missing database
        '<incomplete dsn>'
    """
    if not isinstance(dsn, str):
        return "<invalid dsn type>"
    
    try:
        url: URL = make_url(dsn)
        host: str | None = url.host
        port: int = url.port if url.port is not None else 5432
        db: str | None = url.database
        
        if not host or not db:
            return "<incomplete dsn>"
        return f"{host}:{port}/{db}"
    
    except (ValueError, ArgumentError, TypeError):
        return "<unparseable dsn>"