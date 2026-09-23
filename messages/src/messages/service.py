from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database.models import Message
from .schemas import MessageCreate, MessageResponse

class MessageService:
    def create_message(self, session: Session, payload: MessageCreate) -> MessageResponse:
        try:
            with session.begin():
                message = Message(text=payload.text)
                session.add(message)
                session.flush()
                session.refresh(message)
            return MessageResponse.model_validate(message)
        except SQLAlchemyError as error:
            # We raise a custom exception or just the SQLAlchemyError
            # The controller will map this to an HTTPException
            raise error

    def get_messages(self, session: Session) -> list[MessageResponse]:
        try:
            rows = session.execute(
                select(Message).order_by(Message.created_at.asc(), Message.id.asc())
            ).scalars().all()
            return [MessageResponse.model_validate(row) for row in rows]
        except SQLAlchemyError as error:
            raise error
