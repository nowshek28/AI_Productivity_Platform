import pytest

from sqlalchemy import create_engine, delete as sql_delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.storage.json_storage import JsonStorage
from app.repositories.json_todo_repository import JsonTodoRepository
from app.services.todo_service import TodoService
from app.tests.fakes import FakeTodoRepository

from fastapi.testclient import TestClient
from app.main import app
from app.database.base import Base
from app.database.models import TodoModel
from app.core.dependencies import get_db


# ---------------------------------------------------------------------------
# Shared in-memory SQLite engine.
# StaticPool forces all connections to reuse the same in-memory database so
# that the tables created here are visible inside the TestClient requests.
# The production PostgreSQL database is never touched by any test.
# ---------------------------------------------------------------------------
_test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
Base.metadata.create_all(bind=_test_engine)
_TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)


@pytest.fixture
def storage(tmp_path):
    """Creates a temporary JSON storage for each test."""
    file_path = tmp_path / "test_todos.json"
    storage = JsonStorage(str(file_path))
    yield storage


@pytest.fixture
def repository(storage):
    """Creates a JsonTodoRepository instance using the temporary storage."""
    return JsonTodoRepository(storage)


@pytest.fixture
def service():
    """Creates a TodoService backed by an in-memory FakeTodoRepository."""
    return TodoService(FakeTodoRepository())


@pytest.fixture
def client():
    """
    TestClient wired to an in-memory SQLite database.

    - The production PostgreSQL database is never read or written.
    - Each test starts with a clean table (all rows are deleted on teardown).
    - The SQLite schema is built from the same SQLAlchemy models as production,
      so the structure is identical.
    """
    session = _TestingSessionLocal()

    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    # Do NOT use 'with TestClient(app)' here — the context manager triggers
    # FastAPI's on_startup event, which calls Base.metadata.create_all(engine)
    # against the real PostgreSQL database. Yielding TestClient directly skips
    # startup/shutdown lifecycle events entirely, keeping tests fully offline.
    yield TestClient(app)

    # Teardown: clear all rows so the next test starts with an empty database.
    # This only affects the in-memory SQLite database, not PostgreSQL.
    session.rollback()
    session.execute(sql_delete(TodoModel))
    session.commit()
    session.close()
    app.dependency_overrides.clear()
