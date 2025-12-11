import React, { useEffect, useRef } from "react";
import MessageInput from "./MessageInput";
import MessageList from "./MessageList";
import { useDispatch, useSelector } from "react-redux";
import { setLoading, setMessage } from "./chatslice";
import { connectWebSocket } from "../../api/websocket";
import { PulseLoader } from "react-spinners";



const ChatWindow = () => {
  const dispatch = useDispatch();
  const loading = useSelector((state) => state.chat.loading);
  const ws = useRef(null);
  const sessionId = useSelector((state) => state.chat.sessionId);

  const WS_URL = `ws://localhost:8000/ws/chat?session_id=${sessionId}`;
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
      dispatch(setLoading(false));
    });
    return () => ws.current && ws.current.close();
  }, [dispatch, WS_URL, sessionId]);

  const sendMessage = (msg) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(msg);
      dispatch(
        setMessage({
          text: msg,
          sender: "user",
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        })
      );
    }
    dispatch(setLoading(true));
  }
  return (
    <>
      <div className="messages-container">
        <MessageList />
        {loading && <div className="loader"><PulseLoader color="#7abbf1ff" /></div>}
      </div>
      <div className="messageInput-container">
        <MessageInput onSend={sendMessage} />
      </div>
    </>
  );
};

export default ChatWindow;
