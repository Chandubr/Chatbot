import React, { useEffect, useRef } from "react";
import MessageItem from "./MessageItem";
import { useSelector } from "react-redux";

const MessageList = () => {
  const messages = useSelector((state) => state.chat.messages);
  const endRef = useRef(null);
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);
  return (
    <div className="message-list">
      {messages.map((msg, index) => (
        <MessageItem key={index} message={msg} />
      ))}
      <div ref={endRef} />
    </div>
  );
};

export default MessageList;
