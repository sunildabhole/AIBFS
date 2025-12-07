from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import datetime

from . import models, schemas
from .utils import jwt_handler

# Company
def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

def get_company_by_name(db: Session, name: str):
    return db.query(models.Company).filter(models.Company.name == name).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()

def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(name=company.name)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

# User
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, company_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.company_id == company_id).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = jwt_handler.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        company_id=user.company_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Product
def get_product(db: Session, product_id: int, company_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id, models.Product.company_id == company_id).first()

def get_products(db: Session, company_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Product).filter(models.Product.company_id == company_id).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate, company_id: int):
    db_product = models.Product(**product.dict(), company_id=company_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate, company_id: int):
    db_product = get_product(db, product_id, company_id)
    if db_product:
        update_data = product.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int, company_id: int):
    db_product = get_product(db, product_id, company_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

# Customer
def get_customer(db: Session, customer_id: int, company_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id, models.Customer.company_id == company_id).first()

def get_customers(db: Session, company_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).filter(models.Customer.company_id == company_id).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate, company_id: int):
    db_customer = models.Customer(**customer.dict(), company_id=company_id)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer: schemas.CustomerUpdate, company_id: int):
    db_customer = get_customer(db, customer_id, company_id)
    if db_customer:
        update_data = customer.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int, company_id: int):
    db_customer = get_customer(db, customer_id, company_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer

# Order
def get_order(db: Session, order_id: int, company_id: int):
    return db.query(models.Order).options(joinedload(models.Order.items).joinedload(models.OrderItem.product), joinedload(models.Order.customer)).filter(models.Order.id == order_id, models.Order.company_id == company_id).first()

def get_orders(db: Session, company_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Order).filter(models.Order.company_id == company_id).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate, user_id: int, company_id: int):
    total_price = 0
    for item in order.items:
        product = get_product(db, item.product_id, company_id)
        if not product or product.stock < item.quantity:
            return None
        total_price += product.price * item.quantity

    db_order = models.Order(
        customer_id=order.customer_id,
        user_id=user_id,
        total_price=total_price,
        company_id=company_id
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        product = get_product(db, item.product_id, company_id)
        product.stock -= item.quantity
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

# Reporting
def get_sales_by_date(db: Session, start_date: datetime, end_date: datetime, company_id: int):
    return db.query(models.Order).filter(models.Order.date.between(start_date, end_date), models.Order.company_id == company_id).all()

def get_low_stock_products(db: Session, company_id: int, limit: int = 10):
    return db.query(models.Product).filter(models.Product.stock < limit, models.Product.company_id == company_id).all()

def get_top_selling_products(db: Session, company_id: int, limit: int = 10):
    return db.query(models.Product, func.sum(models.OrderItem.quantity).label('total_quantity')).join(models.OrderItem, models.OrderItem.product_id == models.Product.id).filter(models.Product.company_id == company_id).group_by(models.Product.id).order_by(func.sum(models.OrderItem.quantity).desc()).limit(limit).all()

def get_total_revenue(db: Session, company_id: int):
    return db.query(func.sum(models.Order.total_price)).filter(models.Order.company_id == company_id).scalar()

# AI
def get_product_sales_history(db: Session, product_id: int, company_id: int):
    return db.query(models.Order.date, models.OrderItem.quantity).join(models.OrderItem).filter(models.OrderItem.product_id == product_id, models.Order.company_id == company_id).all()