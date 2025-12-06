import React, { useEffect, useState } from "react";
import "../../assets/styles/chatbot.css";
import { SlOptions } from "react-icons/sl";
import axios from "axios";
import { clearMessages, setMessage, setLoading } from "./chatslice";
import { useDispatch } from "react-redux";

const Sidebar = () => {
  const [previousChats, setPreviousChats] = useState([]);
  const [openOptionsId, setOpenOptionsId] = useState(null);

  const dispatch = useDispatch();
  useEffect(() => {
    axios.get("http://localhost:8000/chat/sessions").then((response) => {
      const sessionIds = response.data.session_ids;
      const chats = sessionIds.map((id) => ({
        id: id,
        title: `Conversation ${id}`,
      }));
      setPreviousChats(chats);
    });
  }, []);
  const onNewChat = () => {
    dispatch(clearMessages());
  };

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
              {chat.title || `Conversation ${index + 1}`}
              <span
                className="chat-options"
                onClick={(e) => handleOptions(e, chat.id)}
              >
                <SlOptions className="chat-options-icon" />
                {openOptionsId === chat.id && (
                  <div className="chatSession-options">
                    <div onClick={()=>handleDelete(chat.id)}>Delete</div>
                    <div>Rename</div>
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
