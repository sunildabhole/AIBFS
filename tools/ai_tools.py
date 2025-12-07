from fastmcp import FastMCP
from app.database import SessionLocal
from app import crud

import pandas as pd
from sklearn.linear_model import LinearRegression

tools_server = FastMCP(name="AI_Tools")

@tools_server.tool
def predict_stock(product_id: int, company_id: int, sales_data: list) -> dict:
    """
    Predicts the stock needed for a product for the next month based on historical sales data.
    :param product_id: The ID of the product to predict stock for.
    :param company_id: The ID of the company the product belongs to.
    :param sales_data: List of dictionaries containing 'date' and 'quantity' for historical sales.
    :return: A dictionary with the predicted stock for the next month.
    """
    db = SessionLocal()
    try:
        if not sales_data or len(sales_data) < 2:
            return {"product_id": product_id, "predicted_stock_next_month": 0.0}

        df = pd.DataFrame(sales_data, columns=['date', 'quantity'])
        df['date'] = pd.to_datetime(df['date'])
        df['days_since_start'] = (df['date'] - df['date'].min()).dt.days

        X = df[['days_since_start']]
        y = df['quantity']

        model = LinearRegression()
        model.fit(X, y)

        last_day = df['days_since_start'].max()
        next_month_days = pd.DataFrame({'days_since_start': range(last_day + 1, last_day + 31)})
        predicted_sales = model.predict(next_month_days)

        predicted_stock = max(0, sum(predicted_sales))

        return {"product_id": product_id, "predicted_stock_next_month": predicted_stock}
    finally:
        db.close()
