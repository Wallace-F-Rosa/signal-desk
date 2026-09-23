from typing import Annotated, TypeAlias

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database import get_session
from .schemas import MessageCreate, MessageResponse
from .service import MessageService

router = APIRouter(prefix="/api", tags=["messages"])

SessionDependency: TypeAlias = Annotated[Session, Depends(get_session)]

def get_message_service() -> MessageService:
    return MessageService()

@router.post(
    "/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    payload: MessageCreate, 
    session: SessionDependency, 
    service: MessageService = Depends(get_message_service)
) -> MessageResponse:
    try:
        return service.create_message(session, payload)
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save message",
        ) from error

@router.get("/messages", response_model=list[MessageResponse])
def get_messages(
    session: SessionDependency, 
    service: MessageService = Depends(get_message_service)
) -> list[MessageResponse]:
    try:
        return service.get_messages(session)
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to load messages",
        ) from error
