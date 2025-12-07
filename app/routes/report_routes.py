from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app import reporting, models
from app.database import get_db
from app.auth import get_current_active_user

router = APIRouter()

@router.get("/sales")
def get_sales_report(
    start_date: datetime,
    end_date: datetime,
    format: Optional[str] = "json",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return reporting.get_sales_report(db, start_date=start_date, end_date=end_date, company_id=current_user.company_id, format=format)

@router.get("/sales/pdf")
def get_sales_report_pdf(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    pdf_content = reporting.get_sales_report(db, start_date=start_date, end_date=end_date, company_id=current_user.company_id, format="pdf")
    return Response(content=pdf_content, media_type="application/pdf")

@router.get("/low-stock")
def get_low_stock_report(
    limit: int = 10,
    format: Optional[str] = "json",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return reporting.get_low_stock_report(db, company_id=current_user.company_id, limit=limit, format=format)

@router.get("/low-stock/pdf")
def get_low_stock_report_pdf(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    pdf_content = reporting.get_low_stock_report(db, company_id=current_user.company_id, limit=limit, format="pdf")
    return Response(content=pdf_content, media_type="application/pdf")

@router.get("/top-selling")
def get_top_selling_report(
    limit: int = 10,
    format: Optional[str] = "json",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return reporting.get_top_selling_report(db, company_id=current_user.company_id, limit=limit, format=format)

@router.get("/top-selling/pdf")
def get_top_selling_report_pdf(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    pdf_content = reporting.get_top_selling_report(db, company_id=current_user.company_id, limit=limit, format="pdf")
    return Response(content=pdf_content, media_type="application/pdf")

@router.get("/total-revenue")
def get_total_revenue_report(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return reporting.get_total_revenue_report(db, company_id=current_user.company_id)

@router.get("/total-revenue/pdf")
def get_total_revenue_report_pdf(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    pdf_content = reporting.get_total_revenue_report(db, company_id=current_user.company_id, format="pdf")
    return Response(content=pdf_content, media_type="application/pdf")
