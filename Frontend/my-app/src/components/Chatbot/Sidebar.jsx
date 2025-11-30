import React, { useState } from "react";
import "../../assets/styles/chatbot.css";
import { SlOptions } from "react-icons/sl";

const Sidebar = () => {
  const dummyChats = [
    {
      id: 1,
      title: "Weather Chat",
      lastMessage: "It's sunny in Bangalore.",
      timestamp: "10:15 AM",
    },
    {
      id: 2,
      title: "Capital of India",
      lastMessage: "The capital of India is New Delhi.",
      timestamp: "10:20 AM",
    },
    {
      id: 3,
      title: "Joke",
      lastMessage: "Why did the chicken cross the road?",
      timestamp: "10:25 AM",
    },
  ];
  const [previousChats, setPreviousChats] = useState(dummyChats);
  const onNewChat = () => {
    // Logic to start a new chat
    console.log("New chat started");
  };
  return (
    <div className="sidebar">
      <div className="sidebar-content">
        <button className="new-chat-button" onClick={onNewChat}>
          New chat
        </button>
        <ul className="chat-list">
          {previousChats.map((chat, index) => (
            <div className="chat-item" key={chat.id || index}>
              {chat.title || `Conversation ${index + 1}`}
              <SlOptions className="chat-options-icon" />
            </div>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Sidebar;
