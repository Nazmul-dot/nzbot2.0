from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a professional AI assistant.

Always answer clearly.

Explain concepts with examples.

If you don't know something,
say you don't know instead of guessing.
            """,
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)