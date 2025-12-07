from fastmcp import FastMCP
from app.database import SessionLocal
from app import crud, schemas, ocr
from typing import List
import os

tools_server = FastMCP(name="Inventory")

UPLOADS_DIR = "uploads"

@tools_server.tool
def create_product(product: dict, company_id: int) -> dict:
    """
    Creates a new product.
    :param product: A dictionary with product data (name, description, price, stock).
    :param company_id: The ID of the company the product belongs to.
    :return: The created product data.
    """
    db = SessionLocal()
    try:
        product_schema = schemas.ProductCreate(**product)
        db_product = crud.create_product(db=db, product=product_schema, company_id=company_id)
        return {"id": db_product.id, "name": db_product.name, "price": db_product.price, "stock": db_product.stock}
    finally:
        db.close()

@tools_server.tool
def read_products(company_id: int, skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Reads a list of products.
    :param company_id: The ID of the company to fetch products from.
    :param skip: The number of products to skip.
    :param limit: The maximum number of products to return.
    :return: A list of product data.
    """
    db = SessionLocal()
    try:
        products = crud.get_products(db, company_id=company_id, skip=skip, limit=limit)
        return [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products]
    finally:
        db.close()

@tools_server.tool
def read_product(product_id: int, company_id: int) -> dict:
    """
    Reads a single product by ID.
    :param product_id: The ID of the product to read.
    :param company_id: The ID of the company the product belongs to.
    :return: The product data.
    """
    db = SessionLocal()
    try:
        db_product = crud.get_product(db, product_id=product_id, company_id=company_id)
        if db_product is None:
            return {"error": "Product not found"}
        return {"id": db_product.id, "name": db_product.name, "price": db_product.price, "stock": db_product.stock}
    finally:
        db.close()

@tools_server.tool
def update_product(product_id: int, product: dict, company_id: int) -> dict:
    """
    Updates a product.
    :param product_id: The ID of the product to update.
    :param product: A dictionary with the product data to update.
    :param company_id: The ID of the company the product belongs to.
    :return: The updated product data.
    """
    db = SessionLocal()
    try:
        product_schema = schemas.ProductUpdate(**product)
        db_product = crud.update_product(db, product_id=product_id, product=product_schema, company_id=company_id)
        if db_product is None:
            return {"error": "Product not found"}
        return {"id": db_product.id, "name": db_product.name, "price": db_product.price, "stock": db_product.stock}
    finally:
        db.close()

@tools_server.tool
def delete_product(product_id: int, company_id: int) -> dict:
    """
    Deletes a product.
    :param product_id: The ID of the product to delete.
    :param company_id: The ID of the company the product belongs to.
    :return: The deleted product data.
    """
    db = SessionLocal()
    try:
        db_product = crud.delete_product(db, product_id=product_id, company_id=company_id)
        if db_product is None:
            return {"error": "Product not found"}
        return {"id": db_product.id, "name": db_product.name, "price": db_product.price, "stock": db_product.stock}
    finally:
        db.close()

@tools_server.tool
def upload_product_image(product_id: int, image_bytes: bytes, filename: str, company_id: int, extract_text: bool = False) -> dict:
    """
    Uploads an image for a product.
    :param product_id: The ID of the product to upload the image for.
    :param image_bytes: The image content as bytes.
    :param filename: The name of the image file.
    :param company_id: The ID of the company the product belongs to.
    :param extract_text: Whether to extract text from the image using OCR.
    :return: A dictionary with information about the saved file and extracted text if requested.
    """
    db = SessionLocal()
    try:
        db_product = crud.get_product(db, product_id=product_id, company_id=company_id)
        if not db_product:
            return {"error": "Product not found"}

        image_dir = os.path.join(UPLOADS_DIR, "products", str(company_id))
        os.makedirs(image_dir, exist_ok=True)
        
        file_path = os.path.join(image_dir, f"{product_id}_{filename}")
        
        with open(file_path, "wb") as buffer:
            buffer.write(image_bytes)

        db_product.image = file_path
        db.commit()
        db.refresh(db_product)

        response = {"info": f"file '{filename}' saved at '{file_path}'"}
        if extract_text:
            text = ocr.extract_text_from_image(image_bytes)
            response["extracted_text"] = text

        return response
    finally:
        db.close()
