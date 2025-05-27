from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.agent.data.model import Base, User


def main():

    engine = create_engine('sqlite:///example.db')
    Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    # Example of adding a record (optional)
    new_user = User(name="Hannah", age=26, city="New York")
    session.add(new_user)
    session.commit()

    session.close()

if __name__ == "__main__":
    main()
