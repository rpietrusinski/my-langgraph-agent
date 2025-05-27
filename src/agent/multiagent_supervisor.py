from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from agent.tools import tools as t


load_dotenv()

flight_assistant = create_react_agent(
    model="openai:gpt-4o-mini",
    tools=[t.book_flight],
    prompt="You are a flight booking assistant",
    name="flight_assistant"
)

hotel_assistant = create_react_agent(
    model="openai:gpt-4o-mini",
    tools=[t.book_hotel],
    prompt="You are a hotel booking assistant",
    name="hotel_assistant"
)

graph = create_supervisor(
    agents=[flight_assistant, hotel_assistant],
    model=ChatOpenAI(model="gpt-4o-mini"),
    prompt=(
        "You manage a hotel booking assistant and a"
        "flight booking assistant. Assign work to them."
    )
).compile()



# result = graph.invoke({"messages": {"role": "user", "content": "book a flight from warsaw to lax. then book a hotel in la"}})
#
# for msg in result["messages"]:
#     msg.pretty_print()
