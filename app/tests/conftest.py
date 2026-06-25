import pytest
import tempfile

from app.storage.json_storage import JsonStorage
from app.repositories.todo_repository import TodoRepository
from app.services.todo_service import TodoService
from app.tests.fakes import FakeTodoRepository

from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def storage(tmp_path):
    """
    Creates a temporary JSON storage for each test.
    """

    """with tempfile.NamedTemporaryFile(suffix=".json") as temp_file:
        storage = JsonStorage(temp_file.name)
        yield storage"""
    
    file_path = tmp_path / "test_todos.json"
    storage = JsonStorage(str(file_path))
    yield storage

@pytest.fixture
def repository(storage):
    """
    Creates a TodoRepository instance using the temporary storage.
    """

    return TodoRepository(storage)

@pytest.fixture
def service(repository):
    """
    Creates a TodoService instance using the temporary repository.
    """
    repository = FakeTodoRepository()  # Use the fake repository for testing

    return TodoService(repository)

@pytest.fixture
def client():
    """
    Creates a TestClient instance for testing the FastAPI app.
    """
    return TestClient(app)