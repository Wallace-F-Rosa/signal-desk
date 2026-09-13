from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, String, func, text as sa_text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (
        CheckConstraint("length(trim(text)) > 0", name="ck_messages_text_not_blank"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(5000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="sent",
        server_default=sa_text("'sent'"),
    )
