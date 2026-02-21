from sqlalchemy import BIGINT, String, Boolean, TIMESTAMP, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.enums import ShipmentDirection, ShipmentStatus
from app.db.base import Base

class ReturnShipment(Base):
    __tablename__ = "return_shipments"
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
    direction: Mapped[str] = mapped_column(
        Enum(ShipmentDirection, name="shipment_direction_enum", create_type=False),
        nullable=False  
    )
    carrier: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    tracking_number: Mapped[str] = mapped_column(   
        String,
        nullable=False
    )
    label_provided_by_seagate: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )
    shipping_cost_payer: Mapped[str] = mapped_column(   
        String,
        nullable=False
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )
    delivered_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP,
        nullable=True
    )