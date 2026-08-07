# AI Productivity Platform

<p align="center">
  <img src="/FastAPI_production.PNG" alt="AI Productivity Platform Banner" width="100%">
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)
![Celery](https://img.shields.io/badge/Celery-Asynchronous-37814A.svg)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Message%20Broker-FF6600.svg)
![AWS S3](https://img.shields.io/badge/AWS-S3-orange.svg)
![ChromaDB](https://img.shields.io/badge/Vector-Database-7B68EE.svg)
![SentenceTransformers](https://img.shields.io/badge/Embeddings-all--MiniLM--L6--v2-success.svg)
![Groq](https://img.shields.io/badge/LLM-Groq-black.svg)
![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)

</p>

---

## Project Overview

AI Productivity Platform is a backend application that enables users to interact intelligently with their documents using Retrieval-Augmented Generation (RAG). The platform combines asynchronous document processing, semantic search, and conversational memory to deliver context-aware AI responses grounded in user-provided content.

The system follows a modular architecture built with **FastAPI**, where uploaded documents are processed through an asynchronous ETL pipeline, transformed into vector embeddings, and indexed in **ChromaDB** for efficient semantic retrieval. During conversations, relevant transcript chunks are combined with conversational context—including session summaries and recent chat history—to generate accurate, multi-turn responses using a Large Language Model (LLM).

Key architectural principles include:

* Asynchronous document processing using Celery and RabbitMQ
* Modular service-oriented architecture
* Retrieval-Augmented Generation (RAG) with semantic search and reranking
* Persistent chat sessions with conversational memory
* Background AI workflows for scalable processing
* Extensible design for future AI capabilities such as transcript intelligence, task extraction, and sentiment analysis

The project is designed as a production-oriented foundation for AI-powered knowledge management and productivity applications, emphasizing scalability, maintainability, and clean separation of responsibilities.


# Key Features

## Document Processing

* Asynchronous document processing pipeline using Celery and RabbitMQ
* Automatic text extraction and cleaning
* Recursive text chunking for efficient retrieval
* Vector embedding generation and storage in ChromaDB
* Scalable ETL workflow for transcript ingestion

---

## Retrieval-Augmented Generation (RAG)

* Semantic search over indexed transcript content
* Cross-encoder reranking for improved retrieval quality
* Context-aware prompt construction
* AI-generated responses grounded in retrieved transcript context

---

## Conversational Memory

* Persistent chat sessions
* Conversation history stored in PostgreSQL
* Rolling conversation summarization
* Conversation-aware prompt augmentation
* Multi-turn question answering with contextual memory

---

## Background Processing

* Asynchronous document indexing
* Background conversation summarization
* Celery worker architecture with RabbitMQ task queue
* Non-blocking processing for long-running AI tasks

---

## Backend Architecture

* Layered service and repository architecture
* Modular and extensible codebase
* PostgreSQL for relational data persistence
* ChromaDB for vector storage and retrieval
* Environment-based application configuration

---

## Extensibility

The platform is designed to support future AI capabilities, including:

* Hierarchical transcript summarization
* Transcript sentiment analysis
* Task and action item extraction
* Keyword and entity extraction
* User-specific memory and personalization

---


# System Architecture

                                    Client
                                       │
                                       ▼
                               FastAPI REST API
                                       │
                ┌──────────────────────┴──────────────────────┐
                │                                             │
                ▼                                             ▼
       Document Processing                           Conversational RAG
                │                                             │
                ▼                                             ▼
          Upload Transcript                          Chat Session Request
                │                                             │
                ▼                                             ▼
              AWS S3                                Session Management
                │                                             │
                ▼                                             ▼
          RabbitMQ Queue                         Conversation Memory Service
                │                                             │
                ▼                                             ▼
          Celery Worker                     ┌──────────────────┴──────────────────┐
                │                           │                                     │
                ▼                           ▼                                     ▼
         Text Extraction           Session Summary                     Recent Messages
                │                           │                                     │
                ▼                           └──────────────────┬──────────────────┘
         Text Cleaning                                         │
                │                                               ▼
                ▼                                     Retrieval Service
      Recursive Chunking                                      │
                │                                              ▼
                ▼                                     Query Embedding
      Embedding Generation                                    │
                │                                              ▼
                ▼                                     ChromaDB Search
         ChromaDB Storage                                     │
                                                              ▼
                                                  Cross Encoder Reranking
                                                              │
                                                              ▼
                                                      Prompt Builder
                                                              │
                    ┌─────────────────────────────────────────┼────────────────────────────────────────┐
                    │                                         │                                        │
                    ▼                                         ▼                                        ▼
          Conversation Summary                    Recent Conversation                    Retrieved Transcript Context
                    └─────────────────────────────────────────┬────────────────────────────────────────┘
                                                              │
                                                              ▼
                                                           Groq LLM
                                                              │
                                                              ▼
                                                     AI Generated Response
                                                              │
                                                              ▼
                                                  Save Chat Messages (PostgreSQL)
                                                              │
                                                              ▼
                                            Celery Conversation Summarization
                                                              │
                                                              ▼
                                               Update Session Summary (PostgreSQL)



# Project Structure

```text
app/
├── api/                    # REST API endpoints
│   ├── v1/
│   └── v2/
│
├── celery/                 # Background task workers
│   └── tasks/
│
├── core/                   # Configuration, logging, dependencies
│
├── database/               # Database configuration
│
├── models/                 # SQLAlchemy models
│
├── repositories/           # Data access layer
│
├── schemas/                # Pydantic request/response models
│
├── services/
│   ├── auth/               # Authentication services
│   ├── builder/            # Prompt builders
│   ├── embeddings/         # Embedding generation
│   ├── etl/                # Document processing pipeline
│   ├── llm/                # LLM integration
│   ├── retrieval/          # RAG retrieval pipeline
│   ├── session/            # Session and conversation memory
│   ├── storage/            # AWS S3 storage
│   └── vectorstore/        # ChromaDB operations
│
├── prompts/                # Prompt templates
│
└── utils/                  # Shared utility functions

alembic/                    # Database migrations
tests/                      # Unit and integration tests
```


# Processing Pipeline

The platform consists of two primary processing pipelines:

* **Upload Pipeline** – Responsible for processing uploaded transcripts and preparing them for semantic search.
* **Chat Pipeline** – Responsible for handling conversational requests using Retrieval-Augmented Generation (RAG) and conversational memory.

---

## Upload Pipeline

The upload pipeline processes transcripts asynchronously to ensure the API remains responsive.

```text
Client
    │
    ▼
Upload Transcript
    │
    ▼
Store File (AWS S3)
    │
    ▼
Create Transcript Record (PostgreSQL)
    │
    ▼
Queue ETL Task (RabbitMQ)
    │
    ▼
Celery Worker
    │
    ▼
Text Extraction
    │
    ▼
Text Cleaning
    │
    ▼
Recursive Chunking
    │
    ▼
Embedding Generation
    │
    ▼
Store Embeddings (ChromaDB)
    │
    ▼
Update Transcript Status → READY
```

---

## Chat Pipeline

The chat pipeline combines conversational memory with semantic retrieval to generate context-aware responses.

```text
Client
    │
    ▼
Chat Request
    │
    ▼
Validate Session
    │
    ▼
Retrieve Conversation Context
    │
    ├── Session Summary
    └── Recent Messages
    │
    ▼
Semantic Retrieval
    │
    ├── Query Embedding
    ├── ChromaDB Search
    └── Cross Encoder Reranking
    │
    ▼
Prompt Construction
    │
    ├── Conversation Summary
    ├── Recent Messages
    ├── Retrieved Transcript Chunks
    └── User Query
    │
    ▼
LLM Response
    │
    ▼
Store User & AI Messages (PostgreSQL)
    │
    ▼
Check Summarization Threshold
    │
    ▼
Queue Background Summary Task (Celery)
    │
    ▼
Update Session Summary (PostgreSQL)
```


# Technology Stack

| Layer                | Technology              | Purpose                                                               |
| -------------------- | ----------------------- | --------------------------------------------------------------------- |
| Programming Language | Python 3.13             | Backend development                                                   |
| Web Framework        | FastAPI                 | REST API and dependency injection                                     |
| Data Validation      | Pydantic v2             | Request and response validation                                       |
| ORM                  | SQLAlchemy              | Database abstraction and ORM                                          |
| Database             | PostgreSQL              | Persistent storage for users, transcripts, sessions, and chat history |
| Database Migrations  | Alembic                 | Schema versioning and migrations                                      |
| Object Storage       | AWS S3                  | Transcript file storage                                               |
| Task Queue           | RabbitMQ                | Message broker for asynchronous processing                            |
| Background Workers   | Celery                  | ETL and AI background tasks                                           |
| Vector Database      | ChromaDB                | Semantic vector storage and retrieval                                 |
| Embedding Model      | BAAI/bge-small-en-v1.5  | Dense vector embedding generation                                     |
| Reranking Model      | BAAI/bge-reranker-base  | Cross-encoder reranking of retrieved chunks                           |
| Large Language Model | Groq API                | Retrieval-Augmented Generation (RAG) and conversational summarization |
| Containerization     | Docker & Docker Compose | Development and deployment environment                                |



# API Overview

The platform exposes a RESTful API organized into resource-based endpoints.

## Authentication

| Method | Endpoint                | Description                               |
| ------ | ----------------------- | ----------------------------------------- |
| POST   | `/api/v1/auth/register` | Register a new user                       |
| POST   | `/api/v1/auth/login`    | Authenticate and obtain an access token   |
| GET    | `/api/v1/auth/me`       | Retrieve the authenticated user's profile |

---

## Transcripts

| Method | Endpoint                              | Description                                  |
| ------ | ------------------------------------- | -------------------------------------------- |
| POST   | `/api/v2/transcripts/upload`          | Upload a transcript for processing           |
| GET    | `/api/v2/transcripts`                 | List uploaded transcripts                    |
| GET    | `/api/v2/transcripts/{transcript_id}` | Retrieve transcript details                  |
| DELETE | `/api/v2/transcripts/{transcript_id}` | Delete a transcript and associated resources |

---

## Sessions

| Method | Endpoint                        | Description                            |
| ------ | ------------------------------- | -------------------------------------- |
| POST   | `/api/v2/sessions`              | Create a chat session for a transcript |
| GET    | `/api/v2/sessions`              | List user chat sessions                |
| GET    | `/api/v2/sessions/{session_id}` | Retrieve session details               |
| DELETE | `/api/v2/sessions/{session_id}` | Delete a session and its chat history  |

---

## Chat

| Method | Endpoint                                 | Description                                            |
| ------ | ---------------------------------------- | ------------------------------------------------------ |
| POST   | `/api/v2/sessions/{session_id}/chat`     | Send a message and receive a context-aware AI response |
| GET    | `/api/v2/sessions/{session_id}/messages` | Retrieve chat history for a session                    |

---

## Semantic Search

| Method | Endpoint                   | Description                                                    |
| ------ | -------------------------- | -------------------------------------------------------------- |
| POST   | `/api/v2/retrieval/search` | Perform transcript semantic search without conversation memory |

---

## Interactive API Documentation

Once the application is running, the API documentation is available at:

| Documentation | URL                           |
| ------------- | ----------------------------- |
| Swagger UI    | `http://localhost:8000/docs`  |
| ReDoc         | `http://localhost:8000/redoc` |


# Running the Project

## Prerequisites

Ensure the following software is installed:

* Docker
* Docker Compose
* Git

---

## Clone the Repository

```bash
git clone <repository-url>
cd ai-productivity-platform
```

---

## Configure Environment Variables

Create a `.env` file in the project root and configure the required environment variables.

Example:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=ai_productivity

AWS_ACCESS_KEY_ID=<your-access-key>
AWS_SECRET_ACCESS_KEY=<your-secret-key>
AWS_S3_BUCKET=<your-bucket>

GROQ_API_KEY=<your-groq-api-key>

CHROMA_PERSIST_DIRECTORY=/app/chroma_db
```

> Refer to the `.env.example` file for the complete list of configuration options.

---

## Start the Application

Build and start all services:

```bash
docker compose up --build
```

To run the application in detached mode:

```bash
docker compose up -d --build
```

---

## Database Migration

Apply database migrations after the services have started:

```bash
docker compose exec api alembic upgrade head
```

---

## Access the Application

| Service     | URL                           |
| ----------- | ----------------------------- |
| FastAPI API | `http://localhost:8000`       |
| Swagger UI  | `http://localhost:8000/docs`  |
| ReDoc       | `http://localhost:8000/redoc` |

---

## Stop the Application

```bash
docker compose down
```

To remove containers, networks, and volumes:

```bash
docker compose down -v
```


# Configuration

The application is configured using environment variables. Copy `.env.example` to `.env` and update the values according to your environment.

```bash
cp .env.example .env
```

The configuration is organized into the following categories:

| Category            | Description                                                          |
| ------------------- | -------------------------------------------------------------------- |
| Application         | General application settings, logging, and environment configuration |
| Database            | PostgreSQL connection and database settings                          |
| Authentication      | JWT secrets, token expiration, and authentication configuration      |
| AWS S3              | Credentials and bucket configuration for transcript storage          |
| Celery & RabbitMQ   | Background task processing and message broker configuration          |
| ChromaDB            | Vector database persistence and connection settings                  |
| Embedding Models    | Embedding model configuration and retrieval parameters               |
| Reranking           | Cross-encoder reranking model and retrieval configuration            |
| LLM                 | Groq API configuration and model selection                           |
| ETL Pipeline        | Chunking strategy, overlap, and document processing settings         |
| Conversation Memory | Chat history window and summarization thresholds                     |

---

## Example Configuration

```env
# Database
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=ai_productivity
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

# LLM
GROQ_API_KEY=<your-api-key>

# AWS
AWS_ACCESS_KEY_ID=<your-access-key>
AWS_SECRET_ACCESS_KEY=<your-secret-key>
AWS_S3_BUCKET=<your-bucket>

# Conversation Memory
CHAT_SUMMARIZATION_THRESHOLD=20
LAST_N_MESSAGES=6
```

> **Note:** The complete list of supported configuration variables is available in the `.env.example` file. New configuration options should be added there to keep this documentation concise.


# Current Capabilities

The platform currently provides the following functionality:

### Authentication

* User registration and authentication
* JWT-based authorization
* Protected API endpoints

### Document Management

* Transcript upload and storage
* Asynchronous document processing
* Transcript lifecycle management

### Retrieval-Augmented Generation (RAG)

* Semantic search over transcript content
* Cross-encoder reranking
* Context-aware question answering
* AI responses grounded in retrieved transcript chunks

### Conversational AI

* Persistent chat sessions
* Conversation history stored in PostgreSQL
* Rolling conversation summarization
* Multi-turn conversations with conversational memory
* Background summary generation using Celery

### Infrastructure

* PostgreSQL for relational data
* ChromaDB for vector storage
* RabbitMQ and Celery for asynchronous processing
* Docker-based development environment
* RESTful API with OpenAPI documentation


# Roadmap

The platform is actively evolving with a focus on expanding AI capabilities while maintaining a modular and scalable architecture.

## Transcript Intelligence

* Hierarchical transcript summarization
* Transcript sentiment analysis
* Task and action item extraction
* Keyword and entity extraction
* Transcript metadata generation

## Conversational AI

* User-level long-term memory
* Personalized conversation context
* Token usage tracking and quota management
* Memory optimization strategies

## Retrieval

* Hybrid search (vector + keyword)
* Metadata-aware retrieval
* Query expansion and rewriting
* Advanced retrieval optimization

## AI Workflows

* Multi-stage AI processing pipelines
* Configurable background AI tasks
* Automated transcript analysis
* Extensible prompt management

## Platform Enhancements

* API versioning and improved developer experience
* Monitoring and observability
* Performance optimization
* Comprehensive unit and integration test coverage
* Production deployment and scaling improvements

---

#  License

This project is licensed under the **Apache License 2.0**.

See the [LICENSE](LICENSE) file for details.