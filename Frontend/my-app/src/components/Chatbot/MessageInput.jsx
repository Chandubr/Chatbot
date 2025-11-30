import React, { useState } from "react";
import "../../assets/styles/chatbot.css";
import { BsSend } from "react-icons/bs";


const MessageInput = ({onSend}) => {
  const [inputValue, setInputValue] = useState("");
  const sendMessage = () => {
    onSend(inputValue);
    setInputValue("");
  };
  return (
    <div className="messageInput">
      <input
        className="input-message"
        type="text"
        placeholder="Type your message..."
        value={inputValue}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            sendMessage();
          }
        }}
        onChange={(e) => setInputValue(e.target.value)}
      />
      <div className="send-button" onClick={() => sendMessage()}>
        <BsSend />
      </div>
    </div>
  );
};

export default MessageInput;
