from app.utils.duckduckgo_search import duckduckgo_search
from langchain_openai import ChatOpenAI
from app.core.logging import logger
import asyncio
import os
from app.core.config import envconfig
from app.services.prompt_templates import get_generate_answer_prompt
from langchain_core.messages import AIMessage, ToolMessage

os.environ["OPENAI_API_KEY"] = envconfig.openai_api_key
os.environ["LANGSMITH_API_KEY"] = envconfig.langsmith_api_key
os.environ["LANGSMITH_TRACING"] = str(envconfig.langsmith_tracing).lower()

llm = ChatOpenAI(model=envconfig.generation_model_openai, temperature=0)
llm_with_tools = llm.bind_tools([duckduckgo_search])

async def get_bot_response(user_message: list,timeout_sec=15) -> str:
	try:
		user_question=user_message[-1].content
		messages = get_generate_answer_prompt().format_messages(question=user_question,history=user_message[:-1])
		ai_msg: AIMessage = await asyncio.wait_for(llm_with_tools.ainvoke(messages), timeout=timeout_sec)
		if ai_msg.tool_calls:
			tool_results=[]
			for call in ai_msg.tool_calls:
				if call["name"]== "duckduckgo_search":
					args = call.get("args", {})
					result = duckduckgo_search.invoke(args)
					logger.info(f"DuckDuckGo search results for query '{args.get('query', '')}': {result}")
					if isinstance(result, list):
						result = "\n".join(result)
					tool_results.append(ToolMessage(
						content= result,
						name = call["name"],
						tool_call_id=call["id"]
					))
			followup_messages = messages + [ai_msg] + tool_results
			ai_msg = await asyncio.wait_for(llm.ainvoke(followup_messages), timeout=timeout_sec)		 

		return ai_msg.content
	except asyncio.TimeoutError as e:
		logger.error(f"Timeout getting bot response: {e}")
		return "Bot is taking too long to respond. Please try again later."
	except Exception as e:
		logger.error(f"Error getting bot response: {e}")
		return "Sorry, there was an error processing your request."
