from fastmcp import FastMCP
from app.database import SessionLocal
from app import crud, schemas
from typing import List

tools_server = FastMCP(name="Customers")

@tools_server.tool
def create_customer(customer: dict, company_id: int) -> dict:
    """
    Creates a new customer.
    :param customer: A dictionary with customer data (name, email, phone, address).
    :param company_id: The ID of the company the customer belongs to.
    :return: The created customer data.
    """
    db = SessionLocal()
    try:
        customer_schema = schemas.CustomerCreate(**customer)
        db_customer = crud.create_customer(db=db, customer=customer_schema, company_id=company_id)
        return {"id": db_customer.id, "name": db_customer.name, "email": db_customer.email}
    finally:
        db.close()

@tools_server.tool
def read_customers(company_id: int, skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Reads a list of customers.
    :param company_id: The ID of the company to fetch customers from.
    :param skip: The number of customers to skip.
    :param limit: The maximum number of customers to return.
    :return: A list of customer data.
    """
    db = SessionLocal()
    try:
        customers = crud.get_customers(db, company_id=company_id, skip=skip, limit=limit)
        return [{"id": c.id, "name": c.name, "email": c.email} for c in customers]
    finally:
        db.close()

@tools_server.tool
def read_customer(customer_id: int, company_id: int) -> dict:
    """
    Reads a single customer by ID.
    :param customer_id: The ID of the customer to read.
    :param company_id: The ID of the company the customer belongs to.
    :return: The customer data.
    """
    db = SessionLocal()
    try:
        db_customer = crud.get_customer(db, customer_id=customer_id, company_id=company_id)
        if db_customer is None:
            return {"error": "Customer not found"}
        return {"id": db_customer.id, "name": db_customer.name, "email": db_customer.email}
    finally:
        db.close()

@tools_server.tool
def update_customer(customer_id: int, customer: dict, company_id: int) -> dict:
    """
    Updates a customer.
    :param customer_id: The ID of the customer to update.
    :param customer: A dictionary with the customer data to update.
    :param company_id: The ID of the company the customer belongs to.
    :return: The updated customer data.
    """
    db = SessionLocal()
    try:
        customer_schema = schemas.CustomerUpdate(**customer)
        db_customer = crud.update_customer(db, customer_id=customer_id, customer=customer_schema, company_id=company_id)
        if db_customer is None:
            return {"error": "Customer not found"}
        return {"id": db_customer.id, "name": db_customer.name, "email": db_customer.email}
    finally:
        db.close()

@tools_server.tool
def delete_customer(customer_id: int, company_id: int) -> dict:
    """
    Deletes a customer.
    :param customer_id: The ID of the customer to delete.
    :param company_id: The ID of the company the customer belongs to.
    :return: The deleted customer data.
    """
    db = SessionLocal()
    try:
        db_customer = crud.delete_customer(db, customer_id=customer_id, company_id=company_id)
        if db_customer is None:
            return {"error": "Customer not found"}
        return {"id": db_customer.id, "name": db_customer.name, "email": db_customer.email}
    finally:
        db.close()
