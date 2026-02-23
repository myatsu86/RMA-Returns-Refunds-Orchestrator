from datetime import date, datetime
from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    serial_number: str
    warranty_expires_at: date
    model: str | None = None
    sku: str | None = None

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)