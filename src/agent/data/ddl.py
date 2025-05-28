import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from agent.data.model import Base, User


load_dotenv()
DB = os.environ.get("SQLITE_DB")


def main():

    engine = create_engine(f"sqlite:///{DB}")
    Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    new_user = User(name="Hannah", age=26, city="New York")
    session.add(new_user)
    session.commit()

    session.close()

if __name__ == "__main__":
    main()
