from __future__ import annotations
from typing import Any, TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, PrimaryKeyConstraint, CheckConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import SchemaItem

from mdls.base.base import Base, db_enum, varchar_enum, NotesMixin, TablenameMixin, ReprMixin
from utils.utils.name import _fk_ref
from utils.enums import ActorRole, AttributionConfidence

if TYPE_CHECKING:
    from core import Actor, Event

class EventActor(    
    Base,  
    TablenameMixin,
    NotesMixin,
    ReprMixin
    ):
    """
    Junction table linking events to participating organizational actors.

    This association object extends a simple many-to-many link by adding
    ``actor_role`` (how the actor participated) and ``attribution_confidence``
    (the confidence level of that attribution). Inherited mixins provide:
        - ``TablenameMixin`` : auto-generates ``__tablename__`` from class name.
        - ``NotesMixin``     : ``notes`` (Text) column for unstructured remarks.
        - ``ReprMixin``      : ``__repr__`` using ``__repr_fields__``.

    .. note::

        The string representation is based on
        ``('event_id', 'actor_id', 'actor_role', 'attribution_confidence')``.

    **Table-level constraints and settings:**

    - ``PrimaryKeyConstraint('event_id', 'actor_id')`` :
        Composite primary key ensures each (event, actor) pair is unique.
    - ``CheckConstraint(TRIM(notes) != '' OR notes IS NULL)`` :
        If ``notes`` are provided, they must not be empty/whitespace-only strings.
    - Table comment : describes the table as the junction linking events to
      participating organizational actors.

    **Columns:**

        event_id : ``int``, **not null**, part of PK
            Foreign key to ``event.id``. **ON DELETE CASCADE** – if the referenced
            event is deleted, this association is automatically removed.
        actor_id : ``int``, **not null**, part of PK
            Foreign key to ``actor.id``. **ON DELETE CASCADE** – if the referenced
            actor is deleted, this association is automatically removed.
        actor_role : ``ActorRole`` enum, **not null**
            Categorical classification of the actor's role in the incident
            (e.g., ``INITIATOR``, ``RESPONDER``, ``TARGET``, ``PARTICIPANT``,
            ``CLAIMANT``, ``OBSERVER``). Stored via ``varchar_enum()``.
        attribution_confidence : ``AttributionConfidence`` enum, **not null**
            Confidence level for the attribution (``CONFIRMED``, ``SUSPECTED``,
            ``THIRD_PARTY``, ``CONTESTED``). Defaults to ``CONFIRMED`` using a
            server-level default – the database will set this value if omitted.
        notes : ``Text``, nullable (from ``NotesMixin``)
            Additional remarks about the actor's specific role or the evidence
            supporting the attribution.

    **Relationships:**

        event : ``Event`` (many-to-one, **writable**)
            The associated ``Event`` instance. Back-populates
            ``Event.actor_associations``. Loaded lazily (``lazy='select'``).
            Writable – assign an ``Event`` directly to this association object.
        actor : ``Actor`` (many-to-one, **writable**)
            The associated ``Actor`` instance. Back-populates
            ``Actor.event_associations``. Also lazy and writable.

    **Loading strategies and performance considerations:**

        All relationships use ``lazy='select'`` (load on first access). This is safe
        for single-object work but **causes the N+1 query problem** when iterating
        over collections of associations. For any query that returns multiple
        ``EventActor`` rows, always apply eager loading if you know you will access
        the related ``event`` or ``actor``:

        .. code-block:: python

            from sqlalchemy.orm import selectinload

            associations = (
                session.query(EventActor)
                .options(selectinload(EventActor.event), selectinload(EventActor.actor))
                .filter(EventActor.actor_role == ActorRole.INITIATOR)
                .all()
            )

        This table is a pure association (junction). In most access patterns, you
        will query it indirectly via ``Event.actor_associations`` or
        ``Actor.event_associations``. Ensure those parent relationships also use
        appropriate eager loading when traversing large collections.

    **Usage examples:**

        Create a new association linking an existing event and actor:

        >>> from yourapp.models import Event, Actor, EventActor, ActorRole, AttributionConfidence
        >>> event = session.get(Event, 101)
        >>> actor = session.get(Actor, 42)
        >>> association = EventActor(
        ...     event=event,
        ...     actor=actor,
        ...     actor_role=ActorRole.INITIATOR,
        ...     attribution_confidence=AttributionConfidence.SUSPECTED,
        ...     notes="Based on internal intelligence reports, but no public confirmation."
        ... )
        >>> session.add(association)
        >>> session.commit()

        Query all confirmed initiators for a given event:

        >>> initiators = (
        ...     session.query(EventActor)
        ...     .filter(
        ...         EventActor.event_id == 101,
        ...         EventActor.actor_role == ActorRole.INITIATOR,
        ...         EventActor.attribution_confidence == AttributionConfidence.CONFIRMED
        ...     )
        ...     .all()
        ... )
        >>> for assoc in initiators:
        ...     print(assoc.actor.name, assoc.attribution_confidence)  # N+1 – use eager loading

    **Important design notes:**

        - This table uses a **composite primary key** instead of a surrogate ``id``
          column. This is appropriate for a pure many-to-many association with
          additional attributes, as it enforces uniqueness naturally and avoids an
          unnecessary auto-increment column.
        - ``ON DELETE CASCADE`` on both foreign keys ensures that deleting an
          ``Event`` or ``Actor`` automatically cleans up its junction rows,
          maintaining referential integrity without application‑level logic.
        - The ``notes`` column is validated at the database level (via
          ``CheckConstraint``) to prevent empty whitespace strings, but allows
          ``NULL`` as “no comment”.
        - The ``attribution_confidence`` default is implemented as a server default
          (``server_default``) rather than a Python‑side default. This ensures the
          default is applied even for bulk inserts or when the column is omitted in
          INSERT statements from other clients.

    .. seealso::
        :class:`Event`
        :class:`Actor`
        :class:`ActorRole`
        :class:`AttributionConfidence`
    """
    __repr_fields__ = ('event_id', 'actor_id', 'actor_role', 'attribution_confidence')
    
    __table_args__: tuple[SchemaItem | dict[str, Any], ...] = (
        PrimaryKeyConstraint(
            'event_id', 'actor_id',
            name="pk_event_actors"
        ),
        
        CheckConstraint(
            "(notes IS NULL OR TRIM(notes) != '')",
            name="ck_event_actor_fields_non_empty"
        ),
        
        {'comment': 'Junction table linking events to participating organizational actors'}
    )

    event_id: Mapped[int] = mapped_column(
        Integer(), 
        ForeignKey(_fk_ref(Base.metadata, 'event.id'), ondelete='CASCADE'), 
        nullable=False,
        comment='FOREIGN KEY referencing events table.'
    )
    
    actor_id: Mapped[int] = mapped_column(
        Integer(), 
        ForeignKey(_fk_ref(Base.metadata, 'actor.id'), ondelete='CASCADE'), 
        nullable=False,
        comment='FOREIGN KEY referencing actors table.'
    )
    
    actor_role: Mapped[ActorRole] = mapped_column(
        varchar_enum(ActorRole), 
        nullable=False,
        comment='Role played in incident (Initiator, Responder, Target, Participant, Claimant, Observer). Useful for action-reaction analysis.'
    )
    
    attribution_confidence: Mapped[AttributionConfidence] = mapped_column(
        db_enum(AttributionConfidence),
        nullable=False,
        default=AttributionConfidence.confirmed,
        server_default=text("'confirmed'::attribution_confidence"),
        comment='Confidence level for actor attribution (Confirmed, Suspected, Third-Party, Contested). Defaults to Confirmed.'
    )
    
    event: Mapped['Event'] = relationship(
        back_populates='actor_associations',
        lazy='select',
        uselist=False,
        viewonly=False
    )
    
    actor: Mapped['Actor'] = relationship(
        back_populates='event_associations',
        lazy='select',
        uselist=False,
        viewonly=False
    )