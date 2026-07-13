from sqlalchemy.orm import Session

from app.core.config import settings  



def save_chat(db: Session, payload: ChatMessageDTO) -> ChatMessage:
    chat:ChatMessage = save_chat_message(db, payload)
    return SingleChatResponse.model_validate(chat)


def history(db: Session, user_id: int):
    chats = get_chat_history_by_user_id(db, user_id)
    return ChatResponseDTO(messages=[SingleChatResponse.model_validate(chat) for chat in chats])