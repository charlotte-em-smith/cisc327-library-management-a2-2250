import pytest
import database

@pytest.fixture(scope="session", autouse=True)
def setup_databse():
    print("initializing database.")
    database.init_database()