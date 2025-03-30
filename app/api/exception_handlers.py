import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)


def sqlalchemy_exception_handler(request, exc) -> None:
    """Global handler for all SQLAlchemy errors."""
    # pylint: disable = unused-argument

    # log the error and do not include it into user messages
    # to avoid exposing sensitive database information
    logger.error("Database error: %s", str(exc))

    if isinstance(exc, IntegrityError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error. Possible duplicate entry or constraint violation."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="A database error occurred. Please try again later."
    )
