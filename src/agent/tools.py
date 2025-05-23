import requests
from langsmith import traceable
from pydantic import BaseModel, Field
from langchain_core.tools import tool


class Person(BaseModel):
    """A person model."""
    name: str = Field(..., min_length=2)
    age: int = Field(..., gt=0)
    city: str


class StructuredResponse(BaseModel):
    text: str


@tool("create_person_tool")
@traceable
def create_person(name: str, age: int, city: str):
    """Create an instance of Person class for the purpose of database load."""
    _person = Person(name=name, age=age, city=city)
    return repr(_person)


@tool("get_weather_tool")
@traceable
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@tool("get_joke_tool")
@traceable
def get_joke() -> str:
    """Get a random joke from the joke API."""
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        joke_data = response.json()
        return f"{joke_data['setup']} - {joke_data['punchline']}"
    else:
        return "Failed to retrieve joke"
