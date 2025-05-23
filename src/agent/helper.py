from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, AnyMessage
from langchain_openai import ChatOpenAI
from agent import tools as t
from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel


load_dotenv()
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)
checkpointer = InMemorySaver()

# dynamic prompt
def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
    user_name = config["configurable"].get("user_name")
    system_msg = f"You are a helpful assistant. Address the user as {user_name}."
    return [{"role": "system", "content": system_msg}] + state["messages"]


class Response(BaseModel):
    text: str

# define agent
graph = create_react_agent(
    model=model,
    tools=[t.get_weather, t.get_joke, t.create_person],
    prompt=prompt,
    name="MyAgent",
    checkpointer=checkpointer,
    response_format=Response
)

# Run the agent
config = {"configurable": {"user_name": "John Smith", "thread_id": "1"}}
messages1 = [HumanMessage("Hello! I'm in bad mood. Tell me a joke!")]
messages2 = [HumanMessage("Give me one more")]

messages3 = [HumanMessage("Hello! What's the weather in Warsaw?")]
messages4 = [HumanMessage("And how about Krakow?")]


result1 = graph.invoke(
    input={"messages": messages3},
    config=config,
)

result2 = graph.invoke(
    input={"messages": messages4},
    config=config,
)


# print agent outputs
for msg in result2["messages"]:
    msg.pretty_print()
