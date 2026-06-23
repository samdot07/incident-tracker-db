from __future__ import annotations
from enum import Enum

from utils.utils.name import _snake_case
from utils.enums.enums import ActorType, Region, EventTypeEnum,AttributionConfidence,StrategicSignificance, PoliticalImpact, LegalPrecedent,LocationType, SourceType, InvolvementType, ActorRole

DB_ENUMS: list[type[Enum]] = [
    ActorType,
    Region,
    EventTypeEnum,
    AttributionConfidence,
    StrategicSignificance,
    PoliticalImpact,
    LegalPrecedent,
    LocationType,
    SourceType,
    InvolvementType,
    ActorRole
]

def _get_enum(
    enum_class: type[Enum] | None = None 
) -> list[tuple[str, str, type[Enum]]]:
    """
    Retrieve a list of registered Python Enum classes along with their
    corresponding SQL type names for PostgreSQL ENUM creation.

    This function is the central registry for mapping application‑defined
    Enum subclasses to PostgreSQL `ENUM` types. It is used primarily by
    Alembic migrations (e.g., `enums.py`) to generate `CREATE TYPE` statements
    and by other parts of the system that need to know the set of enumerated
    types that are persisted in the database.

    The function optionally filters to a single enum class if provided;
    otherwise, it returns all enums defined in the `DB_ENUMS` list.

    For each enum, it returns a 3‑element tuple containing:
        1. The original Python class name (e.g., `"ActorType"`).
        2. A snake_case conversion of the class name, suitable as a
           PostgreSQL type identifier (e.g., `"actor_type"`).
        3. The Enum class itself (for use in SQLAlchemy `sa.Enum` construction).

    The snake_case conversion is performed by `_snake_case()`, which ensures
    the generated SQL type name follows PostgreSQL's convention of using
    lowercase, underscore‑separated identifiers.

    Parameters:
        enum_class (type[Enum] | None): An optional specific Enum subclass to
            retrieve. If provided, the returned list will contain only that
            enum. If `None` (the default), all enums from `DB_ENUMS` are
            returned.

    Returns:
        list[tuple[str, str, type[Enum]]]: A list of tuples, each containing:
            - `python_name` (str): The original class name (e.g., `"UserRole"`).
            - `sql_name` (str): The snake_case SQL type name (e.g., `"user_role"`).
            - `enum_class` (type[Enum]): The actual Enum class.

    Raises:
        This function does not raise any exceptions directly. However, if
        `enum_class` is provided and is not a valid `Enum` subclass,
        subsequent usage may lead to errors elsewhere.

    Usage examples:
        # Get all registered enums
        all_enums = _get_enum()

        # Get a single enum by class
        actor_enum = _get_enum(ActorType)

        # In a migration (from enums.py):
        for _, enum_name, cls in _get_enum():
            sa_enum = sa.Enum(cls, name=enum_name, ...)
            sa_enum.create(conn, checkfirst=True)

    Notes:
        - The `DB_ENUMS` list is the authoritative source of enum types
          that are managed by the application. Any new enum that should be
          persisted in the database must be added to this list.
        - The snake_case naming is critical for consistency: the SQL type
          name must match the name used in `CREATE TYPE` statements and in
          column type definitions (e.g., `Column(sa.Enum(ActorType, name="actor_type"))`).
        - This function is also used by the downgrade migration to drop
          types, ensuring the same naming logic is applied consistently.
        - The return type order (name, snake_case, class) is intentionally
          chosen to match the expected tuple format in `enums.py` where the
          loop unpacks as `(_, enum, cls)`.
    """
    if enum_class is not None:
        enum_list: list[type[Enum]] = [enum_class]
    else:
        enum_list = DB_ENUMS
    
    return [
        (cls.__name__, _snake_case(cls.__name__), cls) for cls in enum_list
    ]