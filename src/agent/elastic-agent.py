from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from agent.tools import elastic_tools as t


load_dotenv()


model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

graph = create_react_agent(
    model=model,
    tools=[t.query_elastic_tool, t.human_assistance],
    prompt="You are an assistant working for a BioPharma company. The user will ask you questions about specific "
           "biomedical terms. Try to help. Reach out to Elasticsearch if necessary. Always verify user input with "
           "human assistance first and only after that use Elasticsearch. Query Elastic with exact query provided by "
           "user in human assistance step.",
    name="ElasticAgent",
)


