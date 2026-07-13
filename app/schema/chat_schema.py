"""
Stores chat history — the kind of table you'll want in almost
any AI backend so conversations can be replayed / used as context.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func

from app.database.base import Base


class ChatMessage(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())