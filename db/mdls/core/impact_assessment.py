from __future__ import annotations
from decimal import Decimal
from typing import Any, TYPE_CHECKING

from sqlalchemy import Integer, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from sqlalchemy.schema import SchemaItem
    
from mdls.base.base import Base, db_enum, IdMixin, NotesMixin, TimestampMixin, TablenameMixin, UUIDMixin, ReprMixin
from utils.utils.name import _fk_ref
from utils.enums import StrategicSignificance, PoliticalImpact, LegalPrecedent

if TYPE_CHECKING:
    from core import Event

class ImpactAssessment(    
    Base, 
    TablenameMixin,
    IdMixin, 
    UUIDMixin,
    NotesMixin, 
    TimestampMixin,
    ReprMixin
    ):
    """
    Models the multidimensional consequences and strategic significance of an event.
    Each event can have at most one impact assessment (one-to‑one relationship),
    enforced by a unique foreign key constraint on ``event_id``.

    Inherited mixins provide standard functionality:
        - ``TablenameMixin`` : auto-generates ``__tablename__`` from the class name.
        - ``IdMixin``        : integer primary key column ``id``.
        - ``UUIDMixin``      : universally unique identifier ``uuid``.
        - ``NotesMixin``     : ``notes`` (Text) column for unstructured analyst remarks.
        - ``TimestampMixin`` : ``created_at`` and ``updated_at`` datetime columns.
        - ``ReprMixin``      : ``__repr__`` that uses ``__repr_fields__``.

    .. note::

        The string representation is based on ``('id', 'event_id', 'strategic_significance')``.

    **Table-level constraints and settings:**

    - ``UniqueConstraint`` on ``event_id`` (implicit from ``unique=True``) :
        Guarantees a one‑to‑one relationship between ``Event`` and ``ImpactAssessment``.
    - ``CheckConstraint`` on casualty fields:
        ``(casualties_killed IS NULL OR casualties_killed >= 0) AND ...``
        Ensures all numeric impact metrics are either NULL or non‑negative.
    - ``CheckConstraint`` on notes:
        ``(notes IS NULL OR trim(notes) != '')``
        Prevents empty/whitespace strings in the notes field.
    - Table comment : describes the table's purpose in the domain model.

    **Columns:**

        event_id : ``int``, **not null**, unique, foreign key to ``event.id`` (ON DELETE CASCADE)
            Links the assessment to a single event. Cascade delete means removing an event
            automatically removes its impact assessment.
        strategic_significance : ``StrategicSignificance`` enum or ``None``
            Categorical strategic importance (Low, Medium, High, Critical).
            Nullable when significance is indeterminate.
        casualties_killed : ``int`` or ``None``
            Number of fatalities directly attributed to the event.
        casualties_wounded : ``int`` or ``None``
            Number of injured persons.
        displaced_persons : ``int`` or ``None``
            Number of people displaced (internally or externally).
        economic_impact_usd : ``Decimal`` or ``None``
            Estimated economic cost in US dollars, stored with 2 decimal places (Numeric(15,2)).
        political_impact : ``PoliticalImpact`` enum or ``None``
            Diplomatic consequences: Improved, Stable, Deteriorated, Ruptured.
        legal_precedent : ``LegalPrecedent`` enum or ``None``
            Implications for international legal norms: Affirming, Neutral, Testing, Violating.
        notes : ``Text``, nullable (from ``NotesMixin``)
            Additional context, methodology notes, or uncertainty explanations.

    **Relationships:**

        event : ``Event`` (one‑to‑one, **viewonly**)
            The associated event. Lazy-loaded (``lazy='select'``). This relationship is
            read‑only; to create or update an assessment, assign the ``event_id`` directly
            or use the event's ``impact_assessment`` attribute if bidirectional synchronisation
            is configured on the ``Event`` side.

    **Loading strategies and performance considerations:**

        The relationship uses ``lazy='select'`` (load on first access). When fetching an
        event together with its impact assessment, always use eager loading to avoid N+1
        queries:

        .. code-block:: python

            from sqlalchemy.orm import selectinload

            events_with_assessment = (
                session.query(Event)
                .options(selectinload(Event.impact_assessment))
                .all()
            )

        Because this table has no auto‑increment defaults other than the primary key,
        ``eager_defaults = False`` is safe to uncomment in ``__mapper_args__`` for bulk
        insert performance.

    **Usage examples:**

        Create a new impact assessment for an existing event:

        >>> assessment = ImpactAssessment(
        ...     event_id=event.id,
        ...     strategic_significance=StrategicSignificance.HIGH,
        ...     casualties_killed=120,
        ...     economic_impact_usd=Decimal('50000000.00')
        ... )
        >>> session.add(assessment)
        >>> session.commit()

        Update political impact after diplomatic fallout:

        >>> assessment.political_impact = PoliticalImpact.DETERIORATED
        >>> session.commit()

        Query assessments with high economic impact:

        >>> high_cost = session.query(ImpactAssessment).filter(
        ...     ImpactAssessment.economic_impact_usd > Decimal('100000000')
        ... ).all()

    .. seealso::
        :class:`Event`
        :class:`StrategicSignificance`
        :class:`PoliticalImpact`
        :class:`LegalPrecedent`
    """
    __repr_fields__ = ('id', 'event_id', 'strategic_significance')
    
    @declared_attr
    def __mapper_args__(cls) -> Any:
        args: Any = super().__mapper_args__.copy()
        # args["eager_defaults"] = False
        return args
    
    __table_args__: tuple[SchemaItem | dict[str, Any], ...] = (        
        CheckConstraint(
            "(casualties_killed IS NULL OR casualties_killed >= 0) AND "
            "(casualties_wounded IS NULL OR casualties_wounded >= 0) AND "
            "(displaced_persons IS NULL OR displaced_persons >= 0) AND "
            "(economic_impact_usd IS NULL OR economic_impact_usd >= 0)", 
            name="ck_impact_assessments_positive_or_null"
        ),
        CheckConstraint(
            "(notes IS NULL OR trim(notes) != '')", 
            name="ck_impact_assessments_fields_non_empty"
        ),
        
        {'comment': 'Models consequences and significance of incidents across multiple dimensions.'}
    )

    event_id: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey(_fk_ref(Base.metadata, 'event.id'), ondelete='CASCADE'),
        unique=True,
        nullable=False,
        comment='FOREIGN KEY to events table. Must not be NULL.'
    )

    strategic_significance: Mapped[StrategicSignificance | None] = mapped_column(
        db_enum(StrategicSignificance),
        nullable=True,
        comment='Strategic importance level (Low, Medium, High, Critical). Nullable if indeterminate.'
    )
    
    casualties_killed: Mapped[int | None] = mapped_column(
        Integer(), 
        nullable=True,
        comment='Count of fatalities. Nullable if not applicable.'
    )
    
    casualties_wounded: Mapped[int | None] = mapped_column(
        Integer(), 
        nullable=True,
        comment='Count of injured persons. Nullable if not applicable.'
    )
    
    displaced_persons: Mapped[int | None] = mapped_column(
        Integer(), 
        nullable=True,
        comment='Count of displaced persons. Nullable if not applicable.'
    )
    
    economic_impact_usd: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2), 
        nullable=True,
        comment='Economic impact in USD. Nullable if not applicable.'
    )
    
    political_impact: Mapped[PoliticalImpact | None] = mapped_column(
        db_enum(PoliticalImpact),
        nullable=True,
        comment='Assessment of diplomatic relationship consequences (Improved, Stable, Deteriorated, Ruptured). Nullable if not applicable.'
    )
    
    legal_precedent: Mapped[LegalPrecedent | None] = mapped_column(
        db_enum(LegalPrecedent),
        nullable=True,
        comment='Assessment of implications for international legal norms (Affirming, Neutral, Testing, Violating). Nullable if not applicable.'
    )
    
    event: Mapped['Event'] = relationship(
        'Event', 
        back_populates='impact_assessment',
        lazy='select',
        uselist=False,
        viewonly=True
    )
    