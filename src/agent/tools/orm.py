from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from langchain_core.tools import tool

from src.agent.data.model import User


def get_db():
    engine = create_engine('sqlite:///example.db')
    session = sessionmaker(bind=engine)()
    return session


SESSION = get_db()


@tool("get_user_by_name_tool")
def get_user_by_name(name: str):
    """Extracts user with given name from db"""

    specific_user = SESSION.query(User).filter_by(name=name).first()
    return convert_user_to_dict(specific_user)


@tool("get_user_by_age_tool")
def get_user_by_age(age: int):
    """Extracts user with given age from db"""

    specific_user = SESSION.query(User).filter_by(age=age).first()
    return convert_user_to_dict(specific_user)


@tool("get_n_users_tool")
def get_n_users(n):
    """Extracts top n users from db"""
    all_users = SESSION.query(User).limit(n).all()
    return [convert_user_to_dict(user) for user in all_users]


@tool("create_user_tool")
def create_user(
    name: str,
    age: Optional[int] = None,
    city: Optional[str] = None,
):
    """Puts user to db"""
    new_user = User(name=name, age=age, city=city)
    SESSION.add(new_user)
    SESSION.commit()


def convert_user_to_dict(user):
    """Convert User instance to a dictionary."""
    if user:
        return {
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "city": user.city
        }
    return None


# session.close()
