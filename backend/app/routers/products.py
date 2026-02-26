from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.models.products import Product
from app.schemas.products import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/{serial_number}")
async def get_product(serial_number: str, db: Session = Depends(get_db)):
    product = db.get(Product, serial_number)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product