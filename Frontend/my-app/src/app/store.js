import { configureStore } from "@reduxjs/toolkit";
import chatReducer from "../components/Chatbot/chatslice";

export const store = configureStore({
  reducer: {
    chat: chatReducer,
  },
});
