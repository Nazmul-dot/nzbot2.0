# from app.memory import get_history, record_turn
# from app.models import llm
# from app.prompts import chat_prompt

# chain = chat_prompt | llm


# def ask(question: str):
#     history = get_history()

#     response = chain.invoke(
#         {
#             "question": question,
#             "history": history,
#         }
#     )

#     record_turn(question, response.content)

#     return response.content