from sqlalchemy import BIGINT, TIMESTAMP, String, Enum, func, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.schemas.enums import EventType
from app.db.base import Base

class RMAEvent(Base):
    __tablename__ = "rma_events"
    id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True
    )
    rma_request_id: Mapped[int] = mapped_column(
        BIGINT,
        nullable=False,
        foreign_key="rma_requests.id"
    )
    event_type: Mapped[str] = mapped_column(
        Enum(EventType, name="event_type_enum", create_type=False),
        nullable=False
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )
    actor_type: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    actor_id: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    message: Mapped[str] = mapped_column(
        String
    )
    meta: Mapped[str] = mapped_column(
        JSON
    )