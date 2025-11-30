import React from 'react'
import '../../assets/styles/chatbot.css'
import { RiRobot3Fill } from "react-icons/ri";
import { FaUser } from "react-icons/fa";

const MessageItem = ({ message }) => {
    const { text, sender, timestamp } = message;
    return (
        <div className={`message-item ${sender === 'ai' ? 'ai-message' : 'user-message'}`}>
            <div className="message-header">
                <span className="sender-label">{sender === 'ai' ? <RiRobot3Fill /> : <FaUser />}</span>
            </div>
            <div className="message-content">
                {text.trim()}
            </div>
            {timestamp && <span className="timestamp">{timestamp}</span>}
        </div>
    );
}

export default MessageItem