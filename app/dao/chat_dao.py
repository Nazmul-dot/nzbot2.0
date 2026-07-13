"""Database access for persisted chat history."""

from sqlalchemy.orm import Session

from app.schema.chat_schema import ChatMessage


class ChatDAO:
    @staticmethod
    def save_chat_message(
        db: Session, user_id: int, message: str, response: str
    ) -> ChatMessage:
        chat = ChatMessage(user_id=user_id, message=message, response=response)
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat

    @staticmethod
    def get_chat_history_by_user_id(db: Session, user_id: int) -> list[ChatMessage]:
        return (
            db.query(ChatMessage)
            .filter(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.asc(), ChatMessage.id.asc())
            .all()
        )
