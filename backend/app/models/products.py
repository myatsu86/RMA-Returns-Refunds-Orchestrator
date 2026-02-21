from sqlalchemy import String, Date, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"
    serial_number: Mapped[str] = mapped_column(
        String,
        primary_key=True
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
    model: Mapped[str] = mapped_column(
        String, 
        nullable=False
    )
    sku: Mapped[str] = mapped_column(
        String, 
        nullable=False
    )
    warranty_expires_at: Mapped[Date] = mapped_column(
        Date,
        nullable=False
    )