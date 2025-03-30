"""Expense database model. """

from datetime import datetime
import uuid
from enum import Enum as PyEnum

from sqlalchemy import Column, String, Float, DateTime, Enum, UUID

from app.core.database import Base
from app.schemas.transaction import TransactionResponse


class TransactionMethod(str, PyEnum):
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    CASH = "cash"
    PAYPAL = "paypal"
    OTHER = "other"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    amount = Column(Float, nullable=False)
    method = Column(Enum(TransactionMethod), nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
    description = Column(String(255), nullable=True)


    def to_response(self) -> TransactionResponse:
        """Convert a Transaction ORM object into a TransactionResponse Pydantic model."""
        return TransactionResponse(
            id=self.id,
            amount=self.amount,
            method=self.method,
            date=self.date,
            description=self.description,
        )
