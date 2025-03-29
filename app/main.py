from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.endpoints import expenses

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
