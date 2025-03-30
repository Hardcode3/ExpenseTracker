from typing import List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse

router = APIRouter()


def retrieve_transaction(transaction_id: uuid.UUID, db: Session) -> Transaction:
    """Gets a single transaction or raise if non existent.

    Raises:
        HTTPException (404 Not Found) if the transaction does not exist.
    """
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).one_or_none()

    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction with ID {transaction_id} not found")

    return transaction


@router.post(
    "/",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db)
) -> TransactionResponse:

    transaction = Transaction(
        amount=data.amount,
        method=data.method,
        date=data.date,
        description=data.description,
    )
    db.add(transaction)
    try:
        db.commit()
        db.refresh(transaction)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database constraint violation") from e

    return transaction.to_response()


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
    status_code=status.HTTP_200_OK,
)
def get_single_transaction(
    transaction_id: uuid.UUID,
    db: Session = Depends(get_db)
) -> TransactionResponse:

    transaction = retrieve_transaction(transaction_id, db)
    return transaction.to_response()


@router.get(
    "/",
    response_model=List[TransactionResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_transactions(
    db: Session = Depends(get_db),
    offset: int = Query(0, ge=0, description="Offset must be 0 or greater (defaults to 0)"),
    limit: int = Query(10, ge=1, le=100, description="Limit must be between 1 and 100 (defaults to 10)"),
) -> List[TransactionResponse]:

    transactions = db.query(Transaction).offset(offset).limit(limit).all()
    return [t.to_response() for t in transactions]


@router.patch(
    "/{transaction_id}",
    response_model=TransactionResponse,
    status_code=status.HTTP_200_OK,
)
def update_transaction(
    transaction_id: uuid.UUID,
    data: TransactionUpdate,
    db: Session = Depends(get_db),
) -> TransactionResponse:

    transaction = retrieve_transaction(transaction_id, db)

    update_data = data.model_dump(exclude_unset=True)

    field_mapping = {
        "amount": "amount",
        "description": "description",
        "method": "method",
        "date": "date"
    }

    for schema_field, db_field in field_mapping.items():
        if schema_field in update_data:
            setattr(transaction, db_field, update_data[schema_field])

    db.commit()
    db.refresh(transaction)

    return transaction.to_response()


@router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_transaction(
        transaction_id: uuid.UUID,
        db: Session = Depends(get_db),
) -> None:

    transaction = retrieve_transaction(transaction_id, db)

    try:
        db.delete(transaction)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cannot delete transaction due to related records") from e
