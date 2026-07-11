from langchain_core.messages import AIMessage, HumanMessage

_conversation: list = []


def get_history():
    return _conversation.copy()


def record_turn(question: str, answer: str):
    _conversation.append(HumanMessage(content=question))
    _conversation.append(AIMessage(content=answer))


def reset_history():
    _conversation.clear()
