def test_health(client):
    """
    Test the health check endpoint.
    """
    response = client.get("api/v1/health")
    assert response.status_code == 200

#####################################################################################  

def test_root(client):
    """
    Test the root endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ToDo API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "running"
    assert data["docs"] == "/docs"

#####################################################################################  

def test_create_todo_success(client):
    """
    Test the creation of a new todo item.
    """
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo item.",
        "completed": False
    }
    response = client.post("/api/v1/todos", json=todo_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["description"] == todo_data["description"]
    assert data["completed"] == todo_data["completed"]
    assert data["id"] is not None
    assert data["created_at"] is not None
    assert data["updated_at"] is not None

def test_title_too_short(client):
    """
    Test creating a todo item with a title that is too short.
    """
    todo_data = {
        "title": "Hi",  # Title is too short (less than 3 characters)
        "description": "This is a test todo item.",
        "completed": False
    }
    response = client.post("/api/v1/todos", json=todo_data)

    assert response.status_code == 422  # Unprocessable Entity
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "title"]
    assert data["detail"][0]["msg"] == "ensure this value has at least 3 characters"

def test_title_too_long(client):
    """
    Test creating a todo item with a title that is too long.
    """
    todo_data = {
        "title": "T" * 101,  # Title is too long (more than 100 characters)
        "description": "This is a test todo item.",
        "completed": False
    }
    response = client.post("/api/v1/todos", json=todo_data)

    assert response.status_code == 422  # Unprocessable Entity
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "title"]
    assert data["detail"][0]["msg"] == "ensure this value has at most 100 characters"

def test_missing_title(client):
    """
    Test creating a todo item with a missing title.
    """
    todo_data = {
        "description": "This is a test todo item.",
        "completed": False
    }
    response = client.post("/api/v1/todos", json=todo_data)

    assert response.status_code == 422  # Unprocessable Entity
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "title"]
    assert data["detail"][0]["msg"] == "field required"

def test_description_too_long(client):
    """
    Test creating a todo item with a description that is too long.
    """
    todo_data = {
        "title": "Test Todo",
        "description": "D" * 501,  # Description is too long (more than 500 characters)
        "completed": False
    }
    response = client.post("/api/v1/todos", json=todo_data)

    assert response.status_code == 422  # Unprocessable Entity
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "description"]
    assert data["detail"][0]["msg"] == "ensure this value has at most 500 characters"


#####################################################################################  

def test_get_todo(client):
    """
    Test retrieving a todo item by ID.
    """
    # First, create a new todo item
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo item.",
        "completed": False
    }
    create_response = client.post("/api/v1/todos", json=todo_data)
    assert create_response.status_code == 201
    created_todo = create_response.json()
    todo_id = created_todo["id"]

    # Now, retrieve the created todo item
    get_response = client.get(f"/api/v1/todos/{todo_id}")
    assert get_response.status_code == 200
    retrieved_todo = get_response.json()
    assert retrieved_todo == created_todo

#####################################################################################  

def test_get_todo_by_id(client):
    """
    Test retrieving a todo item by its ID.
    """
    # First, create a new todo item
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo item.",
        "completed": False
    }
    create_response = client.post("/api/v1/todos", json=todo_data)
    assert create_response.status_code == 201
    created_todo = create_response.json()
    todo_id = created_todo["id"]

    # Now, retrieve the created todo item by its ID
    get_response = client.get(f"/api/v1/todos/{todo_id}")
    assert get_response.status_code == 200
    retrieved_todo = get_response.json()
    assert retrieved_todo == created_todo

def test_get_todo_invalid_uuid(client):
    """
    Test retrieving a todo item with an invalid ID format.
    """
    invalid_id = "invalid-id"
    response = client.get(f"/api/v1/todos/{invalid_id}")
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["path", "todo_id"]
    assert data["detail"][0]["msg"] == "value is not a valid uuid"

def test_get_todo_not_found(client):
    """
    Test retrieving a todo item that does not exist.
    """
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/todos/{non_existent_id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Todo not found"

#####################################################################################  

def test_update_todo_success(client):
    """
    Test updating an existing todo item.
    """
    # First, create a new todo item
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo item.",
        "completed": False
    }
    create_response = client.post("/api/v1/todos", json=todo_data)
    assert create_response.status_code == 201
    created_todo = create_response.json()
    todo_id = created_todo["id"]

    # Now, update the created todo item
    updated_data = {
        "title": "Updated Test Todo",
        "description": "This is an updated test todo item.",
        "completed": True
    }
    update_response = client.put(f"/api/v1/todos/{todo_id}", json=updated_data)
    assert update_response.status_code == 200
    updated_todo = update_response.json()
    assert updated_todo["title"] == updated_data["title"]
    assert updated_todo["description"] == updated_data["description"]
    assert updated_todo["completed"] == updated_data["completed"]
    assert updated_todo["id"] == todo_id
    assert updated_todo["created_at"] == created_todo["created_at"]
    assert updated_todo["updated_at"] != created_todo["updated_at"]

def test_update_todo_not_found(client):
    """
    Test updating a todo item that does not exist.
    """
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    updated_data = {
        "title": "Updated Test Todo",
        "description": "This is an updated test todo item.",
        "completed": True
    }
    response = client.put(f"/api/v1/todos/{non_existent_id}", json=updated_data)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Todo not found"


#####################################################################################  

def test_delete_todo_success(client):
    """
    Test deleting an existing todo item.
    """
    # First, create a new todo item
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo item.",
        "completed": False
    }
    create_response = client.post("/api/v1/todos", json=todo_data)
    assert create_response.status_code == 201
    created_todo = create_response.json()
    todo_id = created_todo["id"]

    # Now, delete the created todo item
    delete_response = client.delete(f"/api/v1/todos/{todo_id}")
    assert delete_response.status_code == 204

    # Verify that the todo item no longer exists
    get_response = client.get(f"/api/v1/todos/{todo_id}")
    assert get_response.status_code == 404

def test_delete_todo_not_found(client):
    """
    Test deleting a todo item that does not exist.
    """
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/api/v1/todos/{non_existent_id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Todo not found"
    