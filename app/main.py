from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.core.database import engine, Base
from app.api.endpoints import expenses

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])

@app.get("/", include_in_schema=False)
async def redirect_to_swagger():
    return RedirectResponse(url="/docs")
