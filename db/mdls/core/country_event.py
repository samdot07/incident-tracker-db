from __future__ import annotations
from typing import Any, TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, PrimaryKeyConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import SchemaItem
    
from mdls.base.base import Base, varchar_enum, NotesMixin, TablenameMixin, ReprMixin
from utils.utils.name import _fk_ref
from utils.enums import InvolvementType

if TYPE_CHECKING:
    from core import Country, Event

class CountryEvent(    
    Base,  
    TablenameMixin,
    NotesMixin,
    ReprMixin
    ):
    """
    Represents the many-to-many relationship between a ``Country`` and an ``Event``,
    including the nature of the country's involvement (e.g., victim, perpetrator,
    observer, affected territory). This association object allows additional
    attributes beyond a simple link table, such as ``involvement_type``.

    Inherited mixins provide standard functionality:
        - ``TablenameMixin`` : auto-generates ``__tablename__`` from the class name.
        - ``NotesMixin``     : ``notes`` (Text) column for unstructured analyst remarks.
        - ``ReprMixin``      : ``__repr__`` that uses ``__repr_fields__``.

    .. note::

        The string representation is based on ``('event_id', 'country_id', 'involvement_type')``.

    **Table-level constraints and settings:**

    - ``PrimaryKeyConstraint('event_id', 'country_id')`` :
        The composite primary key ensures each (event, country) pair is unique.
    - ``CheckConstraint(TRIM(notes) != '' OR notes IS NULL)`` :
        If ``notes`` are provided, they must not be empty/whitespace-only strings.
    - Table comment : describes the table as the junction linking events to
      participating/affected countries.

    **Columns:**

        event_id : ``int``, **not null**, part of PK
            Foreign key to ``event.id``. **ON DELETE CASCADE** – if the referenced
            event is deleted, this association is automatically removed.
        country_id : ``int``, **not null**, part of PK
            Foreign key to ``country.id``. **ON DELETE CASCADE** – if the referenced
            country is deleted, this association is automatically removed.
        involvement_type : ``InvolvementType`` enum, **not null**
            Categorical classification of how the country was involved (e.g.,
            ``VICTIM``, ``PERPETRATOR``, ``AFFECTED_TERRITORY``, ``OBSERVER``).
            Stored as a database-backed enum or varchar constraint, depending on
            ``varchar_enum()`` implementation.
        notes : ``Text``, nullable (from ``NotesMixin``)
            Additional contextual remarks about the country's specific role in the
            event.

    **Relationships:**

        event : ``Event`` (many-to-one, **writable**)
            The associated ``Event`` instance. This relationship back-populates
            ``Event.country_associations``. Loaded lazily (``lazy='select'``).
            It is writable – you can assign an ``Event`` directly to this
            association object.
        country : ``Country`` (many-to-one, **writable**)
            The associated ``Country`` instance. Back-populates
            ``Country.event_associations``. Also writable and lazily loaded.

    **Loading strategies and performance considerations:**

        All relationships use ``lazy='select'`` (load on first access). This is safe
        for single-object work but **will cause the N+1 query problem** when iterating
        over collections of associations. For any query that returns multiple
        ``CountryEvent`` rows, always apply eager loading if you know you will access
        the related ``event`` or ``country``:

        .. code-block:: python

            from sqlalchemy.orm import selectinload

            associations = (
                session.query(CountryEvent)
                .options(selectinload(CountryEvent.event), selectinload(CountryEvent.country))
                .filter(CountryEvent.involvement_type == InvolvementType.VICTIM)
                .all()
            )

        This table is intended as a pure association (junction). In most access
        patterns, you will query it indirectly via ``Event.country_associations`` or
        ``Country.event_associations``. Ensure those parent relationships also use
        appropriate eager loading when traversing large collections.

    **Usage examples:**

        Create a new association linking an existing event and country:

        >>> from yourapp.models import Event, Country, CountryEvent, InvolvementType
        >>> event = session.get(Event, 101)
        >>> country = session.get(Country, 42)
        >>> association = CountryEvent(
        ...     event=event,
        ...     country=country,
        ...     involvement_type=InvolvementType.VICTIM,
        ...     notes="Sustained economic damage due to cyber attack"
        ... )
        >>> session.add(association)
        >>> session.commit()

        Query all events where a specific country was a perpetrator:

        >>> perpetrator_assocs = (
        ...     session.query(CountryEvent)
        ...     .filter(
        ...         CountryEvent.country_id == 42,
        ...         CountryEvent.involvement_type == InvolvementType.PERPETRATOR
        ...     )
        ...     .all()
        ... )
        >>> events = [assoc.event for assoc in perpetrator_assocs]  # N+1 – use eager loading

    **Important design notes:**

        - This table uses **composite primary key** instead of a surrogate ``id``
          column. This is appropriate for a pure many-to-many association with
          additional attributes, as it enforces uniqueness naturally and avoids
          an unnecessary auto-increment column.
        - ``ON DELETE CASCADE`` on both foreign keys ensures that deleting an
          ``Event`` or ``Country`` automatically cleans up its junction rows,
          maintaining referential integrity without application-level logic.
        - The ``notes`` column is validated at the database level (via
          ``CheckConstraint``) to prevent empty whitespace strings, but allows
          ``NULL`` as “no comment”.

    .. seealso::
        :class:`Event`
        :class:`Country`
        :class:`InvolvementType` (enum)
    """
    __repr_fields__ = ('event_id', 'country_id', 'involvement_type')
    
    __table_args__: tuple[SchemaItem | dict[str, Any], ...] = (
        PrimaryKeyConstraint(
            'event_id', 'country_id',
            name="pk_country_events"
        ),

        CheckConstraint(
            "(notes IS NULL OR TRIM(notes) != '')",
            name="ck_country_event_fields_non_empty"
        ),

        {'comment': 'Junction table linking events to participating/affected countries'}
    )

    event_id: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey(_fk_ref(Base.metadata, 'event.id'), ondelete='CASCADE'),
        nullable=False,
        comment='FOREIGN KEY referencing Events table.'
    )
    
    country_id: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey(_fk_ref(Base.metadata, 'country.id'), ondelete='CASCADE'),
        nullable=False,
        comment='FOREIGN KEY referencing Countries table.'
    )
    
    involvement_type: Mapped[InvolvementType] = mapped_column(
        varchar_enum(InvolvementType),
        nullable=False,
        comment='Nature of involvement. Must not be NULL'
    )
    
    event: Mapped['Event'] = relationship(
        back_populates='country_associations',
        lazy='select',
        uselist=False,
        viewonly=False
    )
    
    country: Mapped['Country'] = relationship(
        back_populates='event_associations',
        lazy='select',
        uselist=False,
        viewonly=False
    )