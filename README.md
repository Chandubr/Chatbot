# 💬 AI Chatbot – FastAPI + React + LangGraph

A full-stack, session-based AI chatbot with real-time messaging, LLM integration, and persistent conversation history.

Built with **FastAPI**, **React**, **MongoDB**, and **LangChain/LangGraph** for modular, production-friendly workflows.

> Talk to an AI assistant with web search, multi-turn memory, and session management – all in one app.

---

## ✨ Features

- ⚡ **Real-time chat** with WebSocket-based messaging
- 🧠 **LLM integration** using LangChain / LangGraph
- 💬 **Multi-turn conversation** with context-aware responses
- 💾 **Persistent sessions** stored in MongoDB
- 🗂️ **Session management & renaming** (chat history per session)
- 🌐 **DuckDuckGo web search tool** for up-to-date answers
- 🧱 **Modular backend workflow** using LangGraph nodes and tools
- 🖥️ **Modern React frontend** with Redux state management

---

## 🧰 Tech Stack

**Backend**

- FastAPI
- LangChain & LangGraph
- OpenAI / LLM provider (pluggable)
- Motor (MongoDB async client)
- Pydantic for models

**Frontend**

- React
- Redux (for global state & sessions)
- Axios (HTTP requests)
- WebSocket (real-time messaging)

**Database**

- MongoDB (session + message history)

---
