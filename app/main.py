from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from sqlalchemy.exc import SQLAlchemyError

from app.core.database import engine, Base
from app.api.endpoints import transaction
import app.api.exception_handlers as ExHandler

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")
app.add_exception_handler(SQLAlchemyError, ExHandler.sqlalchemy_exception_handler)

app.include_router(transaction.router, prefix="/transaction", tags=["Transactions"])

@app.get("/", include_in_schema=False)
async def redirect_to_swagger():
    return RedirectResponse(url="/docs")
