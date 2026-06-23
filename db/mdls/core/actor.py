from __future__ import annotations
from typing import Any, TYPE_CHECKING

from sqlalchemy import Integer, String, Text, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from sqlalchemy.schema import SchemaItem

from mdls.base.base import Base, db_enum, IdMixin, NotesMixin, TimestampMixin, TablenameMixin, UUIDMixin, ReprMixin
from utils.utils.name import _fk_ref, _secondary_ref
from utils.enums import ActorType

if TYPE_CHECKING:
    from core import Event, Country, EventActor

class Actor(
    Base,
    TablenameMixin, 
    IdMixin, 
    UUIDMixin,
    NotesMixin, 
    TimestampMixin,
    ReprMixin
    ):
    """
    Represents a specific organizational entity (e.g., government body, militant group,
    corporation, NGO) that can participate in events. An Actor is distinct from a
    `Country`, which models the abstract nation-state. This design supports
    hierarchical organizational structures via a self-referential parent relationship.

    Inherited mixins provide standard functionality:
        - ``TablenameMixin`` : auto-generates ``__tablename__`` from the class name.
        - ``IdMixin``        : integer primary key column ``id``.
        - ``UUIDMixin``      : universally unique identifier ``uuid``.
        - ``NotesMixin``     : ``notes`` (Text) column for unstructured analyst remarks.
        - ``TimestampMixin`` : ``created_at`` and ``updated_at`` datetime columns.
        - ``ReprMixin``      : ``__repr__`` that uses ``__repr_fields__``.

    .. note::

        The string representations are based on ``('id', 'actor_name', 'actor_type')``.

    **Table-level constraints and settings:**

    - ``UniqueConstraint('actor_name', 'country_id')`` :
        Prevents duplicate actor names within the same country. Two actors with the
        same name but different ``country_id`` (including NULL) are allowed, which
        is intentional for international/multinational organisations.
    - ``CheckConstraint(trim(actor_name) != '', …)`` :
        Ensures ``actor_name`` is never an empty/whitespace string, and that
        ``description`` and ``notes`` are either NULL or non-empty after trimming.
    - ``CheckConstraint(parent_actor_id IS NULL OR parent_actor_id != id)`` :
        Prevents a row from being its own parent. Application-level logic should be
        added to prevent deeper cycles if required.
    - Table comment : describes the role of the ``actor`` table in the domain model.

    **Columns:**

        actor_name : ``String(200)``, **not null**
            Full organisational name, potentially including hierarchical designations
            (e.g. "Ministry of Defence, Cyber Directorate").
        actor_type : ``ActorType`` enum, **not null**
            Categorical classification (e.g. ``GOVERNMENT``, ``REBEL_GROUP``,
            ``CORPORATE``). Stored using a database-level enum for data integrity.
        country_id : ``int`` or ``None``
            Foreign key to ``country.id``. **ON DELETE SET NULL** – if the referenced
            country is deleted, this column becomes NULL, preserving the actor record.
            Nullable to represent entities without a single national affiliation.
        parent_actor_id : ``int`` or ``None``
            Self-referential foreign key to ``actor.id``. **ON DELETE SET NULL** –
            deleting a parent does not cascade; children become top-level entities.
            Used to model organisational trees (e.g. a specific brigade under a
            military command). ``NULL`` for top-level actors.
        description : ``Text``, nullable
            Free-form contextual details for analyst disambiguation.
        notes : ``Text``, nullable (from ``NotesMixin``)
            Additional remarks.

    **Relationships:**

        events : ``list[Event]`` (many-to-many, **viewonly**)
            Events this actor participated in. Uses the ``event_actor`` secondary
            table. Loaded lazily (``lazy='select'``). Because the relationship is
            view‑only, modifications must go through the association object
            (``event_associations``).
        country : ``Country | None`` (many-to-one, **viewonly**)
            The associated ``Country`` instance, if any. Lazy-loaded.
        event_associations : ``list[EventActor]`` (one-to-many, **writable**)
            Association objects linking actors to events. These can hold additional
            data (e.g. role, certainty). This relationship is the intended path for
            creating/removing event–actor links.

    **Loading strategies and performance considerations:**

        All relationships use ``lazy='select'`` (load on first access). This is safe
        for single-object operations but **will cause the N+1 query problem** when
        iterating over collections of actors. For any query that returns multiple
        actors, always apply eager loading:

        .. code-block:: python

            from sqlalchemy.orm import selectinload

            actors = (
                session.query(Actor)
                .options(
                    selectinload(Actor.country),
                    selectinload(Actor.events),
                )
                .all()
            )

        For bulk inserts/updates where defaults are not required, uncomment the
        ``eager_defaults = False`` mapper argument to avoid per-row roundtrips for
        server-generated defaults.

    **Usage examples:**

        Create a new top-level actor and attach it to a country:

        >>> actor = Actor(
        ...     actor_name="National Cyber Security Centre",
        ...     actor_type=ActorType.GOVERNMENT,
        ...     country_id=some_country.id
        ... )
        >>> session.add(actor)
        >>> session.commit()

        Link an actor to an event through the writable association:

        >>> assoc = EventActor(actor=actor, event=event, role="perpetrator")
        >>> session.add(assoc)
        >>> session.commit()

    .. seealso::
        :class:`Country`
        :class:`Event`
        :class:`EventActor`
    """
    __repr_fields__ = ('id', 'actor_name', 'actor_type')
    
    @declared_attr
    def __mapper_args__(cls) -> Any:
        args: Any = super().__mapper_args__.copy()
        # args["eager_defaults"] = False
        return args
    
    __table_args__: tuple[SchemaItem | dict[str, Any], ...] = (
        UniqueConstraint(
            'actor_name', 'country_id',
            name="uq_actors_actor_name_country_id"
        ),
        
        CheckConstraint(
            "TRIM(actor_name) != '' AND (description IS NULL OR TRIM(description) != '') AND (notes IS NULL OR TRIM(notes) != '')", 
            name="ck_actors_fields_non_empty"
        ),
        CheckConstraint(
            "parent_actor_id IS NULL OR parent_actor_id != id", 
            name="ck_actors_no_self_reference"
        ),
        
        {
            'comment': 'Models specific organizational entities participating in incidents, distinguished from Countries which represent abstract nation-state units.'
        }
    )
    
    actor_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment='Full organizational name potentially including hierarchical designations.'
    )
    
    actor_type: Mapped[ActorType] = mapped_column(
        db_enum(ActorType),
        nullable=False,
        comment='Categorical classification of actor type.'
    )
    
    country_id: Mapped[int | None] = mapped_column(
        Integer(),
        ForeignKey(_fk_ref(Base.metadata, 'country.id'), ondelete='SET NULL'),
        nullable=True,
        comment='FOREIGN KEY to Countries table. Nullable if entities lack single national affiliation.'
    )
    
    parent_actor_id: Mapped[int | None] = mapped_column(
        Integer(),
        ForeignKey(_fk_ref(Base.metadata, 'actor.id'), ondelete='SET NULL'),
        nullable=True,
        comment='Self-referential FOREIGN KEY for modeling organizational hierarchies. NULL for top-level entities.'
    )
    
    description: Mapped[str | None] = mapped_column(
        Text(),
        nullable=True,
        comment='Contextual details for analyst understanding and disambiguation.'
    )
    
    events: Mapped[list['Event']] = relationship(
        'Event', 
        secondary=_secondary_ref(Base.metadata, 'event_actor'), 
        back_populates='actors',
        lazy='select',
        uselist=True,
        viewonly=True
    )
    
    country: Mapped[Country | None] = relationship(
        'Country', 
        back_populates='actors',
        lazy='select',
        uselist=False,
        viewonly=True
    )
    
    event_associations: Mapped[list[EventActor]] = relationship(
        'EventActor',
        lazy='select',
        uselist=True,
        viewonly=False
    )
