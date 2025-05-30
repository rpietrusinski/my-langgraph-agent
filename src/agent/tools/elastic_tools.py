from langchain_core.tools import tool
from langgraph.types import interrupt
import agent.elastic.functions as f


@tool("query_elastic_tool")
def query_elastic_tool(search_term: str, size: int):
    """Runs elasticsearch request in order to obtain information about given <search_term>. Will return <size>
    number of results.

    """
    return f.elasticsearch_request(search_term, size)


@tool("human_assistance_tool")
def human_assistance(search_term: str, size: int):
    """Request assistance from a human. Modify Elasticsearch search term if necessary"""

    response = interrupt({
        "search_term": search_term,
        "size": size,
    })

    if response == "" :
        pass
    else:
        search_term = response

    return {"search_term": search_term, "size": size}
