


from typing import Optional
from app.services.chatBot_service import get_bot_response
from app.graph.chat_workflow_states import ChatState
from app.core.logging import logger


def add_user_message(state: ChatState) -> ChatState:
    updated_state = dict(state)
    if "new_message" in updated_state and updated_state["new_message"] is not None:
        logger.info(f"Adding user message: {updated_state['new_message']}")
        updated_state.setdefault("messages", []).append(updated_state["new_message"])
        updated_state["new_message"] = None
    logger.debug(f"State after add_user_message: {updated_state}")
    return updated_state

async def generate_answer(state: ChatState) -> ChatState:
    user_messages = state["messages"]
    logger.info(f"Generating answer for messages: {user_messages}")
    answer = await get_bot_response(user_messages)
    updated_state = dict(state)
    updated_state["answer"] = answer
    logger.info(f"Generated answer: {answer}")
    logger.debug(f"State after generate_answer: {updated_state}")
    return updated_state
