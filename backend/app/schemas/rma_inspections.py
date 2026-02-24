from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.enums import InspectionSource, ProductCondition


# Shared (editable) fields
class RMAInspectionBase(BaseModel):
    source: InspectionSource = InspectionSource.warehouse
    inspector_id: Optional[str] = None
    hardware_failure_confirmed: bool = False
    failure_notes: Optional[str] = None
    verified_condition: Optional[ProductCondition] = None
    condition_notes: Optional[str] = None


# POST /inspections (usually you provide rma_request_id)
class RMAInspectionCreate(RMAInspectionBase):
    rma_request_id: int


# PATCH /inspections/{id}
class RMAInspectionUpdate(BaseModel):
    source: Optional[InspectionSource] = None
    inspector_id: Optional[str] = None
    hardware_failure_confirmed: Optional[bool] = None
    failure_notes: Optional[str] = None
    verified_condition: Optional[ProductCondition] = None
    condition_notes: Optional[str] = None


# Response model (DB object)
class RMAInspectionRead(BaseModel):
    id: int
    rma_request_id: int
    inspected_at: datetime
    source: InspectionSource
    inspector_id: Optional[str]
    hardware_failure_confirmed: bool
    failure_notes: Optional[str]
    verified_condition: Optional[ProductCondition]
    condition_notes: Optional[str]

    model_config = ConfigDict(from_attributes=True)