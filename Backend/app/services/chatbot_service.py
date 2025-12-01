from langchain_openai import ChatOpenAI
from app.core.logging import logger
import asyncio
import os
from app.core.config import envconfig
from app.services.prompt_templates import get_generate_answer_prompt

os.environ["OPENAI_API_KEY"] = envconfig.openai_api_key
os.environ["LANGSMITH_API_KEY"] = envconfig.langsmith_api_key
os.environ["LANGSMITH_TRACING"] = str(envconfig.langsmith_tracing).lower()

llm = ChatOpenAI(model=envconfig.generation_model_openai, temperature=0)

async def get_bot_response(user_message: list,timeout_sec=15) -> str:
	try:
		user_question=user_message[-1].content
		messages = get_generate_answer_prompt().format_messages(question=user_question,history=user_message[:-1])
		response = await asyncio.wait_for(llm.ainvoke(messages), timeout=timeout_sec)
		logger.info(f"User message: {user_message}")
		logger.info(f"Bot response: {response.content}")
		return response.content
	except asyncio.TimeoutError as e:
		logger.error(f"Timeout getting bot response: {e}")
		return "Bot is taking too long to respond. Please try again later."
	except Exception as e:
		logger.error(f"Error getting bot response: {e}")
		return "Sorry, there was an error processing your request."
