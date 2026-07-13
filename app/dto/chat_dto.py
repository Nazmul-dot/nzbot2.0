"""Pydantic contracts for the chat API."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ChatMessageDTO(BaseModel):
    """Message submitted by the authenticated user."""

    message: str = Field(min_length=1, max_length=10_000)


class SingleChatResponse(BaseModel):
    """One persisted prompt/response pair."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    message: str
    response: str
    created_at: datetime


class ChatResponseDTO(BaseModel):
    """All chat-history records belonging to the current user."""

    messages: list[SingleChatResponse] = Field(default_factory=list)
