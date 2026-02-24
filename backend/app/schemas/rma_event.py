from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from app.schemas.enums import EventType


class RMAEventBase(BaseModel):
    event_type: EventType
    actor_type: Optional[str] = None
    actor_id: Optional[str] = None
    message: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None


class RMAEventCreate(RMAEventBase):
    rma_request_id: int


class RMAEventRead(BaseModel):
    id: int
    rma_request_id: int
    event_type: EventType
    created_at: datetime
    actor_type: Optional[str]
    actor_id: Optional[str]
    message: Optional[str]
    meta: Optional[Dict[str, Any]]

    model_config = ConfigDict(from_attributes=True)