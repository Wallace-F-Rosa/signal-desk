from contextlib import asynccontextmanager
from typing import Annotated, TypeAlias

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .database import engine, get_session, init_db
from .schemas import MessageCreate, MessageResponse


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Signal Desk Message Service", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

SessionDependency: TypeAlias = Annotated[Session, Depends(get_session)]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is unavailable",
        ) from error
    return {"status": "ready"}


@app.post(
    "/api/messages",
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


@app.get("/api/messages", response_model=list[MessageResponse])
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