"""Chat orchestration: database history, prompt, LLM call, and persistence."""

from sqlalchemy.orm import Session

from app.dao.chat_dao import ChatDAO
from app.dto.chat_dto import ChatMessageDTO, ChatResponseDTO, SingleChatResponse
from app.service.llm_servise.models import get_llm
from langchain_core.messages import AIMessage, HumanMessage
from app.service.llm_servise.prompts import chat_prompt

class ChatService:
    @staticmethod
    def send_message(
        db: Session, user_id: int, payload: ChatMessageDTO
    ) -> SingleChatResponse:


        history_records = ChatDAO.get_chat_history_by_user_id(db, user_id)
        history = []
        for record in history_records:
            history.append(HumanMessage(content=record.message))
            history.append(AIMessage(content=record.response))

        chain = chat_prompt | get_llm()
        llm_response = chain.invoke({"question": payload.message, "history": history})
        response_text = str(llm_response.content)

        chat = ChatDAO.save_chat_message(
            db=db,
            user_id=user_id,
            message=payload.message,
            response=response_text,
        )
        return SingleChatResponse.model_validate(chat)

    @staticmethod
    def get_history(db: Session, user_id: int) -> ChatResponseDTO:
        chats = ChatDAO.get_chat_history_by_user_id(db, user_id)
        return ChatResponseDTO(
            messages=[SingleChatResponse.model_validate(chat) for chat in chats]
        )