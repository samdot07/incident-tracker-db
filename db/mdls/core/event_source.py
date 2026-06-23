from __future__ import annotations
from typing import Any, TYPE_CHECKING

from sqlalchemy import Integer,String, ForeignKey, PrimaryKeyConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import SchemaItem

from mdls.base.base import Base, NotesMixin, TablenameMixin, ReprMixin
from utils.utils.name import _fk_ref

if TYPE_CHECKING:
    from core import Event, Source

class EventSource(    
    Base, 
    TablenameMixin,
    NotesMixin,
    ReprMixin
    ):
    """
    Represents the many-to-many relationship between an ``Event`` and a ``Source``,
    including optional page or section references within the source document.

    This association object sits between events and their supporting documentary
    evidence (e.g., reports, news articles, archival records). It allows attaching
    citation details (``page_reference``) and analyst notes to each specific pairing.

    Inherited mixins provide standard functionality:
        - ``TablenameMixin`` : auto-generates ``__tablename__`` from the class name.
        - ``NotesMixin``     : ``notes`` (Text) column for unstructured analyst remarks.
        - ``ReprMixin``      : ``__repr__`` that uses ``__repr_fields__``.

    .. note::

        The string representation is based on ``('event_id', 'source_id')``.

    **Table-level constraints and settings:**

    - ``PrimaryKeyConstraint('event_id', 'source_id')`` :
        Composite primary key ensures each (event, source) pair is unique.
    - ``CheckConstraint("(notes IS NULL) OR (TRIM(notes) != '')")`` :
        If ``notes`` are provided, they cannot be empty or whitespace-only strings.
    - Table comment : describes the table as the junction linking events to
      documentary sources with citation details.

    **Columns:**

        event_id : ``int``, **not null**, part of PK
            Foreign key to ``event.id``. **ON DELETE CASCADE** – if the referenced
            event is deleted, this association is automatically removed.
        source_id : ``int``, **not null**, part of PK
            Foreign key to ``source.id``. **ON DELETE CASCADE** – if the referenced
            source is deleted, this association is automatically removed.
        page_reference : ``str | None``, nullable
            Optional page numbers, section identifiers, paragraphs, or any
            locator within the source document (max length 50 characters).
            Allows ``NULL`` to indicate the source supports the event as a whole
            without a specific page.
        notes : ``Text``, nullable (from ``NotesMixin``)
            Additional contextual remarks about the credibility, interpretation,
            or significance of this source for the given event.

    **Relationships:**

        source : ``Source`` (many-to-one, **writable**)
            The associated ``Source`` instance. This relationship back-populates
            ``Source.event_associations``. Loaded lazily (``lazy='select'``).
            It is writable – you can assign a ``Source`` directly to this
            association object.
        event : ``Event`` (many-to-one, **writable**)
            The associated ``Event`` instance. Back-populates
            ``Event.source_associations``. Also writable and lazily loaded.

    **Loading strategies and performance considerations:**

        Both relationships use ``lazy='select'`` (load on first access). This is
        safe for single-object work but **will cause the N+1 query problem** when
        iterating over collections of associations. For any query that returns
        multiple ``EventSource`` rows, always apply eager loading if you know you
        will access the related ``event`` or ``source``:

        .. code-block:: python

            from sqlalchemy.orm import selectinload

            associations = (
                session.query(EventSource)
                .options(selectinload(EventSource.event), selectinload(EventSource.source))
                .filter(EventSource.page_reference.is_not(None))
                .all()
            )

        This table is an association (junction). In most access patterns, you will
        query it indirectly via ``Event.source_associations`` or
        ``Source.event_associations``. Ensure those parent relationships also use
        appropriate eager loading when traversing large collections.

    **Usage examples:**

        Link an existing event to a source with a specific page reference:

        >>> from yourapp.models import Event, Source, EventSource
        >>> event = session.get(Event, 101)
        >>> source = session.get(Source, 42)
        >>> association = EventSource(
        ...     event=event,
        ...     source=source,
        ...     page_reference="pp. 15-18",
        ...     notes="Corroborates the timeline of the cyberattack"
        ... )
        >>> session.add(association)
        >>> session.commit()

        Retrieve all sources for a given event, ordered by source title:

        >>> event_id = 101
        >>> associations = (
        ...     session.query(EventSource)
        ...     .filter(EventSource.event_id == event_id)
        ...     .options(selectinload(EventSource.source))
        ...     .all()
        ... )
        >>> for assoc in associations:
        ...     print(assoc.source.title, assoc.page_reference)

        Paginate through associations with notes (avoid N+1):

        >>> page_num = 0
        >>> per_page = 50
        >>> associations = (
        ...     session.query(EventSource)
        ...     .filter(EventSource.notes.is_not(None))
        ...     .options(selectinload(EventSource.event), selectinload(EventSource.source))
        ...     .offset(page_num * per_page)
        ...     .limit(per_page)
        ...     .all()
        ... )

    **Important design notes:**

        - This table uses a **composite primary key** instead of a surrogate ``id``
          column. This is appropriate for a many-to-many association with optional
          additional attributes, as it enforces uniqueness and avoids an unnecessary
          auto-increment column.
        - ``ON DELETE CASCADE`` on both foreign keys ensures that deleting an
          ``Event`` or a ``Source`` automatically cleans up its junction rows,
          maintaining referential integrity without application-level logic.
        - The ``page_reference`` column is limited to 50 characters – enough for
          typical citations like "p. 12", "§3.2", "Figure 4", or "pp. 45-67".
          For longer citation text, use the ``notes`` column or extend the length.
        - The ``notes`` column is validated at the database level via
          ``CheckConstraint`` to prevent empty/whitespace-only strings, but allows
          ``NULL`` as “no comment”.

    .. seealso::
        :class:`Event`
        :class:`Source`
    """
    __repr_fields__ = ('event_id', 'source_id')
    
    __table_args__: tuple[SchemaItem | dict[str, Any], ...] = (
        PrimaryKeyConstraint(
            'event_id', 'source_id',
            name="pk_event_sources"
        ),
        
        CheckConstraint(
            "(notes IS NULL) OR (TRIM(notes) != '')",
            name="ck_event_source_fields_non_empty"
        ),
        
        {'comment': 'Junction table linking events to documentary sources with citation details.'}
    )

    event_id: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey(_fk_ref(Base.metadata, 'event.id'), ondelete='CASCADE'),
        nullable=False,
        comment='FOREIGN KEY referencing events table.'
    )
    
    source_id: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey(_fk_ref(Base.metadata, 'source.id'), ondelete='CASCADE'),
        nullable=False,
        comment='FOREIGN KEY referencing sources table.'
    )

    page_reference: Mapped[str | None] = mapped_column(
        String(50), 
        nullable=True, 
        comment='Specific page numbers or section identifiers within source documents.'
    )
    
    source: Mapped['Source'] = relationship(
        back_populates='event_associations',
        lazy='select',
        uselist=False,
        viewonly=False
    )
        
    event: Mapped['Event'] = relationship(
        back_populates='source_associations',
        lazy='select',
        uselist=False,
        viewonly=False
    )