from __future__ import annotations
from typing import Any, TYPE_CHECKING

from sqlalchemy import String, Boolean, CheckConstraint, false
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from sqlalchemy.schema import SchemaItem
    
from mdls.base.base import Base, db_enum, IdMixin, NotesMixin, TimestampMixin, TablenameMixin, UUIDMixin, ReprMixin
from utils.utils.name import _secondary_ref
from utils.enums import Region

if TYPE_CHECKING:
    from core import Actor, Event, CountryEvent

class Country(    
    Base, 
    TablenameMixin,
    IdMixin, 
    UUIDMixin,
    NotesMixin, 
    TimestampMixin,
    ReprMixin
    ):
    """
    Stores country data for analysis, focusing on ASEAN members and their key dialogue partners.
    A Country represents an abstract nation‑state (e.g., "Malaysia", "United States") and is
    distinct from `Actor`, which models specific organisational entities (e.g., "Malaysian
    Ministry of Defence").

    Inherited mixins provide standard functionality:
        - ``TablenameMixin`` : auto‑generates ``__tablename__`` from the class name.
        - ``IdMixin``        : integer primary key column ``id``.
        - ``UUIDMixin``      : universally unique identifier ``uuid``.
        - ``NotesMixin``     : ``notes`` (Text) column for unstructured analyst remarks.
        - ``TimestampMixin`` : ``created_at`` and ``updated_at`` datetime columns.
        - ``ReprMixin``      : ``__repr__`` that uses ``__repr_fields__``.

    .. note::

        The string representation is based on ``('id', 'country_name', 'region')``.

    **Table‑level constraints and settings:**

    - ``UniqueConstraint`` on ``country_name``, ``iso_alpha_2``, and ``iso_alpha_3``:
        Each field is individually unique.
    - ``CheckConstraint("iso_alpha_2 = UPPER(iso_alpha_2) AND iso_alpha_3 = UPPER(iso_alpha_3)")``:
        Forces ISO codes to be stored in uppercase for consistency.
    - ``CheckConstraint("LENGTH(iso_alpha_2) = 2 AND LENGTH(iso_alpha_3) = 3")``:
        Ensures ISO codes have the correct length.
    - ``CheckConstraint("TRIM(country_name) != '' AND (notes IS NULL OR TRIM(notes) != '')")``:
        Prevents empty or whitespace‑only country names; notes, if provided, must not be empty.
    - Table comment: describes the purpose of the table.

    **Columns:**

        country_name : ``String(100)``, **not null**, **unique**
            Official name of the country (e.g., "Vietnam", "United Kingdom").
        iso_alpha_2 : ``String(2)``, **not null**, **unique**
            ISO 3166‑1 alpha‑2 country code (e.g., "VN", "GB"). Stored uppercase.
        iso_alpha_3 : ``String(3)``, **not null**, **unique**
            ISO 3166‑1 alpha‑3 country code (e.g., "VNM", "GBR"). Stored uppercase.
        region : ``Region`` enum, **not null**
            Geographic region classification (e.g., ``Region.MAINLAND_SE_ASIA``,
            ``Region.EAST_ASIA``). Uses a database enum for integrity.
        asean_member : ``bool``, **not null**, default ``False``
            Flag indicating whether the country is an ASEAN member state.
        notes : ``Text``, nullable (from ``NotesMixin``)
            Free‑text analyst remarks. Enforced non‑empty if provided.

    **Relationships:**

        events : ``list[Event]`` (many‑to‑many, **viewonly**)
            Events associated with this country. Uses the ``country_event`` secondary
            table. Loaded lazily (``lazy='select'``). Because the relationship is
            view‑only, modifications must go through the association object
            (``event_associations``).
        actors : ``list[Actor]`` (one‑to‑many, **viewonly**)
            Actors that are primarily affiliated with this country (via
            ``Actor.country_id``). Lazy‑loaded.
        event_associations : ``list[CountryEvent]`` (one‑to‑many, **writable**)
            Association objects linking countries to events. These can store additional
            data (e.g., role, confidence). This is the intended path for creating or
            removing country‑event links.

    **Loading strategies and performance considerations:**

        All relationships use ``lazy='select'`` (load on first access). This is safe
        for single‑object operations but **will cause the N+1 query problem** when
        iterating over collections of countries. For any query that returns multiple
        countries, always apply eager loading:

        .. code-block:: python

            from sqlalchemy.orm import selectinload

            countries = (
                session.query(Country)
                .options(
                    selectinload(Country.events),
                    selectinload(Country.actors),
                )
                .all()
            )

        For bulk inserts/updates where server defaults are not required, uncomment the
        ``eager_defaults = False`` mapper argument to avoid per‑row roundtrips.

    **Usage examples:**

        Create a new country:

        >>> vietnam = Country(
        ...     country_name="Vietnam",
        ...     iso_alpha_2="VN",
        ...     iso_alpha_3="VNM",
        ...     region=Region.MAINLAND_SE_ASIA,
        ...     asean_member=True
        ... )
        >>> session.add(vietnam)
        >>> session.commit()

        Link a country to an event through the writable association:

        >>> from . import CountryEvent
        >>> assoc = CountryEvent(country=vietnam, event=some_event, impact_level="high")
        >>> session.add(assoc)
        >>> session.commit()

    .. seealso::
        :class:`Actor`
        :class:`Event`
        :class:`CountryEvent`
    """
    __repr_fields__ = ('id', 'country_name', 'region')
    
    @declared_attr
    def __mapper_args__(cls) -> Any:
        args: Any = super().__mapper_args__.copy()
        # args["eager_defaults"] = False
        return args
    
    __table_args__: tuple[SchemaItem | dict[str, Any], ...] = (
        CheckConstraint(
            "iso_alpha_2 = UPPER(iso_alpha_2) AND iso_alpha_3 = UPPER(iso_alpha_3)",
            name="ck_countries_iso_upper_case"
        ),
        CheckConstraint(
            "LENGTH(iso_alpha_2) = 2 AND LENGTH(iso_alpha_3) = 3",
            name="ck_countries_iso_length"
        ),
        CheckConstraint(
            "TRIM(country_name) != '' AND (notes IS NULL OR TRIM(notes) != '')",
            name="ck_countries_fields_non_empty"
        ),

        {'comment': 'Stores country data for analysis, focusing on ASEAN members and their key dialogue partners.'}
    )
    
    country_name: Mapped[str] = mapped_column(
        String(100), 
        unique=True,
        nullable=False, 
        comment='Official name of the country. Must be UNIQUE.'
    )
    
    iso_alpha_2: Mapped[str] = mapped_column(
        String(2), 
        unique=True,
        nullable=False, 
        comment='ISO 3166-1 alpha-2 country code. UNIQUE.'
    )
    
    iso_alpha_3: Mapped[str] = mapped_column(
        String(3), 
        unique=True,
        nullable=False, 
        comment='ISO 3166-1 alpha-3 country code. UNIQUE.'
    )
    
    region: Mapped[Region] = mapped_column(
        db_enum(Region),
        nullable=False,
        comment='Geographic region for grouping data (Mainland Southeast Asia, Maritime Southeast Asia, East Asia, South Asia, Oceania, North America, Europe, Other).'
    )
    
    asean_member: Mapped[bool] = mapped_column(
        Boolean(), 
        nullable=False, 
        default=False,
        server_default=false(),
        comment='BOOLEAN flag indicating ASEAN membership status.'
    )
    
    events: Mapped[list[Event]] = relationship(
        'Event', 
        secondary=_secondary_ref(Base.metadata, 'country_event'), 
        back_populates='countries',
        lazy='select',
        uselist=True,
        viewonly=True
    )
    
    actors: Mapped[list[Actor]] = relationship(
        'Actor',
        back_populates='country',
        lazy='select',
        uselist=True,
        viewonly=True
    )
    
    event_associations: Mapped[list[CountryEvent]] = relationship(
        'CountryEvent',
        lazy='select',
        uselist=True,
        viewonly=False
    )
