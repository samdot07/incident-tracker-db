from __future__ import annotations
from datetime import date
from typing import Any, TYPE_CHECKING

from sqlalchemy import String, Date, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr
from sqlalchemy.schema import SchemaItem

from mdls.base.base import Base, db_enum, IdMixin, NotesMixin, TimestampMixin, TablenameMixin, UUIDMixin, ReprMixin
from utils.utils.name import _secondary_ref
from utils.enums import SourceType

if TYPE_CHECKING:
    from core import Event, EventSource

class Source(    
    Base, 
    TablenameMixin,
    IdMixin, 
    UUIDMixin,
    NotesMixin, 
    TimestampMixin,
    ReprMixin
    ):
    """
    Represents a documentary source (e.g., news article, report, dataset, interview)
    that provides evidence for one or more events. Sources enable validation via
    triangulation and protect intellectual property through clear attribution.

    Inherited mixins provide standard functionality:
        - ``TablenameMixin`` : auto-generates ``__tablename__`` from the class name.
        - ``IdMixin``        : integer primary key column ``id``.
        - ``UUIDMixin``      : universally unique identifier ``uuid``.
        - ``NotesMixin``     : ``notes`` (Text) column for unstructured analyst remarks.
        - ``TimestampMixin`` : ``created_at`` and ``updated_at`` datetime columns.
        - ``ReprMixin``      : ``__repr__`` that uses ``__repr_fields__``.

    .. note::

        The string representation is based on ``('id', 'source_title', 'source_type')``.

    **Table‑level constraints and settings:**

    - ``CheckConstraint("publication_date <= CURRENT_DATE")`` :
        Prevents future publication dates, ensuring data consistency.
    - ``CheckConstraint("TRIM(source_title) != '' AND …")`` :
        Guarantees that ``source_title`` and ``publisher`` are never empty/whitespace.
        Allows ``author`` and ``notes`` to be NULL or non‑empty after trimming.
    - ``CheckConstraint("url IS NULL OR url ~ '^https?://[^/[:space:]]+'")`` :
        If a URL is provided, it must start with ``http://`` or ``https://`` and have
        at least one character after the domain separator. Simple but effective
        front‑line validation.
    - Table comment : describes the role of the ``source`` table in the domain model.

    **Columns:**

        source_title : ``String(500)``, **not null**
            Full title of the publication or document.
        author : ``String(200)``, nullable
            Individual author or organisational publisher. May be NULL if unknown.
        publication_date : ``Date``, nullable
            When the source was published. Cannot be a future date.
        url : ``String(2048)``, nullable
            Web location for online sources. NULL for offline materials (books,
            physical reports, etc.).
        source_type : ``SourceType`` enum, **not null**
            Classification of the source (e.g. ``NEWS_ARTICLE``, ``GOVERNMENT_REPORT``,
            ``ACADEMIC_PAPER``). Stored as a database‑level enum for integrity.
        publisher : ``String(200)``, **not null**, default ``'Unknown'``
            Entity that published the source. Uses a server default to avoid
            application‑side fallbacks.
        notes : ``Text``, nullable (from ``NotesMixin``)
            Additional remarks (e.g. translation notes, access date for URLs).

    **Relationships:**

        events : ``list[Event]`` (many‑to‑many, **viewonly**)
            Events that reference this source. Uses the ``event_source`` secondary
            table. Loaded lazily (``lazy='select'``). Because the relationship is
            view‑only, modifications must go through the association object
            (``event_associations``).
        event_associations : ``list[EventSource]`` (one‑to‑many, **writable**)
            Association objects linking sources to events. These can store additional
            metadata (e.g. confidence score, specific pages cited). This is the
            intended path for creating/removing event–source links.

    **Loading strategies and performance considerations:**

        All relationships use ``lazy='select'`` (load on first access). This is safe
        for single‑object operations but **will cause the N+1 query problem** when
        iterating over collections of sources. For any query that returns multiple
        sources, always apply eager loading:

        .. code-block:: python

            from sqlalchemy.orm import selectinload

            sources = (
                session.query(Source)
                .options(selectinload(Source.events))
                .all()
            )

        For bulk inserts/updates where defaults are not required, uncomment the
        ``eager_defaults = False`` mapper argument to avoid per‑row roundtrips for
        server‑generated defaults (such as the ``publisher`` default). 

    **Usage examples:**

        Create a new source and associate it with an existing event:

        >>> src = Source(
        ...     source_title="Cyber Attack Attribution Framework 2024",
        ...     author="J. Smith",
        ...     publication_date=date(2024, 3, 15),
        ...     url="https://example.com/report.pdf",
        ...     source_type=SourceType.ACADEMIC_PAPER,
        ...     publisher="Journal of Cybersecurity"
        ... )
        >>> session.add(src)
        >>> session.commit()

        Link a source to an event through the writable association object:

        >>> from myapp.models import EventSource
        >>> assoc = EventSource(source=src, event=some_event, confidence=0.95)
        >>> session.add(assoc)
        >>> session.commit()

    .. seealso::
        :class:`Event`
        :class:`EventSource`
    """
    __repr_fields__ = ('id', 'source_title', 'source_type')
    
    @declared_attr
    def __mapper_args__(cls) -> Any:
        args: Any = super().__mapper_args__.copy()
        # args["eager_defaults"] = False
        return args
    
    __table_args__: tuple[SchemaItem | dict[str, Any], ...] = (
        CheckConstraint(
            "publication_date <= CURRENT_DATE",
            name="ck_sources_valid_publication_date"
        ),
        CheckConstraint(
            "TRIM(source_title) != '' AND (author IS NULL OR TRIM(author) != '') AND TRIM(publisher) != '' AND (notes IS NULL OR TRIM(notes) != '')", 
            name="ck_sources_fields_non_empty"
        ),
        CheckConstraint(
            "url IS NULL OR url ~ '^https?://[^/[:space:]]+'",
            name="ck_sources_valid_url"
        ),
        
        {
            'comment': 'Documents sources used for incident coding to enable validation via triangulation and protect intellectual property through attribution.'
        }
    )
    
    source_title: Mapped[str] = mapped_column( 
        String(500), 
        nullable=False,
        comment='Publication or document title.'
    )
    
    author: Mapped[str | None] = mapped_column( 
        String(200), 
        nullable=True,
        comment='Individual author or organizational publisher.'
    )
    
    publication_date: Mapped[date | None] = mapped_column(
        Date(), 
        nullable=True,
        comment='When the source was published. Nullable for undated materials.'
    )
    
    url: Mapped[str | None] = mapped_column(
        String(2048), 
        nullable=True,
        comment='Web location for online sources. Nullable for offline materials.'
    )
    
    source_type: Mapped[SourceType] = mapped_column(
        db_enum(SourceType),
        nullable=False,
        comment='Source classification for assessing reliability and formatting citations.'
    )
    
    publisher: Mapped[str] = mapped_column(
        String(200),
        default='Unknown',
        server_default='Unknown',
        nullable=False,
        comment='Who the source was published by. Defaults to Unknown.'
    )
    
    events: Mapped[list[Event]] = relationship(
        'Event', 
        secondary=_secondary_ref(Base.metadata, 'event_source'), 
        back_populates='sources',
        lazy='select',
        uselist=True,
        viewonly=True
    ) 

    event_associations: Mapped[list[EventSource]] = relationship(
        'EventSource',
        lazy='select',
        uselist=True,
        viewonly=False
    )
    