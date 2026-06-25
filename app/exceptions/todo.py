from uuid import UUID


class TodoNotFoundError(Exception):
    """
    Raised when a Todo cannot be found.
    """

    def __init__(self, todo_id: UUID):
        self.todo_id = todo_id
        super().__init__(f"Todo with id '{todo_id}' was not found.")