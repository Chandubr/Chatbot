from app.core.logging import logger
from langchain_core.messages import HumanMessage
from app.graph.chat_graph_builder import chatbot_graph
from app.services.conversation_service import (
    get_history_messages,
    save_conversation_turn,
)


async def bot_reply(user_message: str, session_id: str) -> str:
    """
    Process user message and return bot response.
    """
    try:
        try:
            history_messages = await get_history_messages(session_id)
        except Exception as db_error:
            logger.error(f"Failed to load history from MongoDB: {db_error}")
            history_messages = []

        user_message_obj = HumanMessage(content=user_message)
        initial_state = {
            "messages": history_messages,
            "new_message": user_message_obj,
            "session_id": session_id,
        }
        final_state = await chatbot_graph.ainvoke(initial_state)
        answer = final_state["answer"]

        try:
            await save_conversation_turn(session_id, user_message_obj, answer)
        except Exception as db_error:
            logger.error(f"Failed to store conversation turn in MongoDB: {db_error}")

        return answer
    except Exception as e:
        logger.error(f"Error in bot_reply: {e}")
        return "Sorry, there was an error processing your request."
