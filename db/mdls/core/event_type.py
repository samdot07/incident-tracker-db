from __future__ import annotations
from typing import Any, TYPE_CHECKING

from sqlalchemy import Integer, String, Text, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import SchemaItem
    
from mdls.base.base import Base, db_enum, IdMixin, NotesMixin, TimestampMixin, TablenameMixin, UUIDMixin, ReprMixin
from utils.enums import EventTypeEnum
from utils.utils.name import _fk_ref

if TYPE_CHECKING:
    from core import Event

class EventType(    
    Base, 
    TablenameMixin,
    IdMixin, 
    UUIDMixin,
    NotesMixin, 
    TimestampMixin,
    ReprMixin
    ):
    """
    Represents a two‑tier hierarchical taxonomy for classifying events.

    This model distinguishes primary categories (e.g., ``CYBER_ATTACK``, ``MALWARE``)
    from optional subcategories (e.g., ``RANSOMWARE`` under ``MALWARE``). The
    hierarchy is implemented via a self‑referential foreign key (``parent_type_id``).
    The fixed top‑level classification is stored in the ``event_type`` enum column,
    while ``type_name`` provides a human‑readable display string.

    Inherited mixins provide standard functionality:
        - ``TablenameMixin`` : auto‑generates ``__tablename__`` from the class name.
        - ``IdMixin``        : integer primary key column ``id``.
        - ``UUIDMixin``      : universally unique identifier ``uuid``.
        - ``NotesMixin``     : ``notes`` (Text) column for unstructured remarks.
        - ``TimestampMixin`` : ``created_at`` and ``updated_at`` datetime columns.
        - ``ReprMixin``      : ``__repr__`` that uses ``__repr_fields__``.

    .. note::

        The string representation is based on ``('id', 'type_name', 'event_type')``.

    **Table‑level constraints and settings:**

    - ``UniqueConstraint('type_name', 'parent_type_id')`` :
        Prevents duplicate category names under the same parent. Two categories
        with the same name but different parents (or one with NULL parent) are
        allowed, which models the hierarchy correctly.
    - ``CheckConstraint(TRIM(type_name) != '' AND TRIM(definition) != '' AND ...)`` :
        Ensures that required text fields (``type_name``, ``definition``) are not
        empty or whitespace. Optional fields (``examples``, ``notes``) are allowed
        to be NULL, but if provided they also cannot be empty/whitespace.
    - Table comment : describes the hierarchical taxonomy purpose.

    **Columns:**

        type_name : ``String(100)``, **not null**
            Human‑readable name of the category or subcategory
            (e.g., "Ransomware", "Phishing").
        parent_type_id : ``int | None``
            Self‑referential foreign key to ``event_type.id``. **ON DELETE RESTRICT** –
            prevents deletion of a category that has child subcategories.
            ``NULL`` for top‑level categories.
        event_type : ``EventTypeEnum``, **not null**
            Fixed top‑level classification from a predefined enumeration
            (e.g., ``CYBER_ATTACK``, ``MALWARE``, ``FRAUD``). Stored as a
            database enum for integrity.
        definition : ``Text``, **not null**
            Detailed operational definition that specifies scope, inclusion/exclusion
            criteria, boundary conditions, and disambiguation from related categories.
        examples : ``Text``, nullable
            Representative incident examples that exemplify the category, helping
            analysts classify ambiguous cases.
        notes : ``Text``, nullable (from ``NotesMixin``)
            Free‑text notes about the category (e.g., changes in definition over time).

    **Relationships:**

        events : ``list[Event]`` (one‑to‑many, **viewonly**)
            All events classified under this category/subcategory.
            Loaded lazily (``lazy='select'``). Because the relationship is view‑only,
            modifications must go through the ``Event.event_type`` foreign key.
        parent : ``EventType | None`` (self‑referential many‑to‑one, **viewonly**)
            The immediate parent category, if any. Loaded with **joined** eager loading
            (``lazy='joined'``) to avoid an extra query when accessing a category's
            parent – a common access pattern in hierarchical taxonomies.
        children : ``list[EventType]`` (self‑referential one‑to‑many, **viewonly**)
            All direct subcategories of this category. Loaded with **selectin** eager
            loading (``lazy='selectin'``) to efficiently fetch children without N+1
            queries when iterating over a list of categories.

    **Loading strategies and performance considerations:**

        - The ``parent`` relationship uses ``lazy='joined'`` because parent lookup is
          frequent and avoiding a second query is beneficial. This adds a LEFT JOIN
          when querying categories directly, which is acceptable given the typically
          small size of the taxonomy table (< a few thousand rows).
        - The ``children`` relationship uses ``lazy='selectin'`` to batch‑load all
          children for a collection of parent categories with a single secondary query.
          This avoids the N+1 problem when you load multiple categories and then access
          their ``.children``.
        - The ``events`` relationship remains ``lazy='select'``. If you frequently load
          categories together with their events (e.g., reporting queries), use
          explicit eager loading:

          .. code-block:: python

              from sqlalchemy.orm import selectinload

              categories = (
                  session.query(EventType)
                  .options(selectinload(EventType.events))
                  .all()
              )

        - Because this table is mostly read‑only and small, indexing is minimal.
          The foreign key column ``parent_type_id`` should be indexed manually if you
          frequently traverse upwards from children or perform recursive queries.
          (SQLAlchemy does not auto‑create indexes on FKs.)

    **Usage examples:**

        Create a top‑level category:

        >>> malware = EventType(
        ...     type_name="Malware",
        ...     event_type=EventTypeEnum.MALWARE,
        ...     definition="Any malicious software designed to disrupt, damage, or gain unauthorized access."
        ... )
        >>> session.add(malware)
        >>> session.commit()

        Create a subcategory under it:

        >>> ransomware = EventType(
        ...     type_name="Ransomware",
        ...     parent_type_id=malware.id,
        ...     event_type=EventTypeEnum.MALWARE,
        ...     definition="Malware that encrypts victim data and demands payment for decryption."
        ... )
        >>> session.add(ransomware)
        >>> session.commit()

        Query a category and access its parent/children:

        >>> subcat = session.get(EventType, ransomware.id)
        >>> print(subcat.parent.type_name)  # joined loading → no extra query
        'Malware'
        >>> for child in subcat.parent.children:
        ...     print(child.type_name)      # selectin loading → one extra query for all children

    .. seealso::
        :class:`Event`
        :class:`EventTypeEnum`
    """
    __repr_fields__ = ('id', 'type_name', 'event_type')
    
    __table_args__: tuple[SchemaItem | dict[str, Any], ...] = (
        UniqueConstraint(
            'type_name', 'parent_type_id',
            name="uq_event_types_type_name_parent_type_id"
        ),
        
        CheckConstraint(
            "TRIM(type_name) != '' AND TRIM(definition) != '' AND (examples IS NULL OR TRIM(examples) != '') AND (notes IS NULL OR TRIM(notes) != '')", 
            name="ck_event_types_fields_non_empty"
        ),
        
        {'comment': 'Implements two-tier hierarchical taxonomy distinguishing primary categories from subcategories.'}    
    )
    
    type_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment='Category or subcategory name.'
    )
    
    parent_type_id: Mapped[int | None] = mapped_column(
        Integer(),
        ForeignKey(_fk_ref(Base.metadata, 'event_type.id'), ondelete='RESTRICT'),
        nullable=True,
        comment='Self-referential FOREIGN KEY implementing hierarchical taxonomy. NULL for primary categories, populated for subcategories.'
    )
    
    event_type: Mapped[EventTypeEnum] = mapped_column(
        db_enum(EventTypeEnum),
        nullable=False,
        comment='Primary category from the fixed taxonomy.'
    )
    
    definition: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
        comment='Operational definition specifying scope, inclusion criteria, boundary conditions, and disambiguation from related categories.'
    )
    
    examples: Mapped[str | None] = mapped_column(
        Text(),
        nullable=True,
        comment='Representative incidents exemplifying the category, supporting decisions for ambiguous cases.'
    )
    
    events: Mapped[list[Event]] = relationship(
        'Event', 
        back_populates='event_type',
        lazy='select',
        uselist=True,
        viewonly=True
    )
    
    parent: Mapped[EventType | None] = relationship(
        'EventType', 
        remote_side=["EventType.id"],  # type: ignore
        back_populates='children',
        lazy='joined',
        uselist=False,
        viewonly=True
    ) 
    
    children: Mapped[list[EventType]] = relationship(
        'EventType', 
        back_populates='parent',
        lazy='selectin',
        uselist=True,
        viewonly=True
    ) 