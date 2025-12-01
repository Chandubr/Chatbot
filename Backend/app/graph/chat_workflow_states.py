from typing import Annotated, TypedDict, List, Optional
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class ChatState(TypedDict, total=False):
    messages: Annotated[List[AnyMessage], add_messages]
    answer: Optional[str]
    session_id: Optional[str]
    new_message: Optional[AnyMessage]
