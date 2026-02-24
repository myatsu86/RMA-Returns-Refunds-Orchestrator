from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, ConfigDict, Field


class RMAPolicyLogBase(BaseModel):
    policy_id: str = Field(
        ...,
        pattern=r"^P[0-9]+$",
        description="Policy identifier like P1, P2, P10"
    )
    policy_version: str = "v1"
    engine_version: str = "rules-v1"
    matched: bool
    outcome: str
    details: Optional[Dict[str, Any]] = None


class RMAPolicyLogCreate(RMAPolicyLogBase):
    rma_request_id: int


class RMAPolicyLogUpdate(BaseModel):
    matched: Optional[bool] = None
    outcome: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class RMAPolicyLogRead(BaseModel):
    id: int
    rma_request_id: int
    policy_id: str
    policy_version: str
    engine_version: str
    evaluated_at: datetime
    matched: bool
    outcome: str
    details: Optional[Dict[str, Any]]

    model_config = ConfigDict(from_attributes=True)