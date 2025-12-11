import React, { useEffect, useRef, useState } from "react";
import "../../assets/styles/chatbot.css";
import { SlOptions } from "react-icons/sl";
import axios from "axios";
import { clearMessages, setMessage, setLoading, setSessionId } from "./chatslice";
import { useDispatch } from "react-redux";

const Sidebar = () => {
  const [previousChats, setPreviousChats] = useState([]);
  const [openOptionsId, setOpenOptionsId] = useState(null);
  const [editingChatId, setEditingChatId] = useState(null);
  const [editedTitle, setEditedTitle] = useState("");
  const renameInputRef = useRef(null);

  const dispatch = useDispatch();
  useEffect(() => {
    axios.get("http://localhost:8000/chat/sessions").then((response) => {
      const fetchedChats = response.data.session_ids
      console.log(fetchedChats)
      const chats = fetchedChats.map((item) => ({
        id: item.id,
        title: item.title || `Conversation ${item.id}`,
      }));
      setPreviousChats(chats);
    });
  }, []);
  const onNewChat = () => {
    dispatch(clearMessages());
  };

  useEffect(() => {
    if (editingChatId !== null && renameInputRef.current) {
      renameInputRef.current.focus();
      renameInputRef.current.select();
    }
  }, [editingChatId]);

  const handleOptions = (e, chatId) => {
    e.stopPropagation();
    setOpenOptionsId(openOptionsId === chatId ? null : chatId);
  };

  const getConversation = (sessionId) => {
    dispatch(clearMessages());
    dispatch(setLoading(true));
    axios
      .get(`http://localhost:8000/chat/sessions/${sessionId}`)
      .then((response) => {
        dispatch(setLoading(false));
        dispatch(setSessionId(sessionId));
        const conversation = response.data.conversation;
        conversation.forEach((msg) => {
          dispatch(
            setMessage({
              text: msg.content,
              sender: msg.type === "human" ? "user" : "ai",
              timestamp: msg.created_at
                ? new Date(msg.created_at).toLocaleString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })
                : "",
            })
          );
        });
      });
  };

  const handleDelete = (sessionId) => {
    axios.delete(`http://localhost:8000/chat/delete-sessions/${sessionId}`)
      .then(() => {
        setPreviousChats(previousChats.filter(chat => chat.id !== sessionId));
        dispatch(clearMessages());
      });
  }

  const handleRename = (sessionId, currentTitle) => {
    setEditingChatId(sessionId);
    setEditedTitle(currentTitle || "");
    setOpenOptionsId(null);
  };

  const commitRename = (sessionId, newTitle) => {
    const trimmed = (newTitle || "").trim();
    if (!trimmed) return setEditingChatId(null);

    setPreviousChats((prev) =>
      prev.map((chat) => (chat.id === sessionId ? { ...chat, title: trimmed } : chat))
    );
    setEditingChatId(null);

    axios.put(`http://localhost:8000/chat/rename-session/${sessionId}`, { new_name: trimmed })
      .then(() => console.log("Session renamed successfully"))
      .catch((error) => console.error("Error renaming session:", error));
  };

  const handleRenameKeyDown = (e, sessionId) => {
    if (e.key === "Enter") {
      commitRename(sessionId, editedTitle);
    }
    if (e.key === "Escape") {
      setEditingChatId(null);
    }
  };
  return (
    <div className="sidebar">
      <div className="sidebar-content">
        <button className="new-chat-button" onClick={() => onNewChat()}>
          New chat
        </button>
        <ul className="chat-list">
          {previousChats.map((chat, index) => (
            <div
              className="chat-item"
              key={chat.id || index}
              onClick={() => getConversation(chat.id)}
            >
              {editingChatId === chat.id ? (
                <input
                  ref={renameInputRef}
                  className="chat-rename-input"
                  value={editedTitle}
                  onChange={(e) => setEditedTitle(e.target.value)}
                  onBlur={() => commitRename(chat.id, editedTitle)}
                  onKeyDown={(e) => handleRenameKeyDown(e, chat.id)}
                />
              ) : (
                chat.title || `Conversation ${index + 1}`
              )}
              <span
                className="chat-options"
                onClick={(e) => handleOptions(e, chat.id)}
              >
                <SlOptions className="chat-options-icon" />
                {openOptionsId === chat.id && (
                  <div className="chatSession-options">
                    <div onClick={() => handleDelete(chat.id)}>Delete</div>
                    <div
                      onClick={() =>
                        handleRename(
                          chat.id,
                          chat.title || `Conversation ${index + 1}`
                        )
                      }
                    >
                      Rename
                    </div>
                  </div>
                )}
              </span>
            </div>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Sidebar;
