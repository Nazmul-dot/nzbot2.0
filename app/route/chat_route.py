"""JWT-protected chat endpoints for Postman and other API clients."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import chat_controller
from app.database.connection import get_db
from app.dto.chat_dto import ChatMessageDTO, ChatResponseDTO, SingleChatResponse
from app.route.user_route import get_current_user


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=SingleChatResponse, status_code=201)
def send_message(
    payload: ChatMessageDTO,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    return chat_controller.send_message(db, current_user_id, payload)


@router.get("/history", response_model=ChatResponseDTO)
def get_history(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    return chat_controller.get_history(db, current_user_id)
