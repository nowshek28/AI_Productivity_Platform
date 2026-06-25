from datetime import datetime,timezone
from uuid import uuid4

from app.schemas.todo import TodoResponse

def test_create_todo(repository):

    todo = TodoResponse(
        id=uuid4(),
        title="Learn FastAPI",
        description="Testing repository",
        completed=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    created = repository.create(todo)

    assert created.id == todo.id
    assert created.title == "Learn FastAPI"
    assert created.description == "Testing repository"
    assert created.completed is False


def test_get_all_todos(repository):
    todo1 = TodoResponse(
        id=uuid4(),
        title="Learn FastAPI",
        description="Testing repository",
        completed=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    todo2 = TodoResponse(
        id=uuid4(),
        title="Learn Pytest",
        description="Testing repository",
        completed=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    repository.create(todo1)
    repository.create(todo2)

    todos = repository.get_all()

    assert len(todos) == 2
    assert todos[0].id == todo1.id
    assert todos[1].id == todo2.id


def test_get_todo_by_id(repository):
    todo = TodoResponse(
        id=uuid4(),
        title="Find Todo by ID",
        description="Testing repository",
        completed=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    repository.create(todo)

    fetched_todo = repository.get_by_id(todo.id)

    assert fetched_todo is not None
    assert fetched_todo.id == todo.id
    assert fetched_todo.title == "Find Todo by ID"

def test_update_todo(repository):
    todo = TodoResponse(
        id=uuid4(),
        title="Update Todo",
        description="Testing repository",
        completed=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    repository.create(todo)

    updated_todo = TodoResponse(
        id=todo.id,
        title="Updated Todo",
        description="Updated description",
        completed=True,
        created_at=todo.created_at,
        updated_at=datetime.now(timezone.utc),
    )

    result = repository.update(todo.id, updated_todo)

    assert result is not None
    assert result.title == "Updated Todo"
    assert result.description == "Updated description"
    assert result.completed is True


def test_delete_todo(repository):
    todo = TodoResponse(
        id=uuid4(),
        title="Delete Todo",
        description="Testing repository",
        completed=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    repository.create(todo)

    deleted = repository.delete(todo.id)

    assert deleted is True
    assert repository.get_by_id(todo.id) is None

    