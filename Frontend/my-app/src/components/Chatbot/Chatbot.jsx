import React from "react";
import "../../assets/styles/chatbot.css";
import Sidebar from "./Sidebar";
import ChatWindow from "./ChatWindow";

const Chatbot = () => {
  return (
    <div className="chatbot-container">
      <div className="sidebar-container">
        <Sidebar />
      </div>
      <div className="main-content">
        <ChatWindow />
      </div>
    </div>
  );
};

export default Chatbot;
