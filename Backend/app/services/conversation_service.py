from datetime import datetime
from typing import List
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from app.core.logging import logger
from app.db.database import get_conversation_collection


async def get_history_messages(session_id: str) -> List[BaseMessage]:
    """Fetch chat history for a session and convert it into LangChain messages."""
    collection = get_conversation_collection()
    cursor = collection.find({"session_id": session_id}).sort("created_at", 1)
    documents = await cursor.to_list(length=None)

    history: List[BaseMessage] = []
    for document in documents:
        role = document.get("role")
        content = document.get("content", "")
        created_at = document.get("created_at")
        if role == "user":
            msg = HumanMessage(content=content)
        elif role == "assistant":
            msg = AIMessage(content=content)
        else:
            continue 
        msg.created_at = created_at
        history.append(msg)

    logger.debug(f"Loaded {len(history)} messages from MongoDB for session_id={session_id}")
    return history


async def save_conversation_turn(session_id: str, user_message: HumanMessage, bot_response: str) -> None:
    """Persist the latest user/bot messages for a session."""
    now = datetime.utcnow()
    collection = get_conversation_collection()
    await collection.insert_many(
        [
            {
                "session_id": session_id,
                "role": "user",
                "content": user_message.content,
                "created_at": now,
            },
            {
                "session_id": session_id,
                "role": "assistant",
                "content": bot_response,
                "created_at": now,
            },
        ]
    )
    logger.debug(f"Stored conversation turn in MongoDB for session_id={session_id}")


async def get_all_session_ids() -> List[str]:
    """Return all unique session IDs that have stored messages."""
    collection = get_conversation_collection()
    pipeline = [
        {"$group": {
            "_id": "$session_id",
            "latest_time": {"$max": "$created_at"}
        }},
        {"$sort": {"latest_time": -1}}
    ]
    session_ids = await collection.aggregate(pipeline).to_list(length=None)
    session_ids = [doc["_id"] for doc in session_ids]
    logger.debug(f"Found {len(session_ids)} unique session_ids in MongoDB")
    return session_ids


async def delete_conversation_by_session_id(session_id: str) -> int:
    """
    Delete all messages for a given session_id.
    Returns the number of deleted documents.
    """
    collection = get_conversation_collection()
    result = await collection.delete_many({"session_id": session_id})
    logger.info(f"Deleted {result.deleted_count} messages for session_id={session_id}")
    return result.deleted_count

