import React, { useEffect, useRef} from "react";
import MessageInput from "./MessageInput";
import MessageList from "./MessageList";
import { useDispatch } from "react-redux";
import { setMessage } from "./chatslice";
import { connectWebSocket } from "../../api/websocket";

const WS_URL = "ws://localhost:8000/ws/chat";

const ChatWindow = () => {
  const dispatch = useDispatch();
  const ws = useRef(null);
  useEffect(() => {
    ws.current = connectWebSocket(WS_URL, (data) => {
      dispatch(
        setMessage({
          text: data,
          sender: "ai",
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        })
      );
    });
    return () => ws.current && ws.current.close();
  }, [dispatch]);

  const sendMessage = (msg) =>{
    if(ws.current && ws.current.readyState === WebSocket.OPEN){
      ws.current.send(msg);
      dispatch(
        setMessage({
          text: msg,
          sender: "user",
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        })
      );
    }
  }
  return (
    <>
      <div className="messages-container">
        <MessageList />
      </div>
      <div className="messageInput-container">
        <MessageInput onSend={sendMessage} />
      </div>
    </>
  );
};

export default ChatWindow;
