from typing import Annotated, Sequence, TypedDict
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import HumanMessage, SystemMessage,BaseMessage,AnyMessage
from langgraph.graph.message import add_messages
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    query_type: str
    query:str
    human_feedback: Annotated[list[str], add_messages]