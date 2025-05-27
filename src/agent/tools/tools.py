import requests
from langsmith import traceable
from pydantic import BaseModel
from langchain_core.tools import tool


class StructuredResponse(BaseModel):
    text: str


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


@tool("book_hotel_tool")
def book_hotel(hotel_name: str):
    """Book a hotel"""
    return f"Successfully booked a stay at {hotel_name}."


@tool("book_flight_tool")
def book_flight(from_airport: str, to_airport: str):
    """Book a flight"""
    return f"Successfully booked a flight from {from_airport} to {to_airport}."
