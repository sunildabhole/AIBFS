from fastmcp import FastMCP
from app.database import SessionLocal
from app import reporting
from datetime import datetime
from typing import Optional
import os

tools_server = FastMCP(name="Reports")

UPLOADS_DIR = "uploads"

@tools_server.tool
def get_sales_report(start_date: str, end_date: str, company_id: int, format: Optional[str] = "json") -> dict:
    """
    Generates a sales report.
    :param start_date: The start date of the report (YYYY-MM-DD).
    :param end_date: The end date of the report (YYYY-MM-DD).
    :param company_id: The ID of the company.
    :param format: The format of the report (json or pdf).
    :return: The sales report data or the path to the PDF file.
    """
    db = SessionLocal()
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        report_data = reporting.get_sales_report(db, start_date=start_date_obj, end_date=end_date_obj, company_id=company_id, format=format)
        if format == "pdf":
            report_dir = os.path.join(UPLOADS_DIR, "reports", str(company_id))
            os.makedirs(report_dir, exist_ok=True)
            report_path = os.path.join(report_dir, f"sales_report_{start_date}_{end_date}.pdf")
            with open(report_path, "wb") as f:
                f.write(report_data)
            return {"report_path": report_path}
        return report_data
    finally:
        db.close()

@tools_server.tool
def get_low_stock_report(company_id: int, limit: int = 10, format: Optional[str] = "json") -> dict:
    """
    Generates a low stock report.
    :param company_id: The ID of the company.
    :param limit: The maximum number of products to include in the report.
    :param format: The format of the report (json or pdf).
    :return: The low stock report data or the path to the PDF file.
    """
    db = SessionLocal()
    try:
        report_data = reporting.get_low_stock_report(db, company_id=company_id, limit=limit, format=format)
        if format == "pdf":
            report_dir = os.path.join(UPLOADS_DIR, "reports", str(company_id))
            os.makedirs(report_dir, exist_ok=True)
            report_path = os.path.join(report_dir, "low_stock_report.pdf")
            with open(report_path, "wb") as f:
                f.write(report_data)
            return {"report_path": report_path}
        return report_data
    finally:
        db.close()

@tools_server.tool
def get_top_selling_report(company_id: int, limit: int = 10, format: Optional[str] = "json") -> dict:
    """
    Generates a top selling products report.
    :param company_id: The ID of the company.
    :param limit: The maximum number of products to include in the report.
    :param format: The format of the report (json or pdf).
    :return: The top selling products report data or the path to the PDF file.
    """
    db = SessionLocal()
    try:
        report_data = reporting.get_top_selling_report(db, company_id=company_id, limit=limit, format=format)
        if format == "pdf":
            report_dir = os.path.join(UPLOADS_DIR, "reports", str(company_id))
            os.makedirs(report_dir, exist_ok=True)
            report_path = os.path.join(report_dir, "top_selling_report.pdf")
            with open(report_path, "wb") as f:
                f.write(report_data)
            return {"report_path": report_path}
        return report_data
    finally:
        db.close()

@tools_server.tool
def get_total_revenue_report(company_id: int, format: Optional[str] = "json") -> dict:
    """
    Generates a total revenue report.
    :param company_id: The ID of the company.
    :param format: The format of the report (json or pdf).
    :return: The total revenue report data or the path to the PDF file.
    """
    db = SessionLocal()
    try:
        report_data = reporting.get_total_revenue_report(db, company_id=company_id, format=format)
        if format == "pdf":
            report_dir = os.path.join(UPLOADS_DIR, "reports", str(company_id))
            os.makedirs(report_dir, exist_ok=True)
            report_path = os.path.join(report_dir, "total_revenue_report.pdf")
            with open(report_path, "wb") as f:
                f.write(report_data)
            return {"report_path": report_path}
        return report_data
    finally:
        db.close()
