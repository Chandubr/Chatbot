from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
)
from langchain_core.messages import SystemMessage
from datetime import datetime

def get_generate_answer_prompt(system_prompt=None) -> ChatPromptTemplate:
    """
    Returns a ChatPromptTemplate for generating answers based on user questions.

    Args:
        system_prompt (str): The system prompt for the assistant.

    Returns:
        ChatPromptTemplate: The constructed prompt template.
    """
    current_date = datetime.now().strftime("%B %d, %Y")
    if system_prompt is None:
        system_prompt = (
            f"Today's date is {current_date}. "
            "You are a knowledgeable and trustworthy AI assistant. "
            "You can use tools when needed:\n"
            "Your goal is to provide accurate, clear, and concise responses to the user’s questions. "
            "When answering:\n"
            "- If the answer requires up-to-date or external information, call `duckduckgo_search` with a concise query.\n"
            "- If you can answer from the provided conversation history, respond directly.\n"
            "- Use plain language and keep your tone professional yet friendly.\n"
            "- Be brief but informative — prefer quality over quantity.\n"
            "- If you are unsure or the information is unavailable, say 'I’m not sure about that' rather than guessing.\n"
            "- Never include fabricated facts or references.\n"
            "- When appropriate, organize information in bullet points or short paragraphs for readability.\n"
            "- Always remain neutral and respectful."
        )
    """
    Returns a ChatPromptTemplate for generating answers based on user questions.

    Args:
        system_prompt (str): The system prompt for the assistant.

    Returns:
        ChatPromptTemplate: The constructed prompt template.
    """
    return ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{question}"),
    ])