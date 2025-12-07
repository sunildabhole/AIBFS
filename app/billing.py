from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import crud, schemas
from app.utils.pdf_generator import generate_invoice_pdf
import os

UPLOADS_DIR = "uploads"

def create_order_and_invoice(db: Session, order: schemas.OrderCreate, user_id: int, company_id: int):
    db_order = crud.create_order(db, order=order, user_id=user_id, company_id=company_id)
    if not db_order:
        raise HTTPException(status_code=400, detail="Not enough stock or product not found")

    pdf_buffer = generate_invoice_pdf(db_order)
    
    invoice_dir = os.path.join(UPLOADS_DIR, "invoices", str(company_id))
    os.makedirs(invoice_dir, exist_ok=True)
    
    invoice_path = os.path.join(invoice_dir, f"invoice_{db_order.id}.pdf")
    
    with open(invoice_path, "wb") as f:
        f.write(pdf_buffer.getvalue())
        
    db_order.pdf_invoice_path = invoice_path
    db.commit()
    db.refresh(db_order)
    
    return db_order
