# AI-Powered Inventory & Billing + Stock Prediction System

This is a production-ready FastAPI project with a comprehensive set of features for managing inventory, billing, and stock prediction.

## Features

- **FastAPI Backend:** A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **PostgreSQL Database:** A powerful, open-source object-relational database system.
- **SQLAlchemy ORM + Alembic Migrations:** A powerful and pythonic SQL toolkit and Object Relational Mapper, with Alembic for database migrations.
- **JWT Authentication:** Secure your endpoints with JSON Web Tokens (register/login).
- **Multi-Company Processing:** Support for multiple companies with separate inventory and orders.
- **CRUD Operations:** Endpoints for managing Users, Products, Customers, and Orders.
- **Product Image Upload + OCR:** Upload product images and extract text from them using OCR.
- **Billing System:** Create orders, auto-calculate the total price, and generate PDF invoices.
- **Reporting APIs:** Endpoints for sales, low stock, revenue, and top-selling products, with CSV download option.
- **AI Stock Prediction:** An endpoint to predict next month's stock needs for a product using a linear regression model.
- **Docker Compose:** A `docker-compose.yml` file is provided for easy setup of the PostgreSQL database and pgAdmin.
- **Gemini-Ready:** The project is structured to be easily integrated with Gemini AI for code generation and assistance.

## 1. Getting Started

### Prerequisites

- Python 3.7+
- Docker
- Tesseract OCR Engine (for the OCR functionality)

### 1.1. Create a Virtual Environment

```bash
python -m venv venv
```

### 1.2. Activate the Virtual Environment

**Windows:**

```bash
.\venv\Scripts\activate
```

**macOS/Linux:**

``` bash
source venv/bin/activate
```

### 1.3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 1.4. Set up Environment Variables

Create a `.env` file in the root of the project and add the following line:

``` DATABASE_URL=postgresql://user:password@localhost/aibfs_db
```

### 1.5. Start the Database with Docker

```bash
docker-compose up -d
```

This will start a PostgreSQL container and a pgAdmin container. You can access pgAdmin at `http://localhost:5050`.

### 1.6. Run Database Migrations

```bash
alembic upgrade head
```

This will create all the necessary tables in the database.

### 1.7. Run the FastAPI Server

```bash
uvicorn app.main:app --reload
```

The application will be running at `http://127.0.0.1:8000`. You can access the API documentation at `http://127.0.0.1:8000/docs`.

## 2. Testing the Application

You can use the interactive API documentation at `http://127.0.0.1:8000/docs` to test the endpoints.

Here's a suggested workflow for testing the application:

1. **Create a Company:** Go to the `/companies/` endpoint and create a new company.
2. **Create a User:** Go to the `/auth/register` endpoint and create a new user for the company you just created.
3. **Get a Token:** Go to the `/auth/token` endpoint and log in with the user you just created to get a JWT token.
4. **Authorize:** Click the "Authorize" button in the top right corner of the API documentation and enter your JWT token in the format `Bearer YOUR_TOKEN`.
5. **Test the Endpoints:** Now you can test the other endpoints, such as creating products, customers, and orders.

### 2.1. Generating a PDF Invoice

1. Create a product and a customer.
2. Create an order with the product and customer you just created.
3. Go to the `/orders/{order_id}` endpoint and get the ID of the order you just created.
4. Go to the `/orders/{order_id}` endpoint and you will find the `pdf_invoice_path` in the response.

### 2.2. Calling the Stock Prediction API

1. Create a product and a few orders with that product.
2. Go to the `/ai/predict-stock/{product_id}` endpoint and enter the ID of the product you created.
3. You will get a prediction of the stock needed for the next month.

## 3. Project Structure

```.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── auth.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── ocr.py
│   ├── ai.py
│   ├── billing.py
│   ├── reporting.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── product_routes.py
│   │   ├── customer_routes.py
│   │   ├── order_routes.py
│   │   ├── report_routes.py
│   │   └── ai_routes.py
│   └── utils/
│       ├── __init__.py
│       ├── jwt_handler.py
│       └── pdf_generator.py
├── migrations/
│   ├── versions/
│   │   └── ...
│   ├── env.py
│   └── script.py.mako
├── docker-compose.yml
├── requirements.txt
└── README.md
```
