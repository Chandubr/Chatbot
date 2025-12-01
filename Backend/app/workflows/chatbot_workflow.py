from app.core.logging import logger
from langchain_openai import ChatOpenAI
import asyncio
import os
from app.core.config import envconfig
from langchain_core.messages import HumanMessage
from app.graph.chat_graph_builder import chatbot_graph

async def bot_reply(user_message: str, session_id: str) -> str:
    """
    Process user message and return bot response.
    """
    try:
        user_message_obj = HumanMessage(content=user_message)
        config = {
            "configurable": {
                "thread_id": session_id
            }
        }
        initial_state = {"new_message": user_message_obj, "thread_id": session_id}
        final_state = await chatbot_graph.ainvoke(initial_state, config=config)
        return final_state["answer"]
    except Exception as e:
        logger.error(f"Error in bot_reply: {e}")
        return "Sorry, there was an error processing your request."