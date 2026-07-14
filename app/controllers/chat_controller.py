"""HTTP-facing orchestration for chat requests."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.dto.chat_dto import ChatMessageDTO, ChatResponseDTO, SingleChatResponse
from app.service.llm_servise.chat_service import ChatService


def send_message(
    db: Session, user_id: int, payload: ChatMessageDTO
) -> SingleChatResponse:
    try:
        return ChatService.send_message(db, user_id, payload)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to get a response from the AI service.",
        ) from exc


def get_history(db: Session, user_id: int) -> ChatResponseDTO:
    return ChatService.get_history(db, user_id)
