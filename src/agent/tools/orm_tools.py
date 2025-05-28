from typing import Optional

from langchain_core.tools import tool

from agent.data.model import User
import agent.data.functions as f



@tool("get_user_by_name_tool")
def get_user_by_name_tool(name: str):
    """Extracts user with given name from db"""
    return f.get_user_by_name(name)


@tool("get_user_by_age_tool")
def get_user_by_age_tool(age: int):
    """Extracts user with given age from db"""
    return f.get_user_by_age(age)


@tool("get_n_users_tool")
def get_top_n_users_tool(n):
    """Extracts top n users from db"""
    return f.get_top_n_users(n)


@tool("create_user_tool")
def create_user_tool(
    name: str,
    age: Optional[int] = None,
    city: Optional[str] = None,
):
    """Puts user to db"""
    f.create_user(name, age, city)
