from fastmcp import FastMCP
from app.database import SessionLocal
from app import crud
from typing import List

tools_server = FastMCP(name="Orders")

@tools_server.tool
def read_orders(company_id: int, skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Reads a list of orders.
    :param company_id: The ID of the company to fetch orders from.
    :param skip: The number of orders to skip.
    :param limit: The maximum number of orders to return.
    :return: A list of order data.
    """
    db = SessionLocal()
    try:
        orders = crud.get_orders(db, company_id=company_id, skip=skip, limit=limit)
        return [{"id": o.id, "customer_id": o.customer_id, "date": o.date.isoformat(), "total_price": o.total_price} for o in orders]
    finally:
        db.close()

@tools_server.tool
def read_order(order_id: int, company_id: int) -> dict:
    """
    Reads a single order by ID.
    :param order_id: The ID of the order to read.
    :param company_id: The ID of the company the order belongs to.
    :return: The order data.
    """
    db = SessionLocal()
    try:
        db_order = crud.get_order(db, order_id=order_id, company_id=company_id)
        if db_order is None:
            return {"error": "Order not found"}
        return {"id": db_order.id, "customer_id": db_order.customer_id, "date": db_order.date.isoformat(), "total_price": db_order.total_price, "items": [{"product_id": i.product_id, "quantity": i.quantity, "price": i.price} for i in db_order.items]}
    finally:
        db.close()
