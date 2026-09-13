from typing import Annotated, TypeAlias

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .db import get_session
from .schemas import MessageCreate, MessageResponse

router = APIRouter(prefix="/api", tags=["messages"])

SessionDependency: TypeAlias = Annotated[Session, Depends(get_session)]


@router.post(
    "/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_message(payload: MessageCreate, session: SessionDependency) -> MessageResponse:
    try:
        result = session.execute(
            text(
                """
                INSERT INTO messages (text)
                VALUES (:text)
                RETURNING id, text, created_at, status
                """
            ),
            {"text": payload.text},
        ).mappings().one()
        session.commit()
    except SQLAlchemyError as error:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to save message",
        ) from error
    return MessageResponse.model_validate(result)


@router.get("/messages", response_model=list[MessageResponse])
def get_messages(session: SessionDependency) -> list[MessageResponse]:
    try:
        rows = session.execute(
            text(
                """
                SELECT id, text, created_at, status
                FROM messages
                ORDER BY created_at ASC, id ASC
                """
            )
        ).mappings().all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to load messages",
        ) from error
    return [MessageResponse.model_validate(row) for row in rows]