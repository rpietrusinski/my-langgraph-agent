import os
from dotenv import load_dotenv
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from agent.data.model import User


load_dotenv()
DB = os.environ.get("SQLITE_DB")


def get_db():
    engine = create_engine(f"sqlite:///{DB}")
    session = sessionmaker(bind=engine)()
    return session


SESSION = get_db()


def get_user_by_name(name: str, session=SESSION):
    """Extracts user with given name from db"""

    specific_user = session.query(User).filter_by(name=name).first()
    return convert_user_to_dict(specific_user)


def get_user_by_age(age: int, session=SESSION):
    """Extracts user with given age from db"""

    specific_user = session.query(User).filter_by(age=age).first()
    return convert_user_to_dict(specific_user)


def get_top_n_users(n, session=SESSION):
    """Extracts top n users from db"""
    all_users = session.query(User).limit(n).all()
    return [convert_user_to_dict(user) for user in all_users]


def create_user(
    name: str,
    age: Optional[int] = None,
    city: Optional[str] = None,
    session = SESSION,
):
    """Puts user to db"""
    new_user = User(name=name, age=age, city=city)
    session.add(new_user)
    session.commit()


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
