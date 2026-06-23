from __future__ import annotations
from typing import Any, TypeVar

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql.dml import Insert as PGInsert
from sqlalchemy.orm import Session, Mapper, class_mapper
from sqlalchemy.engine import Result

from utils.utils.utils import build_insert

T = TypeVar("T")

def _bulk_insert(
    model: type[T],
    session: Session,
    data: list[dict[str, Any]],
    *,
    on_conflict: str | None = None,
    chunk_size: int = 1000,
    idx_elements: list[str] | None = None
) -> list[dict[str, Any]]:
    """
    Perform an efficient bulk insert of multiple rows into a PostgreSQL table.

    This function builds a single INSERT statement (optionally with ON CONFLICT handling)
    and executes it in chunks. It automatically determines which column values should be
    returned after insertion – typically those with server defaults, identities, computed
    columns, or ON UPDATE rules. If no such columns exist, it returns all inserted columns.

    The function does NOT manage transactions by itself. It verifies that the session
    is inside an explicit transaction and emits a warning otherwise. Callers are
    responsible for beginning a transaction (e.g., via session.begin() or a context
    manager) before invoking this function.

    Args:
        model (type[T]): The SQLAlchemy ORM model class (e.g., MyTable).
        session (Session): An active SQLAlchemy ORM session. Must be inside a transaction.
        data (list[dict[str, Any]]): List of dictionaries, each representing a row to insert.
            Keys must correspond to column names of the model.
        on_conflict (str | None): Optional ON CONFLICT clause for PostgreSQL.
            Example: "DO NOTHING" or "DO UPDATE SET updated_at = EXCLUDED.updated_at".
            The string is inserted verbatim after "ON CONFLICT". If None, no conflict handling.
        chunk_size (int): Number of rows inserted per batch. Default 1000.
        idx_elements (list[str] | None): List of column names to use in the conflict target
            (e.g., unique constraint columns). Used when constructing the ON CONFLICT clause.
            Ignored if on_conflict is None.

    Returns:
        list[dict[str, Any]]: A list of dictionaries containing the returned column values
            for every inserted row, in insertion order. Each dict's keys are column names.
            If the database returns no rows (e.g., ON CONFLICT DO NOTHING with no rows
            actually inserted), the list may be empty. Otherwise, length equals
            the number of rows that were inserted (or attempted, depending on RETURNING).

    Errors:
        RuntimeError: Emitted if session.in_transaction() returns False, i.e., when
            the session is not inside an explicit transaction. This can lead to partial
            commits or autocommit surprises.

    Raises:
        Does not raise exceptions directly related to data integrity or constraint violations;
        those bubble up from session.execute(). However, if the model does not have a
        configured mapper, class_mapper will raise sqlalchemy.orm.exc.UnmappedClassError.

    Notes:
        - The function relies on an internal helper `_build_insert` (not shown) to construct
          the base Insert statement. That helper must accept `model`, `mapper`, `on_conflict`,
          and `idx_elements`.
        - PostgreSQL's RETURNING clause is used to fetch generated column values efficiently.
        - When no special returning columns exist, the function returns all columns,
          which may have a performance impact for wide tables. Consider narrowing returned
          columns if only a subset is needed.
        - The function does NOT flush or commit the session; that remains the caller's
          responsibility.
        - Chunking is used to avoid excessive memory usage from a single massive VALUES list.

    Example:
        >>> from myapp.models import Product
        >>> from sqlalchemy.orm import Session
        >>>
        >>> data = [
        ...     {"name": "Laptop", "price": 999.99},
        ...     {"name": "Mouse", "price": 19.99}
        ... ]
        >>> with Session(engine) as session:
        ...     with session.begin():
        ...         results = _bulk_insert(
        ...             Product,
        ...             session,
        ...             data,
        ...             on_conflict="DO NOTHING",
        ...             idx_elements=["name"]
        ...         )
        ...         # results contains auto-generated primary keys etc.
    """
    if not session.in_transaction():
        raise RuntimeError(
            "_bulk_insert called without an active transaction. "
            "Call session.begin() or use 'with session.begin():' before invoking this function.",
            RuntimeWarning
        )
        
    if not data:
        return []
    
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")

    # Automatically discover columns that need returning (server defaults, identities, computed)
    mapper: Mapper[T] = class_mapper(model)
    returning_cols: list[Column[Any]] = [
        c for c in mapper.columns
        if c.server_default is not None
        or c.server_onupdate is not None
        or c.identity is not None
        or c.computed is not None
    ]
    
    base_stmt: PGInsert = build_insert(
        model, mapper,
        on_conflict=on_conflict,
        idx_elements=idx_elements,
    )

    all_result: list[dict[str, Any]] = []
        
    for i in range(0, len(data), chunk_size):
        chunk: list[dict[str, Any]] = data[i:i + chunk_size]
        stmt = base_stmt.values(chunk)
        if returning_cols:
            stmt = stmt.returning(*returning_cols)
            col_names: list[str] = [c.key for c in returning_cols]
        else:
            stmt = stmt.returning(*mapper.columns)
            col_names = [c.key for c in mapper.columns]
            
        result: Result = session.execute(stmt) 
        rows: list[dict[str, Any]] = [
            dict(zip(col_names, row)) for row in result.fetchall()
        ]
        all_result.extend(rows)

    return all_result