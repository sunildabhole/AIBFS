from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from app import crud, models, schemas, ocr
from app.database import get_db
from app.auth import get_current_active_user
import os

router = APIRouter()

UPLOADS_DIR = "uploads"

@router.post("/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return crud.create_product(db=db, product=product, company_id=current_user.company_id)

@router.get("/", response_model=List[schemas.Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return crud.get_products(db, company_id=current_user.company_id, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=schemas.Product)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    db_product = crud.get_product(db, product_id=product_id, company_id=current_user.company_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    db_product = crud.update_product(db, product_id=product_id, product=product, company_id=current_user.company_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}", response_model=schemas.Product)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    db_product = crud.delete_product(db, product_id=product_id, company_id=current_user.company_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/{product_id}/image")
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    extract_text: bool = False,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    db_product = crud.get_product(db, product_id=product_id, company_id=current_user.company_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    image_dir = os.path.join(UPLOADS_DIR, "products", str(current_user.company_id))
    os.makedirs(image_dir, exist_ok=True)
    
    file_path = os.path.join(image_dir, f"{product_id}_{file.filename}")
    
    image_bytes = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(image_bytes)

    db_product.image = file_path
    db.commit()
    db.refresh(db_product)

    response = {"info": f"file '{file.filename}' saved at '{file_path}'"}
    if extract_text:
        text = ocr.extract_text_from_image(image_bytes)
        response["extracted_text"] = text

    return response
