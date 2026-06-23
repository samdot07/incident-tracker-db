from __future__ import annotations
from typing import Any, ClassVar
from datetime import datetime
import uuid

from sqlalchemy import MetaData, DateTime, func, FetchedValue, Integer, UUID, Identity, Text, text, Enum as SAEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
import inflect
from enum import Enum

from src.config.config import Settings, get_settings
from utils.utils.metadata import _get_schema
from utils.utils.name import _snake_case

_convention: dict[str, str] = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_N_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

_settings: Settings = get_settings()

class Base(DeclarativeBase):
    """
    Primary base class for all SQLAlchemy ORM models in the application.

    This class extends SQLAlchemy's `DeclarativeBase` and provides a custom
    `MetaData` instance pre‑configured with:

        - The target database schema as defined in application settings
          (`_settings.DB_SCHEMA`).
        - A consistent naming convention for all constraints and indexes,
          ensuring that generated names are predictable and follow a standard
          pattern (e.g., `fk_<table>_<column>_<referred_table>`).

    By inheriting from this base, every model automatically uses the same
    schema and naming rules, eliminating repetitive configuration and
    improving maintainability.

    Attributes:
        metadata (MetaData): A SQLAlchemy `MetaData` object with the
            `naming_convention` and `schema` already set. This is shared
            across all models.

    Usage:
        >>> from sqlalchemy.orm import Mapped, mapped_column
        >>> class User(Base):
        ...     __tablename__ = "users"   # optional if using TablenameMixin
        ...     name: Mapped[str]

    Note:
        - The `metadata.schema` is taken from `settings.DB_SCHEMA` and
          is used for all tables, sequences, and constraints.
        - The naming conventions are applied automatically by SQLAlchemy
          when creating constraints and indexes.
        - For custom schemas per model, override `__table_args__` with
          `{'schema': 'other_schema'}`.
    """
    metadata = MetaData(
        naming_convention=_convention, 
        schema=_settings.DB_SCHEMA
    )
    
_engine = inflect.engine()

class TablenameMixin:
    """
    Mixin that automatically generates a pluralised table name from the model
    class name using `inflect`.

    This mixin eliminates the need to manually write `__tablename__` in every
    model. The table name is derived by:

        1. Converting the class name to snake_case (e.g., `UserProfile` → `user_profile`).
        2. Pluralising the snake‑cased name (e.g., `user_profile` → `user_profiles`).

    The generation uses `declared_attr.directive` so that it works correctly
    with SQLAlchemy's inheritance and mapping machinery.

    Attributes:
        __tablename__ (str): Automatically generated; not to be set manually
            unless you want to override the default.

    Usage:
        >>> class UserProfile(TablenameMixin, Base):
        ...     # __tablename__ becomes "user_profiles"
        ...     bio: Mapped[str]

    Important:
        - If a model explicitly defines `__tablename__`, this mixin is
          ignored (the explicit attribute takes precedence).
        - The pluralisation uses `inflect.engine().plural()`, which handles
          irregular plurals (e.g., `person` → `people`) correctly.
        - Ensure the generated name matches the expectations of any foreign
          key references (e.g., in `_fk_ref` and `_secondary_ref`).

    See Also:
        `_snake_case()` in `name.py` for the conversion logic.
    """
    @declared_attr # type: ignore
    def __tablename__(cls) -> str:
        return _engine.plural(_snake_case(cls.__name__)) # type: ignore
    
class IdMixin:
    """
    Mixin that adds an auto‑incrementing integer primary key column.

    Columns:
        - `id` (int): Auto‑incrementing primary key, using PostgreSQL's
          `IDENTITY` (generated always as identity). This is the modern,
          recommended way for auto‑increment columns in PostgreSQL,
          replacing the older `SERIAL` or `BIGSERIAL` types.

    Behaviour:
        - The column starts at 1 and increments by 1 for each new row.
        - The `IDENTITY` property ensures that the value is always generated
          by the database, even during bulk inserts.
        - The column is the primary key and is non‑nullable.

    Usage:
        >>> class Product(IdMixin, Base):
        ...     name: Mapped[str]
        >>> # Product.id exists and is automatically populated.

    Notes:
        - This mixin is often combined with `UUIDMixin` for a public
          identifier while keeping `id` as an internal, sequential key.
        - Do not set a value for `id` in application code; the database
          will assign it.
        - For composite primary keys, do not use this mixin; define the
          columns explicitly.
    """
    id: Mapped[int] = mapped_column(
        Integer(),
        Identity(always=True, start=1, increment=1),
        primary_key=True,
        comment='Auto-incrementing PRIMARY KEY.'
    )
    
class UUIDMixin:
    """
    Mixin that adds a UUID column suitable for external/public identifiers.

    Columns:
        - `uuid` (uuid.UUID): A unique, non‑nullable UUID that is automatically
          generated for each new record.

    Behaviour:
        - The Python‑side default uses `uuid.uuid4()` (random UUID).
        - A server‑side default (`gen_random_uuid()`) is also set to ensure
          uniqueness even when rows are inserted via raw SQL or by other
          clients that do not supply a UUID.
        - The column is marked `unique=True` and `nullable=False`.

    Usage:
        Use this mixin when you need a public identifier that is not
        sequential and should not expose internal row counts. This is ideal
        for API endpoints, external references, or any context where
        predictability is undesirable.

    Example:
        >>> class Organization(UUIDMixin, Base):
        ...     name: Mapped[str]
        >>> org = Organization(name="ACME")
        >>> session.add(org)
        >>> session.flush()
        >>> print(org.uuid)   # e.g., 123e4567-e89b-12d3-a456-426614174000

    Notes:
        - The `UUID` type is configured with `as_uuid=True`, so SQLAlchemy
          will automatically convert between Python `uuid.UUID` objects and
          the PostgreSQL `UUID` type.
        - Both defaults are applied: the Python default is used when the
          object is instantiated, and the server default is used by the
          database if the Python default is not set (e.g., during bulk
          inserts where the ORM is bypassed).
    """
    uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        unique=True,
        nullable=False
    )
    
class NotesMixin:
    """
    Mixin that adds a free‑text notes column to a model.

    Columns:
        - `notes` (str | None): A text column for storing unstructured
          supplementary observations or comments. Nullable by default.

    Usage:
        Use this mixin on models that may need to store extra remarks,
        such as audit logs, administrative notes, or descriptive metadata
        that does not fit into other columns.

    Example:
        >>> class Transaction(NotesMixin, Base):
        ...     amount: Mapped[Decimal]
        >>> tx = Transaction(amount=99.99, notes="Refund processed manually")
        >>> session.add(tx)

    Notes:
        - The column is stored as `TEXT` in PostgreSQL, which can hold
          large amounts of text.
        - There is no length limit defined; if a limit is needed, override
          the column by redeclaring it in the subclass with a `String(255)`.
        - The column is nullable by default; if you require notes, you can
          set `nullable=False` in the subclass.
    """
    notes: Mapped[str | None] = mapped_column(
        Text(),
        nullable=True,
        comment='Supplementary observations. Nullable.'
    )
    
class TimestampMixin: 
    """
    Mixin that adds `created_at` and `updated_at` timestamp columns with
    automatic management.

    Columns:
        - `created_at` (datetime): Set to the current timestamp (with timezone)
          when a record is inserted. Uses PostgreSQL's `NOW()` via
          `server_default=func.now()`.
        - `updated_at` (datetime): Initially set to the creation timestamp and
          updated on every row modification. The update is performed by a
          database trigger (not by the ORM), using `server_onupdate=FetchedValue()`.
          The ORM will fetch the new value immediately after the update.

    Configuration:
        - `__eager_defaults__ = True` is set on the mixin, forcing SQLAlchemy
          to refresh default values from the database immediately after
          INSERT/UPDATE operations. This prevents stale timestamps in the
          ORM identity map.
        - The mixin overrides `__mapper_args__` to apply `eager_defaults`
          globally to any model that uses it.

    Important:
        - A database trigger (e.g., `update_tg`) must be created separately
          to update the `updated_at` column on `BEFORE UPDATE`. This is
          typically handled by the migrations in `migrs.funcs` and `migrs.trgs`.
        - If you prefer to use the ORM's `onupdate` parameter instead of a
          trigger, remove the `server_onupdate=FetchedValue()` and add
          `onupdate=func.now()`. However, the trigger approach is more robust
          for bulk updates and raw SQL operations.

    Usage:
        >>> class Article(TimestampMixin, Base):
        ...     title: Mapped[str]
        >>> article = Article(title="Hello")
        >>> session.add(article)
        >>> session.flush()
        >>> print(article.created_at)   # current timestamp
        >>> article.title = "Hello World"
        >>> session.flush()
        >>> print(article.updated_at)   # updated timestamp (via trigger)

    Notes:
        - Both columns are `DateTime(timezone=True)` to store timezone‑aware
          timestamps, which is highly recommended for production databases.
        - The `server_onupdate=FetchedValue()` tells SQLAlchemy to fetch
          the database‑generated value after an UPDATE, but it does not
          generate a `DEFAULT` clause itself; that is why the trigger is
          required.
        - If you are using `create_all()` for tests, you may need to
          manually create the trigger function and triggers after the tables
          are created.
    """
    __eager_defaults__: ClassVar[bool] = True
    
    @declared_attr # type: ignore
    def __mapper_args__(cls) -> dict[str, object]:
        return {"eager_defaults": cls.__eager_defaults__}
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment='TIMESTAMP when the record was created (automatically set).'
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=FetchedValue(),
        nullable=False,
        comment='TIMESTAMP of the most recent update (set by TRIGGER). Initially set to creation time; updated by trigger on every subsequent modification.'
    )
    
class ReprMixin:
    """
    Mixin that provides a safe `__repr__` implementation that never triggers
    lazy loading of relationships.

    Attributes (class‑level):
        - `__repr_fields__` (tuple[str, ...]): Defines which attribute names
          should be included in the representation. Defaults to `('id',)`.
          Override this in your model to include additional fields.

    Behaviour:
        - The `__repr__` method iterates over `__repr_fields__` and fetches
          each attribute via `getattr(self, name, None)`.
        - If the attribute value has a `name` property (e.g., a related
          model), it substitutes that `name` for the value to avoid recursive
          or lazy‑loading issues.
        - The resulting string follows the pattern:
          `<ClassName(field1=value1, field2=value2)>`.

    Usage:
        Include this mixin in any model where you want a clean, non‑intrusive
        representation for debugging or logging. It is especially useful in
        development environments to quickly inspect objects.

    Example:
        >>> class User(ReprMixin, Base):
        ...     __repr_fields__ = ('id', 'email', 'profile.name')
        ...     email: Mapped[str]
        ...     profile: Mapped["Profile"] = relationship(back_populates="user")
        >>> user = User(id=42, email="alice@example.com")
        >>> user.profile = Profile(name="Alice")
        >>> repr(user)
        '<User(id=42, email='alice@example.com', profile.name='Alice')>'

    Notes:
        - The `__repr_fields__` tuple can contain dotted names (e.g.,
          `'profile.name'`), but the mixin will only attempt a simple
          `getattr(self, name, None)`. Dotted names are not resolved
          automatically; you must handle them manually if needed.
        - The fallback for `hasattr(value, 'name')` is a common pattern
          for handling relationship objects that have a `name` attribute.
          This avoids the need to load the entire relationship.
        - If a field is not present (e.g., due to lazy loading failure),
          `None` is used.
    """
    __repr_fields__: tuple[str, ...] = ('id',)
    
    def __repr__(self) -> str:
        fields: list[Any] = []
        for n in self.__repr_fields__:
            value: Any = getattr(self, n, None)
            if hasattr(value, 'name'):
                value: Any = value.name
            fields.append(f"{n}={value!r}")
        return  f"<{type(self).__name__}({', '.join(fields)})>"

    
def db_enum(enum_class: type[Enum]) -> SAEnum:
    """
    Create a PostgreSQL native ENUM type from a Python Enum class.

    This function returns a SQLAlchemy `Enum` construct configured to use the
    database's native `CREATE TYPE ... AS ENUM`. The enum type name is derived
    from the Python enum class name via `_snake_case()`.

    Parameters:
        enum_class (type[Enum]): A Python `enum.Enum` subclass whose members
            define the allowed values for the database enum.

    Returns:
        SAEnum: A configured SQLAlchemy `Enum` construct, ready for use in
            `mapped_column()`.

    Configuration:
        - `create_type=False`: The enum type is assumed to already exist in
          the database. This prevents SQLAlchemy from automatically creating
          the type when `Base.metadata.create_all()` is called, which is
          desirable because migrations should handle type creation.
        - `native_enum=True`: Ensures PostgreSQL's native enum type is used,
          providing type safety, validation, and space efficiency.

    Usage:
        >>> from enum import Enum
        >>> class UserRole(Enum):
        ...     ADMIN = "admin"
        ...     EDITOR = "editor"
        >>> class User(Base):
        ...     role: Mapped[UserRole] = mapped_column(db_enum(UserRole))

    Important:
        - The corresponding PostgreSQL enum type **must** be created in the
          database before the table referencing it is created. This is
          typically done in an Alembic migration (e.g., `migrs.enums.enums`).
        - Set `create_type=True` only if you are using `create_all()` in a
          test environment and want SQLAlchemy to manage the type creation.
        - The enum values are stored as text in the database; adding a new
          value to the enum requires an `ALTER TYPE ... ADD VALUE` migration.

    See Also:
        `varchar_enum()` for a non‑native alternative.
        `_get_enum()` in `registry.py` for the list of all registered enums.
    """
    return SAEnum(
        enum_class,
        name=_snake_case(enum_class.__name__),
        schema=_get_schema(Base.metadata),
        create_type=False,
        native_enum=True
    ) 
      
def varchar_enum(enum_class: type[Enum]) -> SAEnum:
    """
    Create a SQLAlchemy Enum column that stores values as plain VARCHAR/text,
    without creating a database native ENUM type.

    This function returns a SQLAlchemy `Enum` construct that does **not**
    use PostgreSQL's `CREATE TYPE ... AS ENUM`. Instead, the column will be
    stored as a text/varchar type (e.g., `VARCHAR`), with validation performed
    only at the application level (by SQLAlchemy when values are assigned).

    Parameters:
        enum_class (type[Enum]): A Python `enum.Enum` subclass whose members
            define the allowed values.

    Returns:
        SAEnum: A configured SQLAlchemy `Enum` construct that does not create
            a database constraint and uses `native_enum=False`.

    Configuration:
        - `create_constraint=False`: No database CHECK constraint is generated.
          Validation is enforced only by the Python enum when the value is
          set on the model instance.
        - `native_enum=False`: Forces the column to be stored as a text type
          (e.g., `VARCHAR` in PostgreSQL) instead of a native ENUM.

    When to use:
        - In high‑write throughput tables where altering a native ENUM is
          expensive (requires a table rewrite or lock).
        - For enums that may change frequently (adding or removing values)
          and you want to avoid migration complexity.
        - For many‑to‑many association tables or other contexts where the
          enum is less critical.
        - When you need to support PostgreSQL versions that do not have
          native enum support (though this is rarely a concern with modern
          versions).

    Example:
        >>> class PaymentStatus(Enum):
        ...     PENDING = "pending"
        ...     PAID = "paid"
        ...     FAILED = "failed"
        >>> class OrderItem(Base):
        ...     status: Mapped[PaymentStatus] = mapped_column(varchar_enum(PaymentStatus))

    Important:
        - Since there is no database‑level validation, it is possible to
          insert invalid values via raw SQL. This is acceptable if the
          application controls all writes.
        - The column will be of type `VARCHAR` (or `TEXT` depending on the
          dialect) and will not benefit from the storage optimizations of
          native enums (e.g., the enum is stored as text, not an OID).
        - Sorting and ordering will be alphabetical, not based on enum order.

    See Also:
        `db_enum()` for a native PostgreSQL enum alternative.
    """
    return SAEnum(
        enum_class,
        name=_snake_case(enum_class.__name__),
        schema=_get_schema(Base.metadata),
        create_constraint=False,
        native_enum=False
    )   
    
