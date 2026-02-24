from __future__ import annotations
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.enums import RefundStatus


Currency = Literal["USD", "EUR", "GBP"]


class RefundTransactionBase(BaseModel):
    amount_cents: int = Field(..., gt=0)
    currency: Currency = "USD"
    status: RefundStatus = RefundStatus.queued
    payment_method: Optional[str] = None
    processor_reference: Optional[str] = None


class RefundTransactionCreate(RefundTransactionBase):
    rma_request_id: int


class RefundTransactionUpdate(BaseModel):
    status: Optional[RefundStatus] = None
    processor_reference: Optional[str] = None
    processed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None


class RefundTransactionRead(BaseModel):
    id: int
    rma_request_id: int
    amount_cents: int
    currency: Currency
    status: RefundStatus
    payment_method: Optional[str]
    processor_reference: Optional[str]
    queued_at: datetime
    processed_at: Optional[datetime]
    failure_reason: Optional[str]

    model_config = ConfigDict(from_attributes=True)