
from app.graph.chat_workflow_states import ChatState
from app.graph.chat_workflow_nodes import add_user_message, generate_answer
from langgraph.graph import StateGraph, START, END

graph = StateGraph(ChatState)
graph.add_node("add_user_message", add_user_message)
graph.add_node("generate_answer", generate_answer)

graph.add_edge(START, "add_user_message")
graph.add_edge("add_user_message", "generate_answer")
graph.add_edge("generate_answer", END)

chatbot_graph = graph.compile()
