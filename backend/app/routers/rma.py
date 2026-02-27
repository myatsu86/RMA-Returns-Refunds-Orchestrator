from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.models.rma_requests import RMARequest as RMARequestModel
from app.schemas.rma_requests import (
    RMARequestCreate,
    RMARequestRead,
    RMARequestUpdate,
    RMAAdminUpdate,
)
router = APIRouter(prefix="/rma-requests", tags=["rma-requests"])

@router.get("", response_model=list[RMARequestRead])
def list_rma_requests(db: Session = Depends(get_db), limit: int = 100, offset: int = 0):
    rma_requests = (
        db.query(RMARequestModel)
        .order_by(RMARequestModel.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return rma_requests

@router.post("/", response_model=RMARequestRead, status_code=status.HTTP_201_CREATED)
def create_rma_request(payload: RMARequestCreate, db: Session = Depends(get_db)):
    #rma_request = RMARequest(**payload.model_dump().values())
    # Create RMA Request with customer provided data. 
    # Admin fields will be set to default values and updated later by admin actions.
    rma_request = RMARequestModel(
    serial_number=payload.serial_number,
    purchase_source=payload.purchase_source,
    delivery_date=payload.delivery_date,
    customer_reported_condition=payload.customer_reported_condition,
    data_responsibility_acknowledged=payload.data_responsibility_acknowledged,
    )
    
    db.add(rma_request)
    db.commit()
    db.refresh(rma_request)
    return rma_request