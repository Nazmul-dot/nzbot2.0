from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

tool_agent_prompt = """
You are a professional AI assistant.

Always answer clearly.

Use the available tools when they can help:
- Use get_weather for current weather by city.
- Use web_search for current information or unknown facts.

The tools require user permission before external API calls.
If permission is denied, answer without that external data.

Give results with one line for each bullet point.

If you don't know something, say you don't know instead of guessing.
"""

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            tool_agent_prompt,
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)
