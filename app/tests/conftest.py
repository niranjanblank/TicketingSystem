import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import create_engine, Session, SQLModel
from app.database import get_session
import os
from dotenv import load_dotenv
from ..models.user import User
from ..models.board import Board

load_dotenv()

TEST_DB_URL = os.getenv('TEST_DB_URL')


@pytest.fixture(scope="session")
def test_db_engine():
    engine = create_engine(TEST_DB_URL)
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    connection = test_db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session  # use this session

    session.close()
    transaction.rollback()  # Ensure a clean state for the next test
    connection.close()


@pytest.fixture(scope="function")
def client(test_db_session):
    # Dependency override for the database session
    app.dependency_overrides[get_session] = lambda: test_db_session
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def user_data(test_db_session):
    # Insert test user data here
    new_user = User(username="testuser", email="test@example.com", password="hashedpassword")
    test_db_session.add(new_user)
    test_db_session.commit()
    test_db_session.refresh(new_user)
    return new_user  # return the user object or just the user ID as needed


@pytest.fixture(scope="function")
def board_data(test_db_session: Session, user_data: User):
    # Create a test board with owner_id from user_data

    test_board = Board(title="Test Board", description="This is a test board", owner_id=user_data.id)
    test_db_session.add(test_board)
    test_db_session.commit()
    test_db_session.refresh(test_board)  # Refresh to load any additional attributes
    return test_board


# Fixture to create users in the database
@pytest.fixture(scope="function")
def create_test_users(test_db_session: Session, ):
    users = [
        User(username=f"user{i}", email=f"user{i}@example.com", password="testpassword")
        for i in range(10)  # Adjust the range for desired number of test users
    ]
    test_db_session.add_all(users)
    test_db_session.commit()
    return users


# Fixture to create boards in the database
@pytest.fixture(scope="function")
def create_test_boards(test_db_session, create_test_users):
    boards = [
        Board(title=f"Board {i}", description=f"Description {i}",
              owner_id=create_test_users[i % len(create_test_users)].id)
        for i in range(20)  # Creating 20 test boards
    ]
    test_db_session.add_all(boards)
    test_db_session.commit()
    return boards
