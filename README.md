# Todo API

A production-inspired REST API for managing todo items, built with **FastAPI** and **Python**. Designed as a learning project to demonstrate professional backend architecture patterns applied to a simple, approachable domain.

---

## Version History

| Version | Storage Backend | Description |
|---|---|---|
| **v1.0** | JSON file | Local JSON file persistence. Simple, zero-setup storage. |
| **v2.0** | PostgreSQL on AWS RDS | Production-grade relational database. SQLAlchemy ORM, connection pooling, cloud-hosted on Amazon RDS. Alembic migrations for safe schema changes. Isolated SQLite test database. |

> **Current version: v2.0 — PostgreSQL AWS Database**

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [API Endpoints](#api-endpoints)
- [Schemas](#schemas)
- [Getting Started](#getting-started)
- [Database Migrations](#database-migrations)
- [Running Tests](#running-tests)

---

## Overview

This API provides full **CRUD** (Create, Read, Update, Delete) operations for todo items. Data is persisted in a **PostgreSQL database hosted on AWS RDS**, replacing the original JSON file storage. The codebase is intentionally structured to mirror real-world production patterns — layered concerns, dependency injection, custom exception handling, request logging, and a comprehensive test suite.

![FastAPI Production](FastAPI_production.PNG)

**Tech Stack:**

| Tool | Purpose |
|---|---|
| FastAPI 0.138 | Web framework |
| Uvicorn 0.49 | ASGI server |
| Pydantic v2 | Data validation and serialization |
| pydantic-settings | Environment configuration |
| SQLAlchemy | ORM and database session management |
| psycopg2-binary | PostgreSQL driver |
| AWS RDS (PostgreSQL) | Cloud-hosted relational database |
| Alembic | Database migration tool |
| Pytest 9.1 | Testing framework |
| HTTPX | HTTP client for testing |

---

## Project Structure

```
app/
├── main.py                           # FastAPI app factory, startup event (creates DB tables)
│
├── api/
│   └── v1/
│       ├── router.py                 # Combines all v1 route groups
│       └── routes/
│           ├── health.py             # GET /api/v1/health
│           └── todos.py              # Todo CRUD endpoints
│
├── core/
│   ├── config.py                     # Settings loaded from .env (pydantic-settings)
│   ├── dependencies.py               # FastAPI dependency injection chain
│   ├── exception_handlers.py         # Maps custom exceptions to HTTP responses
│   ├── logging.py                    # Logging configuration
│   └── middleware.py                 # Request/response timing and logging
│
├── database/
│   ├── base.py                       # SQLAlchemy DeclarativeBase
│   ├── database.py                   # Engine, SessionLocal, get_db() dependency
│   └── models.py                     # TodoModel ORM table definition
│
├── schemas/
│   └── todo.py                       # Pydantic models (request/response shapes)
│
├── services/
│   └── todo_service.py               # Business logic (UUID, timestamps, validation)
│
├── repositories/
│   ├── postgres_todo_repository.py   # PostgreSQL CRUD via SQLAlchemy
│   └── json_todo_repository.py       # Legacy JSON CRUD (retained for reference)
│
├── storage/
│   └── json_storage.py               # Legacy JSON file I/O (retained for reference)
│
├── exceptions/
│   └── todo.py                       # TodoNotFoundError custom exception
│
├── tests/
│   ├── conftest.py                   # Pytest fixtures (SQLite in-memory test DB)
│   ├── fakes.py                      # FakeTodoRepository for unit tests
│   ├── test_api.py                   # API integration tests (SQLite, isolated)
│   ├── test_service.py               # Service unit tests (in-memory fake)
│   ├── test_repository.py            # JSON repository unit tests
│   └── test_storage.py               # JSON storage tests
│
migrations/
├── env.py                            # Alembic environment (reads DATABASE_URL from .env)
├── script.py.mako                    # Migration file template
└── versions/
    └── 20260703_0637_fabbfc95d6f4_initial_schema.py  # Baseline revision
alembic.ini                           # Alembic configuration
```

---

## Architecture

The app follows a **layered architecture** — each layer has a single responsibility and communicates only with the layer directly below it.

```
HTTP Request
     │
     ▼
  Routes          — Handle HTTP: parse input, return responses, set status codes
     │
     ▼
  Services        — Business logic: generate IDs, set timestamps, enforce rules
     │
     ▼
  Repositories    — Data access: CRUD operations via SQLAlchemy ORM
     │
     ▼
  Database        — PostgreSQL on AWS RDS (managed via SQLAlchemy sessions)
```

**Dependency injection** wires these layers together at runtime via FastAPI's `Depends()` system, defined in `core/dependencies.py`:

```
get_service
  └── get_postgres_repository
        └── get_db  →  SessionLocal()  →  AWS RDS PostgreSQL
```

This makes each layer independently testable — integration tests override `get_db` with a test session that cleans up after itself, while unit tests swap the repository entirely for an in-memory `FakeTodoRepository`.

---

## API Endpoints

Base URL prefix: `/api/v1`

### Health

| Method | Path | Description | Status |
|---|---|---|---|
| GET | `/api/v1/health` | Liveness check | 200 |

**Response:**
```json
{ "status": "healthy" }
```

---

### Todos

| Method | Path | Description | Success Status |
|---|---|---|---|
| GET | `/api/v1/todos` | List all todos | 200 |
| POST | `/api/v1/todos` | Create a new todo | 201 |
| GET | `/api/v1/todos/{todo_id}` | Get a todo by UUID | 200 |
| PUT | `/api/v1/todos/{todo_id}` | Update a todo (partial) | 200 |
| DELETE | `/api/v1/todos/{todo_id}` | Delete a todo | 204 |

#### Error Responses

| Scenario | Status | Body |
|---|---|---|
| Todo not found | 404 | `{"detail": "Todo with id '...' was not found."}` |
| Invalid UUID format | 422 | Pydantic validation error |
| Invalid request body | 422 | Pydantic validation error |

---

## Schemas

### `TodoCreate` (POST request body)

| Field | Type | Rules |
|---|---|---|
| `title` | `string` | Required, 3–100 characters |
| `description` | `string \| null` | Optional, max 500 characters |

### `TodoUpdate` (PUT request body)

All fields are optional — send only the fields you want to change.

| Field | Type |
|---|---|
| `title` | `string \| null` |
| `description` | `string \| null` |
| `completed` | `boolean \| null` |

### `TodoResponse`

| Field | Type |
|---|---|
| `id` | `UUID` |
| `title` | `string` |
| `description` | `string \| null` |
| `completed` | `boolean` |
| `created_at` | `datetime (UTC)` |
| `updated_at` | `datetime (UTC)` |

### `TodoListResponse`

| Field | Type |
|---|---|
| `total` | `integer` |
| `items` | `TodoResponse[]` |

---

## Getting Started

### Prerequisites

- Python 3.11+
- A PostgreSQL database (local or cloud — e.g. AWS RDS)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd Fast_api

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
APP_NAME=ToDo API
APP_VERSION=2.0.0
DEBUG=True
DATA_FILE=app/data/todo.json
DATABASE_URL=postgresql+psycopg2://<user>:<password>@<host>:<port>/<database>
```

| Variable | Description |
|---|---|
| `APP_NAME` | Name shown in API metadata |
| `APP_VERSION` | Version shown in API metadata |
| `DEBUG` | Enables debug mode |
| `DATA_FILE` | Path to legacy JSON file (unused in v2, kept for reference) |
| `DATABASE_URL` | Full SQLAlchemy connection string to your PostgreSQL database |

> **First-time setup:** run `alembic upgrade head` after configuring `.env` to create all tables via the migration history. See the [Database Migrations](#database-migrations) section below.

### Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

On startup you will see a log line confirming the database is ready:
```
INFO | app.main | Database tables verified / created successfully.
```

Interactive docs are served automatically at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## Database Migrations

Schema changes are managed with **Alembic**. Every change to a model column is captured in a versioned migration file and applied to the database in a controlled, reversible way.

### Current migration history

| Revision | Description |
|---|---|
| `fabbfc95d6f4` | `initial_schema` — baseline for the `todos` table |

### Common commands

```bash
# Apply all pending migrations (use on a fresh database or after pulling new migrations)
alembic upgrade head

# Check which revision the database is currently at
alembic current

# Show the full migration history
alembic history --verbose

# Roll back the last applied migration
alembic downgrade -1
```

### Adding a new column (example workflow)

**Step 1 — Update the model** in `app/database/models.py`:
```python
priority: Mapped[int] = mapped_column(Integer, default=0)
```

**Step 2 — Generate the migration** (Alembic diffs the model against the live DB):
```bash
alembic revision --autogenerate -m "add_priority_to_todos"
```

**Step 3 — Review** the generated file in `migrations/versions/` and confirm the SQL is correct.

**Step 4 — Apply it:**
```bash
alembic upgrade head
```

> `alembic.ini` does **not** contain the database URL. Alembic reads `DATABASE_URL` directly from `.env` at runtime, so credentials are never stored in a config file.

---

## Running Tests

```bash
pytest
```

The test suite covers four layers:

| File | Layer | Approach | Database |
|---|---|---|---|
| `test_api.py` | API (integration) | Real `TestClient` against live app | **SQLite in-memory** (never touches PostgreSQL) |
| `test_service.py` | Service | `FakeTodoRepository` (in-memory) | None |
| `test_repository.py` | Repository | `JsonTodoRepository` against a temp file | None |
| `test_storage.py` | Storage | Fixture validation | None |

> Integration tests use a shared **in-memory SQLite database** built from the same SQLAlchemy models as production. The schema is identical, the production PostgreSQL database is never opened, and all rows are cleared between tests. This also makes the test suite run significantly faster (~24 s vs ~65 s over the network).

Run with verbose output:

```bash
pytest -v
```

---

## License

See [LICENSE](LICENSE).

