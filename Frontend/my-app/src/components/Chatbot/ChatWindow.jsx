import React, { use, useEffect, useState } from "react";
import MessageInput from './MessageInput'
import MessageList from './MessageList'
import { useDispatch } from "react-redux";
import { setMessage } from "./chatslice";

const ChatWindow = () => {

  const dispatch = useDispatch();
  
    dispatch(setMessage([
    {
      text: "Hello! How can I assist you today?",
      sender: "ai",
      timestamp: "10:00 AM",
    },
    {
      text: "Hi! I have a question about your services.",
      sender: "user",
      timestamp: "10:01 AM",
    },
    {
      text: "Sure! What would you like to know?",
      sender: "ai",
      timestamp: "10:02 AM",
    },
    {
      text: "Can you tell me more about your pricing?",
      sender: "user",
      timestamp: "10:03 AM",
    },
    {
      text: "Our pricing is based on the features you need. We offer several plans to suit different requirements.",
      sender: "ai",
      timestamp: "10:04 AM",
    },
    {
      text: "That sounds great! Thank you for the information.",
      sender: "user",
      timestamp: "10:05 AM",
    },
    {
      text: "You're welcome! If you have any more questions, feel free to ask.",
      sender: "ai",
      timestamp: "10:06 AM",
    },
  ]));

  return (
    <>
      <div className="messages-container">
        <MessageList/>
      </div>
      <div className="messageInput-container">
        <MessageInput />
      </div>
    </>
  );
};

export default ChatWindow;
