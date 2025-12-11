from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool

@tool
def duckduckgo_search(query: str, max_results: int = 5) -> list:
    """
    Perform a DuckDuckGo search and return the top results.

    Args:
        query (str): The search query.
        max_results (int): The maximum number of results to return.

    Returns:
        list: A list of search result snippets.
    """
    search_tool = DuckDuckGoSearchRun()
    results = search_tool.run(query)
    result_list = results.split('\n')[:max_results]
    
    return result_list