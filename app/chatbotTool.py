from app.memory import get_history, record_turn
from app.models import llm
from app.prompts import tool_agent_prompt
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from app.customToolAgent.customsTools import tools

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=tool_agent_prompt,
)


def _format_answer(content) -> str:
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, str):
                text_parts.append(block)
            elif isinstance(block, dict):
                text_parts.append(block.get("text", ""))
            elif hasattr(block, "text"):
                text_parts.append(block.text)

        return "".join(text_parts).strip()

    return str(content)


def ask(question: str) -> str:
    history = get_history()
    result = agent.invoke({"messages": [*history, HumanMessage(content=question)]})

    answer = _format_answer(result["messages"][-1].content)
    record_turn(question, answer)

    return answer
