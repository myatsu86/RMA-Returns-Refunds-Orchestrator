from sqlalchemy import BIGINT, String, DateTime, Enum, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from backend.app.schemas.enums import PurchaseSource, ProductCondition, RMAStatus, RMADecision

class RMARequest(Base):
    __tablename__ = "rma_requests"
    id: Mapped[BIGINT] = mapped_column(
        BIGINT, 
        primary_key=True, 
        autoincrement=True
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    serial_number: Mapped[String] = mapped_column(
        String,
        nullable=False
    )
    purchase_source: Mapped[PurchaseSource] = mapped_column(
        Enum(PurchaseSource),
        nullable=False
    )
    delivery_date: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=True
    )
    customer_reported_condition: Mapped[ProductCondition] = mapped_column(
        Enum(ProductCondition),
        nullable=True
    )
    data_responsibility_acknowledged: Mapped[Boolean] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    status: Mapped[RMAStatus] = mapped_column(
        Enum(RMAStatus),
        nullable=False,
        default=RMAStatus.pending
    )   
    decision: Mapped[String] = mapped_column(
        Enum(RMADecision),
        nullable=True
    )
    decision_reason: Mapped[String] = mapped_column(
        String,
        nullable=True
    )
    decided_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    rma_number: Mapped[String] = mapped_column(
        String,
        nullable=True,
        unique=True
    )
    warranty_checked_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    warranty_valid: Mapped[Boolean] = mapped_column(
        Boolean,
        nullable=True
    )
        


