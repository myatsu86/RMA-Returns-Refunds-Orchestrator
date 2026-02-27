from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.enums import PurchaseSource, ProductCondition, RMAStatus, RMADecision


class RMARequestBase(BaseModel):
    serial_number: str
    purchase_source: PurchaseSource
    delivery_date: date | None = None
    customer_reported_condition: ProductCondition | None = None
    data_responsibility_acknowledged: bool | None = None

class RMARequestCreate(RMARequestBase):
    pass

class RMARequestRead(BaseModel):
    id: int
    created_at: datetime
    serial_number: str
    purchase_source: PurchaseSource
    delivery_date: date | None
    customer_reported_condition: ProductCondition | None
    data_responsibility_acknowledged: bool
    status: RMAStatus
    decision: RMADecision | None
    decision_reason: str | None
    decided_at: datetime | None
    rma_number: str | None
    warranty_checked_at: datetime | None
    warranty_valid: bool | None

    model_config = ConfigDict(from_attributes=True)

class RMARequestUpdate(BaseModel):
    purchase_source: Optional[PurchaseSource] = None
    delivery_date: Optional[date] = None
    customer_reported_condition: Optional[ProductCondition] = None
    data_responsibility_acknowledged: Optional[bool] = None

class RMAAdminUpdate(BaseModel):
    status: Optional[RMAStatus] = None
    decision: Optional[RMADecision] = None
    decision_reason: Optional[str] = None