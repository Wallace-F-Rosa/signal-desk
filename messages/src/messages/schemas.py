from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class MessageCreate(BaseModel):
    text: str = Field(min_length=1, max_length=5000)

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Message text must not be blank")
        return value


class MessageResponse(BaseModel):
    id: int
    text: str
    created_at: datetime
    status: str

    model_config = {"from_attributes": True}
