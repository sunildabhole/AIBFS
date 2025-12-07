from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas, billing
from app.database import get_db
from app.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=schemas.Order)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return billing.create_order_and_invoice(db, order=order, user_id=current_user.id, company_id=current_user.company_id)

@router.get("/", response_model=List[schemas.Order])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return crud.get_orders(db, company_id=current_user.company_id, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=schemas.Order)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    db_order = crud.get_order(db, order_id=order_id, company_id=current_user.company_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.delete("/{order_id}", response_model=schemas.Order)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    db_order = crud.delete_order(db, order_id=order_id, company_id=current_user.company_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
