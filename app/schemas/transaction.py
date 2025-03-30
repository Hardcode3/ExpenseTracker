"""API expense model. """
from typing import Optional
from datetime import datetime
from enum import StrEnum
import uuid

from pydantic import BaseModel, Field


class TransactionMethod(StrEnum):

    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    CASH = "cash"
    PAYPAL = "paypal"
    OTHER = "other"


class TransactionBase(BaseModel):

    amount: float = Field(..., description="Transaction amount (debit is negative and credit positive)")
    description: Optional[str] = Field(None, max_length=255)
    method: TransactionMethod
    date: datetime = Field(default_factory=datetime.now)


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):

    amount: Optional[float] = Field(None, description="Transaction amount (debit is negative and credit positive)")
    description: Optional[str] = Field(None, max_length=255)
    method: Optional[TransactionMethod] = None
    date: Optional[datetime] = None


class TransactionRead(TransactionBase):
    id: uuid.UUID


class TransactionResponse(TransactionBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
