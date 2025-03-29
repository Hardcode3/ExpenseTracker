"""Expense database model. """

from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    # user_id = Column(Integer, ForeignKey("users.id"))
    # user = relationship("User", back_populates="expenses")
