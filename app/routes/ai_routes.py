from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, ai
from app.database import get_db
from app.auth import get_current_active_user

router = APIRouter()

@router.get("/predict-stock/{product_id}")
async def predict_stock(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Predicts the stock needed for a product for the next month based on historical sales data.
    """
    sales_history = crud.get_product_sales_history(db, product_id=product_id, company_id=current_user.company_id)
    if not sales_history:
        raise HTTPException(status_code=404, detail="No sales history found for this product.")

    predicted_stock = await ai.train_and_predict_stock_via_mcp(
        product_id=product_id,
        company_id=current_user.company_id,
        sales_data=[{"date": str(s.date), "quantity": s.quantity} for s in sales_history]
    )
    return {"product_id": product_id, "predicted_stock_next_month": predicted_stock}
