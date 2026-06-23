from __future__ import annotations
from typing import Any, TYPE_CHECKING

from sqlalchemy import Integer, String, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from sqlalchemy.schema import SchemaItem
from geoalchemy2 import Geography
from geoalchemy2.elements import WKBElement
    
from mdls.base.base import Base, db_enum, IdMixin, NotesMixin, TimestampMixin, TablenameMixin, UUIDMixin, ReprMixin
from utils.utils.name import _fk_ref
from utils.enums import LocationType

if TYPE_CHECKING:
    from core import Event
    
class Location(    
    Base,
    TablenameMixin, 
    IdMixin, 
    UUIDMixin,
    NotesMixin, 
    TimestampMixin,
    ReprMixin
    ):
    """
    Represents a specific geographic point or area where an incident (event) occurs.
    Unlike the abstract `Country` (nation‑state model), `Location` captures concrete
    places such as cities, military bases, maritime zones, or disputed territories.
    It optionally includes a PostGIS geography point for precise coordinates.

    Inherited mixins provide standard functionality:
        - ``TablenameMixin`` : auto‑generates ``__tablename__`` from the class name.
        - ``IdMixin``        : integer primary key column ``id``.
        - ``UUIDMixin``      : universally unique identifier ``uuid``.
        - ``NotesMixin``     : ``notes`` (Text) column for unstructured analyst remarks.
        - ``TimestampMixin`` : ``created_at`` and ``updated_at`` datetime columns.
        - ``ReprMixin``      : ``__repr__`` that uses ``__repr_fields__``.

    .. note::

        The string representation is based on ``('id', 'location_name', 'location_type')``.

    **Table‑level constraints:**

    - ``CheckConstraint(TRIM(location_name) != '' AND …)`` :
        Ensures ``location_name`` is never an empty/whitespace string, and that
        ``description`` and ``notes`` are either NULL or non‑empty after trimming.
    - Table comment : describes the purpose of the ``location`` table.

    **Columns:**

        location_name : ``String(200)``, **not null**
            Geographic feature or area name (e.g., "South China Sea", "Port of Shanghai",
            "Donbas Region").
        coordinates : ``Geography('POINT', srid=4326)``, nullable
            Optional PostGIS geography point (longitude/latitude in WGS84).
            Use for precise locations (e.g., a specific military base). Nullable for
            approximate or regional designations.
        location_type : ``LocationType`` enum, **not null**
            Categorical classification for pattern analysis, e.g.,
            ``DISPUTED_ISLAND``, ``MARITIME_FEATURE``, ``BORDER_REGION``,
            ``CAPITAL_CITY``, ``MILITARY_INSTALLATION``, ``ECONOMIC_ZONE``,
            ``INTERNATIONAL_WATERS``, ``OTHER``.
        country_id : ``int`` or ``None``
            Foreign key to ``country.id``. **ON DELETE SET NULL** – if the referenced
            country is deleted, the column becomes NULL, preserving the location record.
            Nullable for disputed territories or international waters not owned by any
            single country.
        description : ``Text``, nullable
            Free‑form contextual details for analyst disambiguation.
        notes : ``Text``, nullable (from ``NotesMixin``)
            Additional remarks.

    **Relationships:**

        events : ``list[Event]`` (one‑to‑many, **viewonly**)
            All events that occurred at this location. Because the relationship is
            view‑only, modifications must be made via the ``Event.location_id`` foreign
            key or by directly assigning an ``Event`` to a location.

    **Loading strategies and performance considerations:**

        The ``events`` relationship uses ``lazy='select'`` (load on first access).
        This is safe for single‑object operations but **will cause the N+1 query
        problem** when iterating over collections of locations. For any query that
        returns multiple locations and requires event data, apply eager loading:

        .. code-block:: python

            from sqlalchemy.orm import selectinload

            locations = (
                session.query(Location)
                .options(selectinload(Location.events))
                .all()
            )

        For bulk inserts/updates where server‑generated defaults are not required,
        uncomment ``eager_defaults = False`` in the mapper arguments to avoid
        per‑row roundtrips.

    **Usage examples:**

        Create a new precise location with coordinates:

        >>> from geoalchemy2 import Geography
        >>> from shapely.geometry import Point
        >>>
        >>> location = Location(
        ...     location_name="Naval Base Guam",
        ...     location_type=LocationType.MILITARY_INSTALLATION,
        ...     coordinates=Point(144.7937, 13.4443),  # longitude, latitude
        ...     country_id=usa.id,
        ...     description="Major US naval facility in the Pacific"
        ... )
        >>> session.add(location)
        >>> session.commit()

        Associate an event with this location:

        >>> event = Event(
        ...     title="Naval Exercise",
        ...     location_id=location.id,
        ...     ...
        ... )
        >>> session.add(event)
        >>> session.commit()

    .. seealso::
        :class:`Country`
        :class:`Event`
        :class:`Actor`
    """
    __repr_fields__ = ('id', 'location_name', 'location_type')
    
    @declared_attr
    def __mapper_args__(cls) -> Any:
        args: Any = super().__mapper_args__.copy()
        # args["eager_defaults"] = False
        return args
    
    __table_args__: tuple[SchemaItem | dict[str, Any], ...] = (
        CheckConstraint(
            "TRIM(location_name) != '' AND (description IS NULL OR TRIM(description) != '') AND (notes IS NULL OR TRIM(notes) != '')",
            name="ck_locations_fields_non_empty"
        ),

        {'comment': 'Models specific geographic points or areas where incidents occur.'}
    )
    
    location_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment='Geographic feature or area name.'
    )
    
    coordinates: Mapped[WKBElement | None] = mapped_column(
        Geography('POINT', srid=4326),
        nullable=True,
        comment='PostGIS GEOGRAPHY point (lat/long in WGS84). Nullable for approximate/regional coordinates.'
    )
    
    location_type: Mapped[LocationType] = mapped_column(
        db_enum(LocationType),
        nullable=False,
        comment='Classification for pattern analysis (Disputed Island, Maritime Feature, Border Region, Capital City, Military Installation, Economic Zone, International Waters, Other).'
    )
    
    country_id: Mapped[int | None] = mapped_column(
        Integer(),
        ForeignKey(_fk_ref(Base.metadata, 'country.id'), ondelete='SET NULL'),
        nullable=True,
        comment='FOREIGN KEY to countries table. Nullable for disputed territories or international waters.'
    )
    
    description: Mapped[str | None] = mapped_column(
        Text(),
        nullable=True,
        comment='Contextual details for analyst understanding and disambiguation.'
    )
    
    events: Mapped[list[Event]] = relationship(
        'Event', 
        back_populates='location',
        lazy='select',
        uselist=True,
        viewonly=True
    ) 