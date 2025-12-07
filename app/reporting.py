from sqlalchemy.orm import Session
from datetime import datetime
import io
import csv
from fastapi.responses import StreamingResponse

from app import crud
from app.utils.pdf_generator import generate_sales_report_pdf, generate_low_stock_report_pdf, generate_top_selling_report_pdf, generate_total_revenue_report_pdf

def get_sales_report(db: Session, start_date: datetime, end_date: datetime, company_id: int, format: str = "json"):
    sales = crud.get_sales_by_date(db, start_date=start_date, end_date=end_date, company_id=company_id)
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["order_id", "customer_id", "total_price", "date"])
        for sale in sales:
            writer.writerow([sale.id, sale.customer_id, sale.total_price, sale.date])
        return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=sales_report.csv"})
    elif format == "pdf":
        pdf_buffer = generate_sales_report_pdf(sales, start_date, end_date)
        return StreamingResponse(iter([pdf_buffer.getvalue()]), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=sales_report.pdf"})
    return sales

def get_low_stock_report(db: Session, company_id: int, limit: int, format: str = "json"):
    products = crud.get_low_stock_products(db, company_id=company_id, limit=limit)
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["product_id", "name", "stock"])
        for product in products:
            writer.writerow([product.id, product.name, product.stock])
        return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=low_stock_report.csv"})
    elif format == "pdf":
        pdf_buffer = generate_low_stock_report_pdf(products)
        return StreamingResponse(iter([pdf_buffer.getvalue()]), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=low_stock_report.pdf"})
    return products

def get_top_selling_report(db: Session, company_id: int, limit: int, format: str = "json"):

    products = crud.get_top_selling_products(db, company_id=company_id, limit=limit)

    if format == "csv":

        output = io.StringIO()

        writer = csv.writer(output)

        writer.writerow(["product_id", "name", "total_quantity"])

        for product, total_quantity in products:

            writer.writerow([product.id, product.name, total_quantity])

        return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=top_selling_report.csv"})

    elif format == "pdf":

        pdf_buffer = generate_top_selling_report_pdf(products)

        return StreamingResponse(iter([pdf_buffer.getvalue()]), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=top_selling_report.pdf"})

    return [{"product": product, "total_quantity": total_quantity} for product, total_quantity in products]

def get_total_revenue_report(db: Session, company_id: int, format: str = "json"):
    total_revenue = crud.get_total_revenue(db, company_id=company_id)
    if format == "pdf":
        pdf_buffer = generate_total_revenue_report_pdf(total_revenue)
        return StreamingResponse(iter([pdf_buffer.getvalue()]), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=total_revenue_report.pdf"})
    return {"total_revenue": total_revenue or 0}
