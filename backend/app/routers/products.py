from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.models.products import Product
from app.schemas.products import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/{serial_number}")
def get_product(serial_number: str, db: Session = Depends(get_db)):
    product = db.get(Product, serial_number)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db), limit: int = 100, offset: int = 0):
    products = (
        db.query(Product)
        .order_by(Product.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return products

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    #Check duplicate serial number
    existing = db.get(Product, payload.serial_number)
    if existing:
        raise HTTPException(status_code=409, detail="Product with this serial number already exists")   
    #product = Product(**payload.model_dump().values())
    product = Product(
        serial_number=payload.serial_number,
        warranty_expires_at=payload.warranty_expires_at,
        model=payload.model,
        sku=payload.sku
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

