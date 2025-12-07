from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    model_config = {
        "from_attributes": True
    }


class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    company_id: int

class User(UserBase):
    id: int
    is_active: bool
    company_id: int
    model_config = {
        "from_attributes": True
    }

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class ProductBase(BaseModel):
    name: str
    price: float
    stock: int
    image: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image: Optional[str] = None

class Product(ProductBase):
    id: int
    company_id: int
    model_config = {
        "from_attributes": True
    }


class CustomerBase(BaseModel):
    name: str
    contact: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None

class Customer(CustomerBase):
    id: int
    company_id: int
    model_config = {
        "from_attributes": True
    }


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    price: float
    model_config = {
        "from_attributes": True
    }


class OrderBase(BaseModel):
    customer_id: int

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    user_id: int
    total_price: float
    date: datetime
    company_id: int
    pdf_invoice_path: Optional[str] = None
    items: List[OrderItem] = []
    model_config = {
        "from_attributes": True
    }


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    company_id: Optional[int] = None
