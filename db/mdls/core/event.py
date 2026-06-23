from __future__ import annotations
from datetime import date
from typing import Any, TYPE_CHECKING

from sqlalchemy import Integer, String, Text, Date, ForeignKey, CheckConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr 
from sqlalchemy.schema import SchemaItem 

from mdls.base.base import Base, db_enum, IdMixin, NotesMixin, TimestampMixin, TablenameMixin, UUIDMixin, ReprMixin
from utils.utils.name import _secondary_ref, _fk_ref
from utils.enums import AttributionConfidence

if TYPE_CHECKING:
    from core import Actor, Country, EventType, Location, Source, ImpactAssessment, EventActor, CountryEvent, EventSource

class Event(    
    Base, 
    TablenameMixin,
    IdMixin, 
    UUIDMixin,
    NotesMixin, 
    TimestampMixin,
    ReprMixin
    ):
    """
    Represents a discrete geopolitical incident that forms the primary unit of
    analysis. Events can have temporal duration (event_date + optional event_end_date),
    spatial attribution (location), a mandatory type classification, descriptive
    narrative, and confidence metadata for attribution.

    Inherited mixins provide standard functionality:
        - ``TablenameMixin`` : auto-generates ``__tablename__`` from the class name.
        - ``IdMixin``        : integer primary key column ``id``.
        - ``UUIDMixin``      : universally unique identifier ``uuid``.
        - ``NotesMixin``     : ``notes`` (Text) column for unstructured analyst remarks.
        - ``TimestampMixin`` : ``created_at`` and ``updated_at`` datetime columns.
        - ``ReprMixin``      : ``__repr__`` that uses ``__repr_fields__``.

    .. note::

        The string representations are based on ``('id', 'event_name', 'event_date')``.

    **Table‑level constraints and settings:**

    - ``CheckConstraint(event_end_date IS NULL OR event_end_date >= event_date)`` :
        Ensures that if an event has an end date, it is not earlier than the start date.
    - ``CheckConstraint(TRIM(event_name) != '' AND TRIM(description) != '' AND (notes IS NULL OR TRIM(notes) != ''))`` :
        Guarantees that ``event_name`` and ``description`` are never empty/whitespace
        strings, and that ``notes`` is either NULL or non‑empty after trimming.
    - Table comment : describes the table's role as the primary incident store.

    **Columns:**

        event_name : ``String(100)``, **not null**
            Concise, human‑readable name for the incident.
        event_date : ``Date``, **not null**
            Start date (or single date) of the event. No time component.
        event_end_date : ``Date``, nullable
            Optional end date for events that span multiple days (e.g., a military
            campaign, a conference). Must be ≥ ``event_date`` when provided.
        location_id : ``int`` or ``None``
            Foreign key to ``location.id``. **ON DELETE RESTRICT** – prevents deletion
            of a location that is referenced by an event. Nullable for events without
            precise spatial attribution (e.g., cyber incidents with unknown origin).
        event_type_id : ``int``, **not null**
            Foreign key to ``event_type.id``. **ON DELETE RESTRICT** – event types
            cannot be deleted while referenced by any event.
        description : ``Text``, **not null**
            Narrative summary of the incident, written by analysts.
        attribution_confidence : ``AttributionConfidence`` enum, **not null**
            Confidence level in the factual accuracy and actor attribution. Defaults
            to ``confirmed`` with a server‑side default to ensure consistency even
            when the column is omitted in INSERT statements.

    **Relationships (view‑only, many‑to‑many):**

        countries : ``list[Country]``
            Countries associated with this event via the ``country_event`` secondary
            table. Loaded lazily (``lazy='select'``). Read‑only – modifications must
            go through the association object (``country_associations``).
        actors : ``list[Actor]``
            Actors participating in the event via ``event_actor``. Loaded lazily.
            Read‑only – use ``actor_associations`` to modify links.
        location : ``Location | None``
            The geographical location of the event. **Eagerly loaded** with
            ``lazy='joined'`` because location is nearly always needed together
            with the event. Read‑only.
        event_type : ``EventType``
            The type classification of the event. **Eagerly loaded** (``lazy='joined'``)
            for the same reason – event type is fundamental to the event.
        sources : ``list[Source]``
            Information sources that report or substantiate the event, via the
            ``event_source`` secondary table. Lazy‑loaded, read‑only.
        impact_assessment : ``ImpactAssessment | None``
            Optional one‑to‑one assessment of the event's consequences (e.g.,
            economic, political, humanitarian). Lazy‑loaded.

    **Relationships (writable, association objects):**

        actor_associations : ``list[EventActor]``
            The writable link between events and actors, allowing additional
            attributes (e.g., role, certainty). This is the intended path for
            creating or removing event‑actor links.
        country_associations : ``list[CountryEvent]``
            Writable many‑to‑many link to countries, if extra data is needed on
            the association (otherwise consider using the view‑only ``countries``
            relationship with a simple secondary table).
        source_associations : ``list[EventSource]``
            Writable link to sources, again allowing per‑association metadata
            (e.g., relevance score, page references).

    **Loading strategies and performance considerations:**

        - Relationships **not** marked as ``lazy='joined'`` default to ``'select'``.
          This includes ``countries``, ``actors``, ``sources``, ``impact_assessment``,
          and the three association relationships.
        - To avoid the N+1 query problem when iterating over multiple events, use
          :func:`~sqlalchemy.orm.selectinload` for collection relationships:

          .. code-block:: python

              from sqlalchemy.orm import selectinload

              events = (
                  session.query(Event)
                  .options(
                      selectinload(Event.actors),
                      selectinload(Event.countries),
                      selectinload(Event.sources),
                  )
                  .all()
              )

        - The ``location`` and ``event_type`` relationships use ``lazy='joined'``
          because they are almost always accessed together with the event. This
          trades a single extra JOIN for eliminating subsequent queries. It is
          generally optimal for many‑to‑one references that are rarely NULL.
        - For bulk insert/update operations where server defaults are not needed,
          uncomment the ``eager_defaults = False`` mapper argument to avoid
          per‑row round‑trips.

    **Usage examples:**

        Create a new event with a known location and event type:

        >>> event = Event(
        ...     event_name="Cyber Attack on Grid",
        ...     event_date=date(2024, 5, 12),
        ...     location_id=some_location.id,
        ...     event_type_id=some_type.id,
        ...     description="Coordinated ransomware attack affecting power distribution."
        ... )
        >>> session.add(event)
        >>> session.commit()

        Link an actor to the event through the writable association:

        >>> from . import EventActor
        >>> assoc = EventActor(event=event, actor=some_actor, role="perpetrator")
        >>> session.add(assoc)
        >>> session.commit()

        Query events with eager loading of actors and country:

        >>> from sqlalchemy.orm import selectinload
        >>> events = (
        ...     session.query(Event)
        ...     .options(
        ...         selectinload(Event.actors),
        ...         selectinload(Event.countries),
        ...     )
        ...     .filter(Event.event_date >= date(2024, 1, 1))
        ...     .all()
        ... )

    .. seealso::
        :class:`Actor`
        :class:`Country`
        :class:`EventType`
        :class:`Location`
        :class:`ImpactAssessment`
        :class:`EventActor`
        :class:`CountryEvent`
        :class:`EventSource`
    """
    __repr_fields__ = ('id', 'event_name', 'event_date')
    
    @declared_attr
    def __mapper_args__(cls) -> Any:
        args: Any = super().__mapper_args__.copy()
        # args["eager_defaults"] = False
        return args
    
    __table_args__: tuple[SchemaItem | dict[str, Any], ...] = (
        CheckConstraint(
            "(event_end_date IS NULL) OR (event_end_date >= event_date)",
            name="ck_events_valid_event_end_date"
        ),
        CheckConstraint(
            "TRIM(event_name) != '' AND TRIM(description) != '' AND (notes IS NULL OR TRIM(notes) != '')", 
            name="ck_events_fields_non_empty"
        ),
        
        {'comment': 'Stores individual geopolitical incidents as the primary unit of analysis.'}
    )
    
    event_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment='Full event name.'
    )

    event_date: Mapped[date] = mapped_column(
        Date(), 
        nullable=False,
        comment='Occurrence DATE of the incident (without time). Must not be NULL.'
    )
    
    event_end_date: Mapped[date | None] = mapped_column(
        Date(), 
        nullable=True,
        comment='End DATE for extended-duration events (optional). Must be on or after event_date.'
    )

    location_id: Mapped[int | None] = mapped_column(
        Integer(),
        ForeignKey(_fk_ref(Base.metadata, 'location.id'), ondelete='RESTRICT'),
        nullable=True,
        comment='FOREIGN KEY to locations table. Nullable if event lacks precise spatial attribution.'
    )
    
    event_type_id: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey(_fk_ref(Base.metadata, 'event_type.id'), ondelete='RESTRICT'),
        nullable=False,
        comment='FOREIGN KEY to event_type table. Must not be NULL.'
    )

    description: Mapped[str] = mapped_column(
        Text(), 
        nullable=False,
        comment='Narrative summary of the incident. Must not be NULL.'
    )
    
    attribution_confidence: Mapped[AttributionConfidence] = mapped_column(
        db_enum(AttributionConfidence),
        nullable=False,
        default=AttributionConfidence.confirmed,
        server_default=text("'confirmed'::attribution_confidence"),
        comment='Confidence level in actor attribution and factual accuracy. Defaults to "confirmed".'    
    )
    
    countries: Mapped[list[Country]] = relationship(
        'Country', 
        secondary=_secondary_ref(Base.metadata, 'country_event'), 
        back_populates='events',
        lazy='select',
        uselist=True,
        viewonly=True
    )
    
    actors: Mapped[list[Actor]] = relationship(
        'Actor', 
        secondary=_secondary_ref(Base.metadata, 'event_actor'), 
        back_populates='events',
        lazy='select',
        uselist=True,
        viewonly=True
    ) 
    
    location: Mapped['Location'] = relationship(
        'Location', 
        back_populates='events',
        lazy='joined',
        uselist=False,
        viewonly=True
    ) 
     
    event_type: Mapped['EventType'] = relationship(
        'EventType', 
        back_populates='events',
        lazy='joined',
        uselist=False,
        viewonly=True
    )  
     
    sources: Mapped[list[Source]] = relationship(
        'Source', 
        secondary=_secondary_ref(Base.metadata, 'event_source'), 
        back_populates='events',
        lazy='select',
        uselist=True,
        viewonly=True
    )
    
    impact_assessment: Mapped[ImpactAssessment | None] = relationship(
        'ImpactAssessment', 
        back_populates='event', 
        lazy='select',
        uselist=False,
        viewonly=True
    )
    
    actor_associations: Mapped[list[EventActor]] = relationship(
        'EventActor',
        lazy='select',
        uselist=True,
        viewonly=False
    )
    
    country_associations: Mapped[list[CountryEvent]] = relationship(
        'CountryEvent',
        lazy='select',
        uselist=True,
        viewonly=False
    )
    
    source_associations: Mapped[list[EventSource]] = relationship(
        'EventSource',
        lazy='select',
        uselist=True,
        viewonly=False
    )