from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict
from app.schemas.enums import ShipmentDirection, ShipmentStatus


ShippingCostPayer = Literal["customer", "emerson", "western_digital"]


class ReturnShipmentBase(BaseModel):
    direction: ShipmentDirection
    carrier: Optional[str] = None
    tracking_number: Optional[str] = None
    label_provided_by_seagate: bool = False
    shipping_cost_payer: ShippingCostPayer
    status: ShipmentStatus = ShipmentStatus.label_created


class ReturnShipmentCreate(ReturnShipmentBase):
    rma_request_id: int


class ReturnShipmentUpdate(BaseModel):
    direction: Optional[ShipmentDirection] = None
    carrier: Optional[str] = None
    tracking_number: Optional[str] = None
    label_provided_by_seagate: Optional[bool] = None
    shipping_cost_payer: Optional[ShippingCostPayer] = None
    status: Optional[ShipmentStatus] = None
    delivered_at: Optional[datetime] = None


class ReturnShipmentRead(BaseModel):
    id: int
    rma_request_id: int
    direction: ShipmentDirection
    carrier: Optional[str]
    tracking_number: Optional[str]
    label_provided_by_seagate: bool
    shipping_cost_payer: ShippingCostPayer
    status: ShipmentStatus
    created_at: datetime
    delivered_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)