import { createSlice } from "@reduxjs/toolkit";

const chatSlice = createSlice({
  name: "chat",
  initialState: {
    messages: [],
    loading: false,
    sessionId: null,
  },
  reducers: {
    setMessage: (state, action) => {
      state.messages.push(action.payload);
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    clearMessages: (state) => {
      state.messages = [];
    },
    setSessionId: (state, action) => {
      state.sessionId = action.payload;
    },
  },
});

export const { setMessage, setLoading, clearMessages, setSessionId } = chatSlice.actions;
export default chatSlice.reducer;
