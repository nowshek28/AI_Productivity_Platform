from app.schemas.todo import TodoCreate


def test_create_generates_uuid(service):
    """
    Test the creation of a new todo item.
    """
    todo = TodoCreate(
        title="Learn FastAPI",
        description="Service test"
    )

    created = service.create(todo)

    assert created.id is not None

def test_create_sets_completed_false(service):
    """
    Test that a new todo item is created with completed set to False.
    """
    todo = TodoCreate(
        title="Learn FastAPI",
        description="Service test"
    )

    created = service.create(todo)

    assert created.completed is False

def test_create_generates_timestamps(service):
    """
    Test that a new todo item is created with created_at and updated_at timestamps.
    """
    todo = TodoCreate(
        title="Learn FastAPI",
        description="Service test"
    )

    created = service.create(todo)

    assert created.created_at is not None
    assert created.updated_at is not None

