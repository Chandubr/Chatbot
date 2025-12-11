from datetime import datetime
from typing import List
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from app.core.logging import logger


async def get_history_messages(collection, session_id: str) -> List[BaseMessage]:
    """Fetch chat history for a session and convert it into LangChain messages."""
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
    return history

async def save_conversation_turn(
    collection, session_id: str, user_message: HumanMessage, bot_response: str
) -> None:
    """Persist the latest user/bot messages for a session, including title if present."""
    now = datetime.utcnow()
    latest_doc = await collection.find_one(
        {"session_id": session_id, "title": {"$exists": True}},
        sort=[("created_at", -1)]
    )
    title = latest_doc["title"] if latest_doc and "title" in latest_doc else None

    user_doc = {
        "session_id": session_id,
        "role": "user",
        "content": user_message.content,
        "created_at": now,
    }
    assistant_doc = {
        "session_id": session_id,
        "role": "assistant",
        "content": bot_response,
        "created_at": now,
    }
    if title:
        user_doc["title"] = title
        assistant_doc["title"] = title

    await collection.insert_many([user_doc, assistant_doc])


async def get_all_session_ids(collection) -> List[dict]:
    """Return all unique session IDs and their latest title."""
    pipeline = [
        {"$sort": {"created_at": -1}},  
        {"$group": {
            "_id": "$session_id",
            "latest_time": {"$max": "$created_at"},
            "title": {"$first": "$title"}
        }},
        {"$sort": {"latest_time": -1}}
    ]
    session_docs = await collection.aggregate(pipeline).to_list(length=None)
    sessions = [{"id": doc["_id"], "title": doc.get("title", f"Conversation {doc['_id']}")} for doc in session_docs]
    return sessions

async def delete_conversation_by_session_id(collection, session_id: str) -> int:
    """
    Delete all messages for a given session_id.
    Returns the number of deleted documents.
    """
    result = await collection.delete_many({"session_id": session_id})
    logger.info(f"Deleted {result.deleted_count} messages for session_id={session_id}")
    return result.deleted_count


async def rename_conversation_name(collection, session_id: str, new_name: str) -> None:
    """
    Rename the conversation by updating the 'title' field
    for all messages with the given session_id.
    """
    await collection.update_many(
        {"session_id": session_id}, {"$set": {"title": new_name}}
    )
    logger.info(f"Renamed conversation {session_id} to '{new_name}'")
