# Chatbot service using LangGraph and LangChain
# from langgraph.chains import Chain
from langchain_openai import OpenAI
import os
from app.core.config import envconfig

os.environ["OPENAI_API_KEY"] = envconfig.openai_api_key
os.environ["LANGSMITH_API_KEY"] = envconfig.langsmith_api_key


llm = OpenAI()

# Define a simple LangGraph pipeline (LLM response)
def get_bot_response(user_message: str) -> str:
	# You can build a more complex graph here
	# For now, just call the LLM with the user message
	response = llm.invoke(user_message)
	return response

# For testing, you can also return an echo:
# def get_bot_response(user_message: str) -> str:
#     return f"Echo: {user_message}"
