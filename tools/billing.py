from fastmcp import FastMCP
from app.database import SessionLocal
from app import crud, schemas
from app.utils.pdf_generator import generate_invoice_pdf
import os

tools_server = FastMCP(name="Billing")

UPLOADS_DIR = "uploads"

@tools_server.tool
def create_order_and_invoice(order: dict, user_id: int, company_id: int) -> dict:
    """
    Creates an order and generates an invoice PDF.

    :param order: A dictionary representing the order, with keys 'items' (a list of dictionaries with 'product_id' and 'quantity') and 'customer_id'.
    :param user_id: The ID of the user creating the order.
    :param company_id: The ID of the company for which the order is being created.
    :return: A dictionary with the order details and the path to the invoice PDF.
    """
    db = SessionLocal()
    try:
        order_schema = schemas.OrderCreate(**order)
        db_order = crud.create_order(db, order=order_schema, user_id=user_id, company_id=company_id)
        if not db_order:
            return {"error": "Not enough stock or product not found"}

        pdf_buffer = generate_invoice_pdf(db_order)
        
        invoice_dir = os.path.join(UPLOADS_DIR, "invoices", str(company_id))
        os.makedirs(invoice_dir, exist_ok=True)
        
        invoice_path = os.path.join(invoice_dir, f"invoice_{db_order.id}.pdf")
        
        with open(invoice_path, "wb") as f:
            f.write(pdf_buffer.getvalue())
            
        db_order.pdf_invoice_path = invoice_path
        db.commit()
        db.refresh(db_order)
        
        return {"order_id": db_order.id, "invoice_path": invoice_path}
    finally:
        db.close()
