from sqlalchemy import BIGINT, Boolean, String, TIMESTAMP, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.schemas.enums import InspectionSource
from app.db.base import Base

class RMAInspection(Base):
    __tablename__ = "rma_inspections"
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
    inspected_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )  
    source: Mapped[str] = mapped_column(
        Enum(InspectionSource, name="inspection_source_enum", create_type=False),
        nullable=False
    )
    inspector_id: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    hardware_failure_confirmed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )
    failure_notes: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    verified_condition: Mapped[str] = mapped_column(
        Enum(InspectionSource, name="inspection_source_enum", create_type=False),
        nullable=True
    )