from sqlalchemy import BIGINT, String, TIMESTAMP, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.models.enums import RMAStatus
from app.db.base import Base

class RefundTransaction(Base):
    __tablename__ = "refund_transactions"
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
    
    currency: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    status: Mapped[str] = mapped_column(
        Enum(RMAStatus, name="refund_status_enum", create_type=False),
        nullable=False
    )
    payment_method: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    processor_reference: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    queued_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP,
        nullable=False,
    )
    processed_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP,
        nullable=True
    )
    failure_reason: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    