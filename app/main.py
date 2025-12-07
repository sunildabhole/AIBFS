from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse # Added
from app.database import engine, Base
from app.routes import auth_routes, product_routes, customer_routes, order_routes, report_routes, ai_routes, user_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Powered Inventory & Billing + Stock Prediction System",
    description="This is a production-ready FastAPI project with a lot of features.",
    version="1.0.0",
)

# Mount static files (like favicon.ico)


app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(product_routes.router, prefix="/products", tags=["Products"])
app.include_router(customer_routes.router, prefix="/customers", tags=["Customers"])
app.include_router(order_routes.router, prefix="/orders", tags=["Orders"])
app.include_router(report_routes.router, prefix="/reports", tags=["Reports"])
app.include_router(ai_routes.router, prefix="/ai", tags=["AI"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])



@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the AI-Powered Inventory & Billing + Stock Prediction System!"}