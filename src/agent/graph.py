from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from agent import tools as t
from langchain_community.tools.tavily_search import TavilySearchResults


load_dotenv()


search = TavilySearchResults(max_results=1)

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

graph = create_react_agent(
    model=model,
    tools=[t.get_weather, t.get_joke, t.create_person, search],
    prompt="Behave like a nasty pirate.",
    name="MyAgent",
    response_format=t.StructuredResponse,
)


# result = graph.invoke({"messages": {"role": "user", "content": "Hello, tell me some joke"}})
#
# for msg in result["messages"]:
#     msg.pretty_print()
#
# result["structured_response"]