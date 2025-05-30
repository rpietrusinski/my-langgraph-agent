from dotenv import load_dotenv
from typing import Annotated
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage
from langchain_tavily import TavilySearch
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from agent.tools import orm_tools as o



load_dotenv()


# define state class (can use MessagesState directly)
class State(MessagesState):
    messages: Annotated[list[AnyMessage], add_messages]


# define nodes
def chatbot(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# define model and tools
llm = init_chat_model("openai:gpt-4o-mini")
tool = TavilySearch(max_results=1)

tools_list = [
    tool,
    o.create_user_tool,
    o.get_user_by_name_tool,
    o.get_user_by_age_tool,
    o.get_top_n_users_tool,
]
llm_with_tools = llm.bind_tools(tools_list)



# build graph
tool_node = ToolNode(tools=tools_list)
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()
