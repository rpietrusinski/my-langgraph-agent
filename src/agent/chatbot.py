from dotenv import load_dotenv
from typing import Annotated
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage
from langchain_tavily import TavilySearch
from langgraph.prebuilt.tool_node import ToolNode, tools_condition


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
llm_with_tools = llm.bind_tools([tool])


# build graph
tool_node = ToolNode(tools=[tool])
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()
