import React, { useEffect, useRef, useState } from "react";
import "../../assets/styles/chatbot.css";
import { BsSend } from "react-icons/bs";
import { useDispatch, useSelector } from "react-redux";
import { setMessage } from "./chatslice";

const MessageInput = () => {
  const dispatch = useDispatch();
  const now = new Date();
  const [inputValue, setInputValue] = useState("");
  const messages = useSelector((state) => state.chat.messages);
  const timeString = now.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  const sendMessage = () => {
    const newMessages = [
      ...messages,
      {
        text: inputValue,
        sender: "user",
        timestamp: timeString,
      },
    ];
    dispatch(setMessage(newMessages));
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
