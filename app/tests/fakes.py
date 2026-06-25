from app.schemas.todo import TodoResponse


class FakeTodoRepository:

    def __init__(self):
        self.todos = []

    def create(self, todo: TodoResponse):
        self.todos.append(todo)
        return todo

    def get_all(self):
        return self.todos

    def get_by_id(self, todo_id):
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def update(self, todo_id, updated_todo):
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                self.todos[i] = updated_todo
                return updated_todo
        return None

    def delete(self, todo_id):
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                del self.todos[i]
                return True
        return False